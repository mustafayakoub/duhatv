#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إنشاء قاعدة بيانات تجريبية للاختبار
Create Test Database for Application Testing
"""

import sqlite3
import os

# مسار قاعدة البيانات
DB_PATH = "quran_ultimate.db"

def create_database():
    """إنشاء قاعدة البيانات وجداولها"""

    # حذف قاعدة البيانات القديمة إن وجدت
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✅ تم حذف قاعدة البيانات القديمة: {DB_PATH}")

    # الاتصال وإنشاء قاعدة بيانات جديدة
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("📦 إنشاء الجداول...")

    # تنفيذ سكريبت SQL
    with open('create_quran_database_final.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
        cursor.executescript(sql_script)

    conn.commit()
    print("✅ تم إنشاء جميع الجداول بنجاح")

    return conn, cursor


def add_sample_data(conn, cursor):
    """إضافة بيانات عينة للاختبار - سورة الفاتحة"""

    print("\n📝 إضافة بيانات عينة - سورة الفاتحة...")

    # بيانات سورة الفاتحة (7 آيات)
    fatiha_verses = [
        {
            'surah_id': 1,
            'ayah_id': 1,
            'text': 'بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ',
            'text_simple': 'بسم الله الرحمن الرحيم',
            'tajweed': '<1>بِسۡمِ</1> <1>ٱللَّهِ</1> <4>ٱلرَّحۡمَٰنِ</4> <1>ٱلرَّحِيمِ</1>',
            'tafsir_muyassar': 'أبتدئ قراءة القرآن باسم الله مستعينا به، (اللهِ) علم على الرب -تبارك وتعالى- المعبود بحق دون سواه، وهو أخص أسماء الله تعالى، ولا يسمى به غيره سبحانه. (الرَّحْمَنِ) ذي الرحمة العامة الذي وسعت رحمته جميع الخلق، (الرَّحِيمِ) بالمؤمنين، وهما اسمان من أسمائه تعالى.',
            'tafsir_saadi': 'أي: أبتدئ كل أموري باسم الله تعالى، وهذا الاسم الكريم أعظم الأسماء الحسنى، والرحمن الرحيم اسمان دالان على أن الله تعالى ذو الرحمة الواسعة العظيمة التي وسعت كل شيء.',
            'translation_en': 'In the name of Allah, the Entirely Merciful, the Especially Merciful.',
            'translation_fr': 'Au nom d\'Allah, le Tout Miséricordieux, le Très Miséricordieux.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 2,
            'text': 'ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ',
            'text_simple': 'الحمد لله رب العالمين',
            'tajweed': '<1>ٱلۡحَمۡدُ</1> <1>لِلَّهِ</1> <2>رَبِّ</2> <4>ٱلۡعَٰلَمِينَ</4>',
            'tafsir_muyassar': 'الحمد لله رب العالمين: الثناء على الله بصفاته التي كلُّها أوصاف كمال، وبنعمه الظاهرة والباطنة، الدينية والدنيوية، وفي ضمنه أَمْرٌ لعباده أن يحمدوه، فهو المستحق له وحده، وهو سبحانه المنشئ للخلق، القائم بأمورهم.',
            'tafsir_saadi': 'الحمد لله: أي الثناء الكامل، والمحبة التامة، مع الخضوع لله تعالى، رب العالمين: أي المربي لجميع الخلق، الذي خلقهم ورزقهم وأنعم عليهم بالنعم الظاهرة والباطنة.',
            'translation_en': '[All] praise is [due] to Allah, Lord of the worlds.',
            'translation_fr': 'Louange à Allah, Seigneur de l\'univers.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 3,
            'text': 'ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ',
            'text_simple': 'الرحمن الرحيم',
            'tajweed': '<4>ٱلرَّحۡمَٰنِ</4> <1>ٱلرَّحِيمِ</1>',
            'tafsir_muyassar': 'الرحمن الرحيم: اسمان يدلان على أن الله تعالى ذو الرحمة الواسعة، وأنه سبحانه أرحم الراحمين.',
            'tafsir_saadi': 'الرحمن الرحيم: وقد تقدم معنى هذين الاسمين الكريمين، والرحمن أشد مبالغة من الرحيم، والرحيم بمعنى راحم عباده.',
            'translation_en': 'The Entirely Merciful, the Especially Merciful.',
            'translation_fr': 'Le Tout Miséricordieux, le Très Miséricordieux.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 4,
            'text': 'مَٰلِكِ يَوۡمِ ٱلدِّينِ',
            'text_simple': 'مالك يوم الدين',
            'tajweed': '<4>مَٰلِكِ</4> <1>يَوۡمِ</1> <2>ٱلدِّينِ</2>',
            'tafsir_muyassar': 'مالك يوم الدين: المتصرف في يوم القيامة، لا يملك أحد معه حكمًا، ولا يقضي غيره أمرًا.',
            'tafsir_saadi': 'مالك يوم الدين: أي المتصرف في يوم القيامة الذي يدين الله العباد فيه بأعمالهم، فيثيب المطيعين ويعاقب العاصين.',
            'translation_en': 'Sovereign of the Day of Recompense.',
            'translation_fr': 'Maître du Jour de la rétribution.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 5,
            'text': 'إِيَّاكَ نَعۡبُدُ وَإِيَّاكَ نَسۡتَعِينُ',
            'text_simple': 'إياك نعبد وإياك نستعين',
            'tajweed': '<1>إِيَّاكَ</1> <1>نَعۡبُدُ</1> <1>وَإِيَّاكَ</1> <4>نَسۡتَعِينُ</4>',
            'tafsir_muyassar': 'إياك نعبد: نخصك وحدك بالعبادة، وإياك نستعين: نطلب منك وحدك العون على طاعتك وفي جميع أمورنا.',
            'tafsir_saadi': 'إياك نعبد: أي نعبدك وحدك يا الله لا نشرك معك غيرك، وإياك نستعين: أي نطلب منك المعونة على عبادتك وعلى جميع أمورنا.',
            'translation_en': 'It is You we worship and You we ask for help.',
            'translation_fr': 'C\'est Toi [Seul] que nous adorons, et c\'est Toi [Seul] dont nous implorons secours.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 6,
            'text': 'ٱهۡدِنَا ٱلصِّرَٰطَ ٱلۡمُسۡتَقِيمَ',
            'text_simple': 'اهدنا الصراط المستقيم',
            'tajweed': '<2>ٱهۡدِنَا</2> <9>ٱلصِّرَٰطَ</9> <4>ٱلۡمُسۡتَقِيمَ</4>',
            'tafsir_muyassar': 'اهدنا الصراط المستقيم: دلنا وأرشدنا إلى الطريق المستقيم، وثبتنا عليه حتى نلقاك، وهو الإسلام.',
            'tafsir_saadi': 'اهدنا الصراط المستقيم: أي دلنا وأرشدنا ووفقنا للصراط المستقيم، وهو الطريق الواضح الموصل إلى الله وإلى جنته، وهو معرفة الحق والعمل به.',
            'translation_en': 'Guide us to the straight path.',
            'translation_fr': 'Guide-nous dans le droit chemin.',
            'juz': 1,
            'page': 1
        },
        {
            'surah_id': 1,
            'ayah_id': 7,
            'text': 'صِرَٰطَ ٱلَّذِينَ أَنۡعَمۡتَ عَلَيۡهِمۡ غَيۡرِ ٱلۡمَغۡضُوبِ عَلَيۡهِمۡ وَلَا ٱلضَّآلِّينَ',
            'text_simple': 'صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين',
            'tajweed': '<9>صِرَٰطَ</9> <1>ٱلَّذِينَ</1> <1>أَنۡعَمۡتَ</1> <1>عَلَيۡهِمۡ</1> <7>غَيۡرِ</7> <12>ٱلۡمَغۡضُوبِ</12> <1>عَلَيۡهِمۡ</1> <1>وَلَا</1> <10>ٱلضَّآلِّينَ</10>',
            'tafsir_muyassar': 'صراط الذين أنعمت عليهم: طريق الذين أنعمت عليهم من النبيين والصديقين والشهداء والصالحين، غير المغضوب عليهم: غير طريق اليهود الذين غضب الله عليهم، ولا الضالين: ولا طريق النصارى الذين ضلوا عن الحق.',
            'tafsir_saadi': 'صراط الذين أنعمت عليهم: وهم أهل الهداية والاستقامة والطاعة لله ورسوله، غير المغضوب عليهم: وهم اليهود الذين علموا الحق وخالفوه، ولا الضالين: وهم النصارى الذين جهلوا الحق فضلوا عنه.',
            'translation_en': 'The path of those upon whom You have bestowed favor, not of those who have evoked [Your] anger or of those who are astray.',
            'translation_fr': 'le chemin de ceux que Tu as comblés de faveurs, non pas de ceux qui ont encouru Ta colère, ni des égarés.',
            'juz': 1,
            'page': 1
        }
    ]

    # إضافة الآيات إلى الجداول
    for verse in fatiha_verses:
        # جدول quran_text
        cursor.execute("""
            INSERT INTO quran_text (surah_id, ayah_id, text, text_simple, juz, page)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['text'],
              verse['text_simple'], verse['juz'], verse['page']))

        # جدول quran_tajweed
        cursor.execute("""
            INSERT INTO quran_tajweed (surah_id, ayah_id, tajweed_text)
            VALUES (?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['tajweed']))

        # جدول tafsir_muyassar
        cursor.execute("""
            INSERT INTO tafsir_muyassar (surah_id, ayah_id, text)
            VALUES (?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['tafsir_muyassar']))

        # جدول tafsir_saadi
        cursor.execute("""
            INSERT INTO tafsir_saadi (surah_id, ayah_id, text)
            VALUES (?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['tafsir_saadi']))

        # جدول translation_english
        cursor.execute("""
            INSERT INTO translation_english (surah_id, ayah_id, text)
            VALUES (?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['translation_en']))

        # جدول translation_french
        cursor.execute("""
            INSERT INTO translation_french (surah_id, ayah_id, text)
            VALUES (?, ?, ?)
        """, (verse['surah_id'], verse['ayah_id'], verse['translation_fr']))

    # إضافة بعض المواضيع كعينة
    topics_data = [
        ('التوحيد', 'آيات عن توحيد الله تعالى', 'العقيدة'),
        ('العبادة', 'آيات عن العبادة والطاعة', 'العبادات'),
        ('الهداية', 'آيات عن طلب الهداية', 'الدعاء')
    ]

    for topic in topics_data:
        cursor.execute("""
            INSERT INTO topics (name, description, category)
            VALUES (?, ?, ?)
        """, topic)

    # ربط بعض الآيات بالمواضيع
    topic_verses = [
        (1, 1, 1),  # التوحيد - الفاتحة:1
        (2, 1, 5),  # العبادة - الفاتحة:5
        (3, 1, 6),  # الهداية - الفاتحة:6
        (3, 1, 7),  # الهداية - الفاتحة:7
    ]

    for topic_id, surah_id, ayah_id in topic_verses:
        cursor.execute("""
            INSERT INTO topics_verses (topic_id, surah_id, ayah_id)
            VALUES (?, ?, ?)
        """, (topic_id, surah_id, ayah_id))

    conn.commit()
    print("✅ تم إضافة 7 آيات من سورة الفاتحة")
    print("✅ تم إضافة 3 مواضيع مع ربطها بالآيات")


def verify_data(cursor):
    """التحقق من البيانات المُدخلة"""

    print("\n🔍 التحقق من البيانات...")

    # عدد السور
    cursor.execute("SELECT COUNT(*) FROM surahs_info")
    surahs_count = cursor.fetchone()[0]
    print(f"   📚 عدد السور: {surahs_count}")

    # عدد الآيات
    cursor.execute("SELECT COUNT(*) FROM quran_text")
    verses_count = cursor.fetchone()[0]
    print(f"   📖 عدد الآيات: {verses_count}")

    # عدد آيات التجويد
    cursor.execute("SELECT COUNT(*) FROM quran_tajweed")
    tajweed_count = cursor.fetchone()[0]
    print(f"   🎨 آيات التجويد: {tajweed_count}")

    # عدد التفاسير
    cursor.execute("SELECT COUNT(*) FROM tafsir_muyassar")
    tafsir_count = cursor.fetchone()[0]
    print(f"   📚 التفسير الميسر: {tafsir_count}")

    # عدد الترجمات
    cursor.execute("SELECT COUNT(*) FROM translation_english")
    trans_count = cursor.fetchone()[0]
    print(f"   🌍 الترجمة الإنجليزية: {trans_count}")

    # عدد المواضيع
    cursor.execute("SELECT COUNT(*) FROM topics")
    topics_count = cursor.fetchone()[0]
    print(f"   🏷️  عدد المواضيع: {topics_count}")

    # عدد آيات السجدة
    cursor.execute("SELECT COUNT(*) FROM sajda_ayahs")
    sajda_count = cursor.fetchone()[0]
    print(f"   🕌 آيات السجدة: {sajda_count}")

    # اختبار استعلام معقد
    print("\n📊 اختبار استعلام get_verse للآية الأولى:")
    cursor.execute("""
        SELECT
            qt.surah_id, qt.ayah_id, qt.text, qt.text_simple,
            qtj.tajweed_text,
            tm.text as tafsir_muyassar,
            ts.text as tafsir_saadi,
            te.text as translation_english
        FROM quran_text qt
        LEFT JOIN quran_tajweed qtj ON qt.surah_id = qtj.surah_id AND qt.ayah_id = qtj.ayah_id
        LEFT JOIN tafsir_muyassar tm ON qt.surah_id = tm.surah_id AND qt.ayah_id = tm.ayah_id
        LEFT JOIN tafsir_saadi ts ON qt.surah_id = ts.surah_id AND qt.ayah_id = ts.ayah_id
        LEFT JOIN translation_english te ON qt.surah_id = te.surah_id AND qt.ayah_id = te.ayah_id
        WHERE qt.surah_id = 1 AND qt.ayah_id = 1
    """)

    verse = cursor.fetchone()
    if verse:
        print(f"   ✅ النص: {verse[2][:50]}...")
        print(f"   ✅ التجويد: {verse[4][:50]}...")
        print(f"   ✅ التفسير: {verse[5][:50]}...")
        print(f"   ✅ الترجمة: {verse[7][:50]}...")
    else:
        print("   ❌ لم يتم العثور على البيانات!")


def main():
    """الدالة الرئيسية"""

    print("=" * 70)
    print("🚀 إنشاء قاعدة بيانات تجريبية - تطبيق القرآن الكريم")
    print("=" * 70)

    try:
        # إنشاء قاعدة البيانات
        conn, cursor = create_database()

        # إضافة بيانات العينة
        add_sample_data(conn, cursor)

        # التحقق من البيانات
        verify_data(cursor)

        # إغلاق الاتصال
        conn.close()

        print("\n" + "=" * 70)
        print("✅ تم إنشاء قاعدة البيانات التجريبية بنجاح!")
        print(f"📍 المسار: {os.path.abspath(DB_PATH)}")
        print("🎯 جاهز للاختبار: python quran_app_ultimate_final_v4.py")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
