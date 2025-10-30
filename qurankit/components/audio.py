#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔊 QuranAudioComponent - مشغل الصوت
Audio Player Component for Quran applications
"""

import os
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import urllib.request
import urllib.error

from PyQt6.QtCore import QObject, pyqtSignal, QUrl, QTimer, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QSlider, QLabel, QCheckBox, QComboBox)


class AudioDownloader(QObject):
    """مدير تحميل الملفات الصوتية"""

    download_progress = pyqtSignal(int)  # نسبة التحميل
    download_finished = pyqtSignal(str)  # المسار المحلي
    download_error = pyqtSignal(str)     # رسالة الخطأ

    def __init__(self, cache_dir: Path = None, reciters_config: Dict = None):
        super().__init__()
        self.cache_dir = cache_dir or Path.home() / '.qurankit' / 'audio'
        self.reciters = reciters_config or {}
        self.current_download = None

    def get_audio_filename(self, sura: int, aya: int) -> str:
        """الحصول على اسم الملف الصوتي"""
        # التنسيق: 001001.mp3 (سورة + آية بـ 3 أرقام)
        return f"{sura:03d}{aya:03d}.mp3"

    def get_local_path(self, reciter_id: str, sura: int, aya: int) -> Path:
        """الحصول على المسار المحلي للملف"""
        filename = self.get_audio_filename(sura, aya)
        reciter_dir = self.cache_dir / reciter_id
        reciter_dir.mkdir(parents=True, exist_ok=True)
        return reciter_dir / filename

    def get_remote_url(self, reciter_id: str, sura: int, aya: int) -> str:
        """الحصول على رابط التحميل"""
        if reciter_id not in self.reciters:
            raise ValueError(f"Unknown reciter: {reciter_id}")

        reciter_info = self.reciters[reciter_id]
        filename = self.get_audio_filename(sura, aya)
        return f"{reciter_info['url_base']}/{filename}"

    def is_cached(self, reciter_id: str, sura: int, aya: int) -> bool:
        """التحقق من وجود الملف في الكاش"""
        local_path = self.get_local_path(reciter_id, sura, aya)
        return local_path.exists() and local_path.stat().st_size > 0

    def download_audio(self, reciter_id: str, sura: int, aya: int):
        """تحميل ملف صوتي"""
        try:
            # التحقق من الكاش أولاً
            if self.is_cached(reciter_id, sura, aya):
                local_path = self.get_local_path(reciter_id, sura, aya)
                self.download_finished.emit(str(local_path))
                return

            # التحميل من الإنترنت
            url = self.get_remote_url(reciter_id, sura, aya)
            local_path = self.get_local_path(reciter_id, sura, aya)

            def reporthook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = int((block_num * block_size / total_size) * 100)
                    self.download_progress.emit(min(percent, 100))

            urllib.request.urlretrieve(url, str(local_path), reporthook)
            self.download_finished.emit(str(local_path))

        except urllib.error.URLError as e:
            error_msg = f"خطأ في التحميل: {e.reason}"
            self.download_error.emit(error_msg)
        except Exception as e:
            error_msg = f"خطأ غير متوقع: {str(e)}"
            self.download_error.emit(error_msg)


class QuranAudioComponent(QObject):
    """مكون تشغيل الصوت للقرآن الكريم"""

    # الإشارات
    state_changed = pyqtSignal(str)      # حالة المشغل
    position_changed = pyqtSignal(int)   # موضع التشغيل
    duration_changed = pyqtSignal(int)   # مدة الملف
    aya_changed = pyqtSignal(int, int)   # تغيير السورة والآية
    error_occurred = pyqtSignal(str)     # خطأ

    def __init__(self, database=None, config: Dict = None):
        super().__init__()

        self.database = database
        self.config = config or {}

        # المشغل
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # الربط بالإشارات
        self.player.positionChanged.connect(self.position_changed.emit)
        self.player.durationChanged.connect(self.duration_changed.emit)
        self.player.errorOccurred.connect(self.on_error)
        self.player.playbackStateChanged.connect(self.on_state_changed)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

        # المحمل
        cache_dir = self.config.get('cache_dir')
        reciters = self.config.get('reciters', {})
        self.downloader = AudioDownloader(cache_dir, reciters)
        self.downloader.download_finished.connect(self.on_download_finished)
        self.downloader.download_error.connect(self.on_download_error)

        # الحالة
        self.current_reciter = self.config.get('default_reciter', 'abdulbasit')
        self.current_sura = 1
        self.current_aya = 1
        self.is_loading = False
        self.auto_play_next = self.config.get('auto_play_next', True)
        self.repeat_aya = self.config.get('repeat_aya', False)

        # قائمة الانتظار
        self.pending_play = None

    def set_reciter(self, reciter_id: str):
        """تعيين القارئ"""
        if reciter_id in self.downloader.reciters:
            self.current_reciter = reciter_id

    def play_ayah(self, sura: int, ayah: int):
        """تشغيل آية"""
        self.current_sura = sura
        self.current_aya = ayah
        self.aya_changed.emit(sura, ayah)

        # التحقق من الكاش
        if self.downloader.is_cached(self.current_reciter, sura, ayah):
            local_path = self.downloader.get_local_path(self.current_reciter, sura, ayah)
            self._play_file(str(local_path))
        else:
            # تحميل الملف
            self.is_loading = True
            self.state_changed.emit("loading")
            self.pending_play = (sura, ayah)
            self.downloader.download_audio(self.current_reciter, sura, ayah)

    def _play_file(self, file_path: str):
        """تشغيل ملف"""
        file_url = QUrl.fromLocalFile(file_path)
        self.player.setSource(file_url)
        self.player.play()

    def on_download_finished(self, file_path: str):
        """عند انتهاء التحميل"""
        self.is_loading = False

        if self.pending_play:
            sura, aya = self.pending_play
            if sura == self.current_sura and aya == self.current_aya:
                self._play_file(file_path)
            self.pending_play = None

    def on_download_error(self, error_msg: str):
        """عند حدوث خطأ في التحميل"""
        self.is_loading = False
        self.error_occurred.emit(error_msg)
        self.state_changed.emit("error")

    def on_error(self, error):
        """عند حدوث خطأ في التشغيل"""
        error_msg = self.player.errorString()
        self.error_occurred.emit(error_msg)
        self.state_changed.emit("error")

    def on_state_changed(self, state):
        """عند تغيير حالة التشغيل"""
        states = {
            QMediaPlayer.PlaybackState.PlayingState: "playing",
            QMediaPlayer.PlaybackState.PausedState: "paused",
            QMediaPlayer.PlaybackState.StoppedState: "stopped"
        }
        state_name = states.get(state, "unknown")
        self.state_changed.emit(state_name)

    def on_media_status_changed(self, status):
        """عند تغيير حالة الوسائط"""
        # عند انتهاء التشغيل
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.repeat_aya:
                # إعادة تشغيل نفس الآية
                self.play_ayah(self.current_sura, self.current_aya)
            elif self.auto_play_next:
                # تشغيل الآية التالية
                self.play_next()

    def play(self):
        """تشغيل"""
        if not self.is_loading:
            self.player.play()

    def pause(self):
        """إيقاف مؤقت"""
        self.player.pause()

    def stop(self):
        """إيقاف"""
        self.player.stop()

    def play_pause(self):
        """تبديل التشغيل/الإيقاف"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def play_next(self):
        """تشغيل الآية التالية"""
        if not self.database:
            return

        try:
            sura_info = self.database.get_sura_info(self.current_sura)
            next_aya = self.current_aya + 1
            next_sura = self.current_sura

            # إذا تجاوزنا آخر آية في السورة
            if next_aya > sura_info.get('ayas_count', 0):
                if self.current_sura < 114:
                    next_sura = self.current_sura + 1
                    next_aya = 1
                else:
                    return  # نهاية القرآن

            self.play_ayah(next_sura, next_aya)

        except Exception as e:
            self.error_occurred.emit(f"خطأ في الانتقال للآية التالية: {e}")

    def play_previous(self):
        """تشغيل الآية السابقة"""
        if not self.database:
            return

        try:
            prev_aya = self.current_aya - 1
            prev_sura = self.current_sura

            # إذا كنا في أول آية من السورة
            if prev_aya < 1:
                if self.current_sura > 1:
                    prev_sura = self.current_sura - 1
                    sura_info = self.database.get_sura_info(prev_sura)
                    prev_aya = sura_info.get('ayas_count', 1)
                else:
                    return  # بداية القرآن

            self.play_ayah(prev_sura, prev_aya)

        except Exception as e:
            self.error_occurred.emit(f"خطأ في الانتقال للآية السابقة: {e}")

    def set_volume(self, volume: float):
        """تعيين مستوى الصوت (0.0 - 1.0)"""
        self.audio_output.setVolume(volume)

    def get_volume(self) -> float:
        """الحصول على مستوى الصوت"""
        return self.audio_output.volume()

    def set_position(self, position: int):
        """تعيين موضع التشغيل (بالميلي ثانية)"""
        self.player.setPosition(position)

    def get_position(self) -> int:
        """الحصول على موضع التشغيل"""
        return self.player.position()

    def get_duration(self) -> int:
        """الحصول على مدة الملف"""
        return self.player.duration()

    def set_auto_play_next(self, enabled: bool):
        """تفعيل/تعطيل التشغيل التلقائي للآية التالية"""
        self.auto_play_next = enabled

    def set_repeat_aya(self, enabled: bool):
        """تفعيل/تعطيل تكرار الآية"""
        self.repeat_aya = enabled

    def get_state(self) -> str:
        """الحصول على حالة المشغل"""
        if self.is_loading:
            return "loading"

        states = {
            QMediaPlayer.PlaybackState.PlayingState: "playing",
            QMediaPlayer.PlaybackState.PausedState: "paused",
            QMediaPlayer.PlaybackState.StoppedState: "stopped"
        }
        return states.get(self.player.playbackState(), "unknown")

    def cleanup(self):
        """تنظيف الموارد"""
        self.stop()
        self.player.setSource(QUrl())


class QuranAudioWidget(QWidget):
    """لوحة التحكم الصوتي"""

    # إشارات مخصصة
    play_requested = pyqtSignal(int, int)      # طلب تشغيل (سورة، آية)
    pause_requested = pyqtSignal()              # طلب إيقاف مؤقت
    stop_requested = pyqtSignal()               # طلب إيقاف
    next_requested = pyqtSignal()               # طلب التالي
    previous_requested = pyqtSignal()           # طلب السابق
    volume_changed = pyqtSignal(float)          # تغيير الصوت

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = False
        self.current_position = 0
        self.duration = 0
        self.init_ui()

    def init_ui(self):
        """بناء الواجهة"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(5)

        # أزرار التحكم
        controls_layout = QHBoxLayout()

        self.prev_btn = QPushButton("⏮")
        self.prev_btn.clicked.connect(self.previous_requested.emit)
        controls_layout.addWidget(self.prev_btn)

        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        controls_layout.addWidget(self.play_pause_btn)

        self.next_btn = QPushButton("⏭")
        self.next_btn.clicked.connect(self.next_requested.emit)
        controls_layout.addWidget(self.next_btn)

        self.stop_btn = QPushButton("⏹")
        self.stop_btn.clicked.connect(self.stop_requested.emit)
        controls_layout.addWidget(self.stop_btn)

        controls_layout.addStretch()

        self.auto_play_checkbox = QCheckBox("تشغيل تلقائي")
        controls_layout.addWidget(self.auto_play_checkbox)

        self.repeat_checkbox = QCheckBox("تكرار")
        controls_layout.addWidget(self.repeat_checkbox)

        main_layout.addLayout(controls_layout)

        # شريط التقدم
        progress_layout = QHBoxLayout()

        self.current_time_label = QLabel("0:00")
        progress_layout.addWidget(self.current_time_label)

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)
        progress_layout.addWidget(self.progress_slider, 1)

        self.duration_label = QLabel("0:00")
        progress_layout.addWidget(self.duration_label)

        main_layout.addLayout(progress_layout)

        # مستوى الصوت
        volume_layout = QHBoxLayout()

        volume_layout.addWidget(QLabel("🔊"))

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_slider)

        self.volume_label = QLabel("80%")
        volume_layout.addWidget(self.volume_label)

        volume_layout.addStretch()

        main_layout.addLayout(volume_layout)

    def on_play_pause_clicked(self):
        """عند النقر على زر التشغيل/الإيقاف"""
        if self.is_playing:
            self.pause_requested.emit()
        else:
            self.play_requested.emit(0, 0)

    def on_volume_changed(self, value):
        """عند تغيير مستوى الصوت"""
        self.volume_label.setText(f"{value}%")
        self.volume_changed.emit(value / 100.0)

    def set_playing_state(self, is_playing: bool):
        """تعيين حالة التشغيل"""
        self.is_playing = is_playing
        self.play_pause_btn.setText("⏸" if is_playing else "▶")

    def set_position(self, position_ms: int):
        """تعيين موضع التشغيل (بالميلي ثانية)"""
        self.current_position = position_ms
        minutes = position_ms // 60000
        seconds = (position_ms % 60000) // 1000
        self.current_time_label.setText(f"{minutes}:{seconds:02d}")

        if self.duration > 0:
            progress = int((position_ms / self.duration) * 1000)
            self.progress_slider.setValue(progress)

    def set_duration(self, duration_ms: int):
        """تعيين المدة الكلية (بالميلي ثانية)"""
        self.duration = duration_ms
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        self.duration_label.setText(f"{minutes}:{seconds:02d}")
