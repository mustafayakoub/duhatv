#!/usr/bin/env python3
"""
🚀 نقطة التشغيل الرئيسية لنظام البحث الذكي - دُحى TV
========================================================
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# إضافة المسارات
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from windows.smart_search_window import SmartSearchWindow


def setup_application():
    """إعداد التطبيق الأساسي"""
    app = QApplication(sys.argv)

    # تعيين اتجاه التطبيق إلى RTL
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # تعيين الخطوط الافتراضية
    app.setFont(QFont("Arial", 10))

    # تعيين اسم التطبيق
    app.setApplicationName("دُحى TV - البحث الذكي")
    app.setOrganizationName("DuhaTV")
    app.setOrganizationDomain("duhatv.com")

    return app


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🌟 دُحى TV - نظام البحث الذكي")
    print("=" * 60)

    # إنشاء التطبيق
    app = setup_application()

    try:
        # إنشاء النافذة الرئيسية
        print("📱 جارٍ تشغيل النافذة الرئيسية...")
        window = SmartSearchWindow()

        # عرض النافذة
        window.show()

        print("✅ تم التشغيل بنجاح!")
        print("=" * 60)

        # تشغيل حلقة الأحداث
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
