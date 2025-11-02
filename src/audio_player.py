#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
🎵 مدير التشغيل الصوتي - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

import os
from pathlib import Path
from typing import Optional, Callable
import urllib.request
import urllib.error

from PyQt6.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from config import *


class AudioDownloader(QObject):
    """مدير تحميل الملفات الصوتية"""

    download_progress = pyqtSignal(int)  # نسبة التحميل
    download_finished = pyqtSignal(str)  # المسار المحلي
    download_error = pyqtSignal(str)     # رسالة الخطأ

    def __init__(self):
        super().__init__()
        self.current_download = None

    def get_audio_filename(self, sura: int, aya: int) -> str:
        """الحصول على اسم الملف الصوتي"""
        # التنسيق: 001001.mp3 (سورة + آية بـ 3 أرقام)
        return f"{sura:03d}{aya:03d}.mp3"

    def get_local_path(self, reciter_id: str, sura: int, aya: int) -> Path:
        """الحصول على المسار المحلي للملف"""
        filename = self.get_audio_filename(sura, aya)
        reciter_dir = AUDIO_CACHE_DIR / reciter_id
        reciter_dir.mkdir(parents=True, exist_ok=True)
        return reciter_dir / filename

    def get_remote_url(self, reciter_id: str, sura: int, aya: int) -> str:
        """الحصول على رابط التحميل"""
        reciter_info = RECITERS.get(reciter_id, RECITERS[DEFAULT_RECITER])
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

            print(f"🔽 تحميل: {url}")

            def reporthook(block_num, block_size, total_size):
                if total_size > 0:
                    percent = int((block_num * block_size / total_size) * 100)
                    self.download_progress.emit(min(percent, 100))

            urllib.request.urlretrieve(url, str(local_path), reporthook)

            print(f"✅ تم التحميل: {local_path}")
            self.download_finished.emit(str(local_path))

        except urllib.error.URLError as e:
            error_msg = f"خطأ في التحميل: {e.reason}"
            print(f"❌ {error_msg}")
            self.download_error.emit(error_msg)
        except Exception as e:
            error_msg = f"خطأ غير متوقع: {str(e)}"
            print(f"❌ {error_msg}")
            self.download_error.emit(error_msg)

    def preload_next_ayas(self, reciter_id: str, sura: int, aya: int, count: int = 3):
        """تحميل مسبق للآيات التالية"""
        from db_manager import QuranDatabase

        try:
            db = QuranDatabase()
            for i in range(1, count + 1):
                next_aya = aya + i
                sura_info = db.get_sura_info(sura)

                # إذا تجاوزنا آخر آية في السورة، انتقل للسورة التالية
                if next_aya > sura_info['ayas_count']:
                    if sura < 114:
                        sura += 1
                        next_aya = 1
                    else:
                        break

                # تحميل إذا لم يكن في الكاش
                if not self.is_cached(reciter_id, sura, next_aya):
                    self.download_audio(reciter_id, sura, next_aya)

            db.close()
        except Exception as e:
            print(f"⚠️  خطأ في التحميل المسبق: {e}")


class QuranAudioPlayer(QObject):
    """مشغل الصوتيات للقرآن الكريم"""

    # الإشارات
    state_changed = pyqtSignal(str)      # حالة المشغل
    position_changed = pyqtSignal(int)   # موضع التشغيل
    duration_changed = pyqtSignal(int)   # مدة الملف
    aya_changed = pyqtSignal(int, int)   # تغيير السورة والآية
    error_occurred = pyqtSignal(str)     # خطأ

    def __init__(self):
        super().__init__()

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
        self.downloader = AudioDownloader()
        self.downloader.download_finished.connect(self.on_download_finished)
        self.downloader.download_error.connect(self.on_download_error)

        # الحالة
        self.current_reciter = DEFAULT_RECITER
        self.current_sura = 1
        self.current_aya = 1
        self.is_loading = False
        self.auto_play_next = AUDIO_SETTINGS['auto_play_next']
        self.repeat_aya = AUDIO_SETTINGS['repeat_aya']

        # قائمة الانتظار
        self.pending_play = None

    def set_reciter(self, reciter_id: str):
        """تعيين القارئ"""
        if reciter_id in RECITERS:
            self.current_reciter = reciter_id
            print(f"🎙️ القارئ: {RECITERS[reciter_id]['name']}")

    def play_aya(self, sura: int, aya: int):
        """تشغيل آية"""
        print(f"▶️  تشغيل: {sura}:{aya}")

        self.current_sura = sura
        self.current_aya = aya
        self.aya_changed.emit(sura, aya)

        # التحقق من الكاش
        if self.downloader.is_cached(self.current_reciter, sura, aya):
            local_path = self.downloader.get_local_path(self.current_reciter, sura, aya)
            self._play_file(str(local_path))

            # تحميل مسبق
            if AUDIO_SETTINGS['download_ahead'] > 0:
                self.downloader.preload_next_ayas(
                    self.current_reciter,
                    sura,
                    aya,
                    AUDIO_SETTINGS['download_ahead']
                )
        else:
            # تحميل الملف
            self.is_loading = True
            self.state_changed.emit("loading")
            self.pending_play = (sura, aya)
            self.downloader.download_audio(self.current_reciter, sura, aya)

    def _play_file(self, file_path: str):
        """تشغيل ملف"""
        file_url = QUrl.fromLocalFile(file_path)
        self.player.setSource(file_url)
        self.player.play()
        print(f"🎵 تشغيل الملف: {file_path}")

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
        print(f"❌ خطأ في التشغيل: {error_msg}")
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
        print(f"🔄 الحالة: {state_name}")

    def on_media_status_changed(self, status):
        """عند تغيير حالة الوسائط"""
        # عند انتهاء التشغيل
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.repeat_aya:
                # إعادة تشغيل نفس الآية
                self.play_aya(self.current_sura, self.current_aya)
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
        from db_manager import QuranDatabase

        try:
            db = QuranDatabase()
            sura_info = db.get_sura_info(self.current_sura)

            next_aya = self.current_aya + 1
            next_sura = self.current_sura

            # إذا تجاوزنا آخر آية في السورة
            if next_aya > sura_info['ayas_count']:
                if self.current_sura < 114:
                    next_sura = self.current_sura + 1
                    next_aya = 1
                else:
                    # نهاية القرآن
                    print("📖 انتهى القرآن الكريم")
                    db.close()
                    return

            self.play_aya(next_sura, next_aya)
            db.close()

        except Exception as e:
            print(f"❌ خطأ في الانتقال للآية التالية: {e}")

    def play_previous(self):
        """تشغيل الآية السابقة"""
        from db_manager import QuranDatabase

        try:
            db = QuranDatabase()

            prev_aya = self.current_aya - 1
            prev_sura = self.current_sura

            # إذا كنا في أول آية من السورة
            if prev_aya < 1:
                if self.current_sura > 1:
                    prev_sura = self.current_sura - 1
                    sura_info = db.get_sura_info(prev_sura)
                    prev_aya = sura_info['ayas_count']
                else:
                    # بداية القرآن
                    print("📖 بداية القرآن الكريم")
                    db.close()
                    return

            self.play_aya(prev_sura, prev_aya)
            db.close()

        except Exception as e:
            print(f"❌ خطأ في الانتقال للآية السابقة: {e}")

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


# ═══════════════════════════════════════════════════════════════
# نهاية الملف
# ═══════════════════════════════════════════════════════════════
