#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
🎵 عناصر التحكم الصوتي - تطبيق القرآن الكريم Pro
═══════════════════════════════════════════════════════════════
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from config import *


class AudioControlWidget(QWidget):
    """لوحة التحكم الصوتي"""

    # إشارات مخصصة
    play_requested = pyqtSignal(int, int)      # طلب تشغيل (سورة، آية)
    pause_requested = pyqtSignal()              # طلب إيقاف مؤقت
    stop_requested = pyqtSignal()               # طلب إيقاف
    next_requested = pyqtSignal()               # طلب التالي
    previous_requested = pyqtSignal()           # طلب السابق
    volume_changed = pyqtSignal(float)          # تغيير الصوت
    reciter_change_requested = pyqtSignal()     # طلب تغيير القارئ

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

        # ═══════════════════════════════════════════════════════════
        # السطر الأول: اختيار القارئ والحالة
        # ═══════════════════════════════════════════════════════════
        top_layout = QHBoxLayout()

        # أيقونة القارئ
        icon_label = QLabel("🎙️")
        icon_label.setStyleSheet("font-size: 20px;")
        top_layout.addWidget(icon_label)

        # اسم القارئ
        self.reciter_label = QLabel("عبد الباسط عبد الصمد")
        self.reciter_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {COLORS['primary']};
            }}
        """)
        top_layout.addWidget(self.reciter_label)

        # زر تغيير القارئ
        self.change_reciter_btn = QPushButton("تغيير ▼")
        self.change_reciter_btn.setMaximumWidth(80)
        self.change_reciter_btn.clicked.connect(self.reciter_change_requested.emit)
        top_layout.addWidget(self.change_reciter_btn)

        top_layout.addStretch()

        # حالة التشغيل
        self.status_label = QLabel("جاهز")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 12px;
            }}
        """)
        top_layout.addWidget(self.status_label)

        main_layout.addLayout(top_layout)

        # ═══════════════════════════════════════════════════════════
        # السطر الثاني: أزرار التحكم
        # ═══════════════════════════════════════════════════════════
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # زر السابق
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setMaximumWidth(50)
        self.prev_btn.setToolTip("الآية السابقة (Ctrl+Left)")
        self.prev_btn.clicked.connect(self.previous_requested.emit)
        controls_layout.addWidget(self.prev_btn)

        # زر تشغيل/إيقاف
        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.setMaximumWidth(60)
        self.play_pause_btn.setToolTip("تشغيل/إيقاف (Space)")
        self.play_pause_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 20px;
                background-color: {COLORS['success']};
                color: white;
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #229954;
            }}
        """)
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        controls_layout.addWidget(self.play_pause_btn)

        # زر التالي
        self.next_btn = QPushButton("⏭")
        self.next_btn.setMaximumWidth(50)
        self.next_btn.setToolTip("الآية التالية (Ctrl+Right)")
        self.next_btn.clicked.connect(self.next_requested.emit)
        controls_layout.addWidget(self.next_btn)

        # زر إيقاف
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setMaximumWidth(50)
        self.stop_btn.setToolTip("إيقاف (Ctrl+S)")
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        controls_layout.addWidget(self.stop_btn)

        controls_layout.addStretch()

        # التشغيل التلقائي
        self.auto_play_checkbox = QCheckBox("تشغيل تلقائي")
        self.auto_play_checkbox.setChecked(AUDIO_SETTINGS['auto_play_next'])
        self.auto_play_checkbox.setToolTip("تشغيل الآية التالية تلقائياً")
        controls_layout.addWidget(self.auto_play_checkbox)

        # التكرار
        self.repeat_checkbox = QCheckBox("تكرار")
        self.repeat_checkbox.setChecked(AUDIO_SETTINGS['repeat_aya'])
        self.repeat_checkbox.setToolTip("تكرار الآية الحالية")
        controls_layout.addWidget(self.repeat_checkbox)

        main_layout.addLayout(controls_layout)

        # ═══════════════════════════════════════════════════════════
        # السطر الثالث: شريط التقدم والوقت
        # ═══════════════════════════════════════════════════════════
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(8)

        # الوقت الحالي
        self.current_time_label = QLabel("0:00")
        self.current_time_label.setMinimumWidth(40)
        self.current_time_label.setStyleSheet("font-size: 11px;")
        progress_layout.addWidget(self.current_time_label)

        # شريط التقدم
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)
        self.progress_slider.setValue(0)
        self.progress_slider.setToolTip("اسحب للتقديم/التأخير")
        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        self.progress_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 6px;
                background: {COLORS['bg_light']};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['primary']};
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['primary']};
                border-radius: 3px;
            }}
        """)
        progress_layout.addWidget(self.progress_slider, 1)

        # المدة الكلية
        self.duration_label = QLabel("0:00")
        self.duration_label.setMinimumWidth(40)
        self.duration_label.setStyleSheet("font-size: 11px;")
        progress_layout.addWidget(self.duration_label)

        main_layout.addLayout(progress_layout)

        # ═══════════════════════════════════════════════════════════
        # السطر الرابع: مستوى الصوت
        # ═══════════════════════════════════════════════════════════
        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(8)

        # أيقونة الصوت
        volume_icon = QLabel("🔊")
        volume_icon.setStyleSheet("font-size: 16px;")
        volume_layout.addWidget(volume_icon)

        # شريط الصوت
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        self.volume_slider.setMaximumWidth(150)
        self.volume_slider.setToolTip("مستوى الصوت")
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.volume_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: {COLORS['bg_light']};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['success']};
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['success']};
                border-radius: 2px;
            }}
        """)
        volume_layout.addWidget(self.volume_slider)

        # نسبة الصوت
        self.volume_label = QLabel("80%")
        self.volume_label.setMinimumWidth(35)
        self.volume_label.setStyleSheet("font-size: 11px;")
        volume_layout.addWidget(self.volume_label)

        volume_layout.addStretch()

        main_layout.addLayout(volume_layout)

        # تطبيق الستايل العام
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_light']};
                border: 2px solid {COLORS['primary']};
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
            }}
            QPushButton:pressed {{
                background-color: #1e4378;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['text_light']};
            }}
        """)

    # ═══════════════════════════════════════════════════════════════
    # معالجات الأحداث
    # ═══════════════════════════════════════════════════════════════

    def on_play_pause_clicked(self):
        """عند النقر على زر التشغيل/الإيقاف"""
        if self.is_playing:
            self.pause_requested.emit()
        else:
            # طلب تشغيل الآية الحالية (0, 0 = الآية المعروضة حالياً)
            self.play_requested.emit(0, 0)

    def on_stop_clicked(self):
        """عند النقر على زر الإيقاف"""
        self.stop_requested.emit()
        self.set_playing_state(False)
        self.set_position(0)

    def on_slider_moved(self, position):
        """عند تحريك شريط التقدم"""
        # سيتم إرسال الموضع للمشغل
        pass

    def on_volume_changed(self, value):
        """عند تغيير مستوى الصوت"""
        self.volume_label.setText(f"{value}%")
        self.volume_changed.emit(value / 100.0)

    # ═══════════════════════════════════════════════════════════════
    # دوال التحديث
    # ═══════════════════════════════════════════════════════════════

    def set_reciter_name(self, name: str):
        """تعيين اسم القارئ"""
        self.reciter_label.setText(name)

    def set_playing_state(self, is_playing: bool):
        """تعيين حالة التشغيل"""
        self.is_playing = is_playing
        if is_playing:
            self.play_pause_btn.setText("⏸")
            self.play_pause_btn.setToolTip("إيقاف مؤقت (Space)")
            self.status_label.setText("جارٍ التشغيل...")
            self.status_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 12px;")
        else:
            self.play_pause_btn.setText("▶")
            self.play_pause_btn.setToolTip("تشغيل (Space)")
            self.status_label.setText("متوقف")
            self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")

    def set_status(self, status: str, color: str = None):
        """تعيين نص الحالة"""
        self.status_label.setText(status)
        if color:
            self.status_label.setStyleSheet(f"color: {color}; font-size: 12px;")

    def set_position(self, position_ms: int):
        """تعيين موضع التشغيل (بالميلي ثانية)"""
        self.current_position = position_ms

        # تحديث النص
        minutes = position_ms // 60000
        seconds = (position_ms % 60000) // 1000
        self.current_time_label.setText(f"{minutes}:{seconds:02d}")

        # تحديث الشريط
        if self.duration > 0:
            progress = int((position_ms / self.duration) * 1000)
            self.progress_slider.setValue(progress)

    def set_duration(self, duration_ms: int):
        """تعيين المدة الكلية (بالميلي ثانية)"""
        self.duration = duration_ms

        # تحديث النص
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        self.duration_label.setText(f"{minutes}:{seconds:02d}")

    def set_enabled(self, enabled: bool):
        """تفعيل/تعطيل الأزرار"""
        self.play_pause_btn.setEnabled(enabled)
        self.prev_btn.setEnabled(enabled)
        self.next_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(enabled)

    def get_auto_play_next(self) -> bool:
        """الحصول على حالة التشغيل التلقائي"""
        return self.auto_play_checkbox.isChecked()

    def get_repeat_aya(self) -> bool:
        """الحصول على حالة التكرار"""
        return self.repeat_checkbox.isChecked()


# ═══════════════════════════════════════════════════════════════
# نهاية الملف
# ═══════════════════════════════════════════════════════════════
