#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإنشاء قاعدة بيانات تجريبية للقرآن الكريم
Demo Quran Database Creator
"""

import sqlite3
import sys

def create_demo_database(db_path='quran.db'):
    """إنشاء قاعدة بيانات تجريبية"""

    print("🔨 جاري إنشاء قاعدة بيانات تجريبية...")

    # الاتصال بقاعدة البيانات (تُنشأ إذا لم تكن موجودة)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # إنشاء جدول النص القرآني
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quran_text_with_tajweed (
            surahNo INTEGER,
            ayahNo INTEGER,
            tajweedText TEXT,
            PRIMARY KEY (surahNo, ayahNo)
        )
    ''')

    # إنشاء جدول التفسير الميسر
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tafsir_moyassar (
            surahNo INTEGER,
            ayahNo INTEGER,
            text TEXT,
            PRIMARY KEY (surahNo, ayahNo)
        )
    ''')

    # إنشاء جدول تفسير السعدي
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tafsir_saadi (
            surahNo INTEGER,
            ayahNo INTEGER,
            text TEXT,
            PRIMARY KEY (surahNo, ayahNo)
        )
    ''')

    # بيانات تجريبية - سورة الفاتحة
    demo_verses = [
        (1, 1, 'بِسْمِ <1>ٱ</1><2>ل</2>لَّهِ <1>ٱ</1>لرَّحْمَٰنِ <1>ٱ</1>لرَّحِيمِ'),
        (1, 2, '<1>ٱ</1>لْحَمْدُ لِلَّهِ رَبِّ <1>ٱ</1>لْعَٰلَمِينَ'),
        (1, 3, '<1>ٱ</1>لرَّحْمَٰنِ <1>ٱ</1>لرَّحِيمِ'),
        (1, 4, 'مَٰلِكِ يَوْمِ <1>ٱ</1>لدِّينِ'),
        (1, 5, 'إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ'),
        (1, 6, 'ٱهْدِنَا <1>ٱ</1>لصِّرَٰطَ <1>ٱ</1>لْمُسْتَقِيمَ'),
        (1, 7, 'صِرَٰطَ <1>ٱ</1>لَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ <1>ٱ</1>لْمَغْضُوبِ عَلَيْهِمْ وَلَا <1>ٱ</1>لضَّآلِّينَ'),
    ]

    print("📝 إضافة سورة الفاتحة...")
    for surah, ayah, text in demo_verses:
        cursor.execute('''
            INSERT OR REPLACE INTO quran_text_with_tajweed (surahNo, ayahNo, tajweedText)
            VALUES (?, ?, ?)
        ''', (surah, ayah, text))

    # إضافة تفسير تجريبي
    demo_tafsir = [
        (1, 1, 'أبتدئ قراءتي باسم الله، مستعينًا به، وهو الرحمن الذي وسعت رحمته جميع الخلق، الرحيم بالمؤمنين.'),
        (1, 2, 'الثناء على الله بصفاته التي كلُّها أوصاف كمال، وبنعمه الظاهرة والباطنة، فهو المستحق لها.'),
        (1, 3, 'الرحمن: ذو الرحمة الواسعة. الرحيم: بالمؤمنين، وهما اسمان من أسماء الله تعالى.'),
        (1, 4, 'وهو وحده مالك يوم القيامة، وهو يوم الجزاء على الأعمال.'),
        (1, 5, 'إياك نعبد وحدك يا ربنا لا نشرك بك شيئًا، وإياك وحدك نستعين في جميع أمورنا.'),
        (1, 6, 'دُلَّنا، وأرشدنا، ووفقنا إلى الطريق المستقيم، وثبتنا عليه حتى نلقاك، وهو الإسلام.'),
        (1, 7, 'طريق الذين أنعمت عليهم من النبيين والصدِّيقين والشهداء والصالحين، غير طريق المغضوب عليهم (اليهود) ولا طريق الضالين (النصارى).'),
    ]

    print("📚 إضافة التفسير الميسر...")
    for surah, ayah, text in demo_tafsir:
        cursor.execute('''
            INSERT OR REPLACE INTO tafsir_moyassar (surahNo, ayahNo, text)
            VALUES (?, ?, ?)
        ''', (surah, ayah, text))

    # إضافة بعض الآيات من سورة البقرة للتجربة
    demo_baqarah = [
        (2, 1, '<4>ٱ</4>لٓمٓ'),
        (2, 2, 'ذَٰلِكَ <1>ٱ</1>لْكِتَٰبُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِّلْمُتَّقِينَ'),
        (2, 3, '<1>ٱ</1>لَّذِينَ يُؤْمِنُونَ بِ<1>ٱ</1>لْغَيْبِ وَيُقِيمُونَ <1>ٱ</1>لصَّلَوٰةَ وَمِمَّا رَزَقْنَٰهُمْ يُنفِقُونَ'),
    ]

    print("📝 إضافة بعض آيات سورة البقرة...")
    for surah, ayah, text in demo_baqarah:
        cursor.execute('''
            INSERT OR REPLACE INTO quran_text_with_tajweed (surahNo, ayahNo, tajweedText)
            VALUES (?, ?, ?)
        ''', (surah, ayah, text))

    # حفظ التغييرات
    conn.commit()

    # عرض الإحصائيات
    cursor.execute('SELECT COUNT(*) FROM quran_text_with_tajweed')
    verse_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(DISTINCT surahNo) FROM quran_text_with_tajweed')
    surah_count = cursor.fetchone()[0]

    conn.close()

    print("\n" + "="*60)
    print("✅ تم إنشاء قاعدة البيانات بنجاح!")
    print("="*60)
    print(f"📊 الإحصائيات:")
    print(f"   • عدد السور: {surah_count}")
    print(f"   • عدد الآيات: {verse_count}")
    print(f"   • اسم الملف: {db_path}")
    print("="*60)
    print("\n⚠️  ملاحظة: هذه قاعدة بيانات تجريبية تحتوي فقط على:")
    print("   - سورة الفاتحة كاملة (7 آيات)")
    print("   - 3 آيات من سورة البقرة")
    print("   - تفسير الفاتحة (التفسير الميسر)")
    print("\n💡 للحصول على قاعدة بيانات كاملة:")
    print("   - قم بتحميلها من المصادر الموثوقة")
    print("   - راجع ملف FIX_INSTRUCTIONS.txt للروابط")
    print("\nالآن يمكنك تشغيل التطبيق:")
    print("   python quran_app_v3_ultimate.py")
    print("="*60)

if __name__ == '__main__':
    try:
        create_demo_database()
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        sys.exit(1)
