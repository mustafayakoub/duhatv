#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق ويب بسيط لعرض بيانات القرآن الكريم
من ثلاث قواعد بيانات SQLite
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # لدعم العربية في JSON

# مسارات قواعد البيانات
DB1_PATH = r"C:\quran11\quran_ultimate_final.db"
DB2_PATH = r"C:\quran11\surah_database_app_v32.db"
DB3_PATH = r"C:\quran11\Quran_Crystalline.db"


def get_db_connection(db_path):
    """إنشاء اتصال بقاعدة البيانات"""
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # للحصول على النتائج كـ dict
    return conn


def check_databases():
    """التحقق من وجود قواعد البيانات"""
    dbs = {
        'db1': os.path.exists(DB1_PATH),
        'db2': os.path.exists(DB2_PATH),
        'db3': os.path.exists(DB3_PATH)
    }
    return dbs


@app.route('/')
def index():
    """الصفحة الرئيسية - عرض قائمة السور"""
    dbs_status = check_databases()

    # محاولة الحصول على قائمة السور من القاعدة الثالثة
    surahs = []
    if dbs_status['db3']:
        try:
            conn = get_db_connection(DB3_PATH)
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT surah_id, name_ar, name_en, revelation_type
                    FROM Surahs
                    ORDER BY surah_id
                """)
                surahs = [dict(row) for row in cursor.fetchall()]
                conn.close()
        except Exception as e:
            print(f"خطأ في قراءة السور: {e}")

    return render_template('index.html',
                         surahs=surahs,
                         dbs_status=dbs_status)


@app.route('/surah/<int:surah_id>')
def surah(surah_id):
    """عرض سورة معينة مع الآيات"""

    # معلومات السورة من DB3
    surah_info = None
    ayahs = []

    conn3 = get_db_connection(DB3_PATH)
    if conn3:
        try:
            # معلومات السورة
            cursor = conn3.cursor()
            cursor.execute("""
                SELECT DISTINCT surah_id, name_ar, name_en, revelation_type, ayah_count
                FROM Surahs
                WHERE surah_id = ?
            """, (surah_id,))
            row = cursor.fetchone()
            if row:
                surah_info = dict(row)

            # الآيات
            cursor.execute("""
                SELECT DISTINCT ayah_number, text
                FROM QuranContent
                WHERE surah_id = ?
                ORDER BY ayah_number
            """, (surah_id,))
            ayahs = [dict(row) for row in cursor.fetchall()]

            conn3.close()
        except Exception as e:
            print(f"خطأ في قراءة السورة: {e}")

    # الترجمات من DB1
    translations = []
    conn1 = get_db_connection(DB1_PATH)
    if conn1:
        try:
            cursor = conn1.cursor()
            cursor.execute("""
                SELECT verse_number, text, language_name
                FROM quran_translations
                WHERE surah_number = ?
                ORDER BY verse_number, language_name
                LIMIT 50
            """, (surah_id,))
            translations = [dict(row) for row in cursor.fetchall()]
            conn1.close()
        except Exception as e:
            print(f"خطأ في قراءة الترجمات: {e}")

    # الإعراب والصرف من DB2
    irab_data = []
    conn2 = get_db_connection(DB2_PATH)
    if conn2:
        try:
            cursor = conn2.cursor()
            cursor.execute("""
                SELECT ayah_number, word_text, irab, sarf
                FROM ayah_words
                WHERE surah_number = ?
                ORDER BY ayah_number, word_position
                LIMIT 100
            """, (surah_id,))
            irab_data = [dict(row) for row in cursor.fetchall()]
            conn2.close()
        except Exception as e:
            print(f"خطأ في قراءة الإعراب: {e}")

    return render_template('surah.html',
                         surah_info=surah_info,
                         ayahs=ayahs,
                         translations=translations,
                         irab_data=irab_data)


@app.route('/api/search')
def search():
    """البحث في النص القرآني"""
    query = request.args.get('q', '')

    if len(query) < 2:
        return jsonify({'error': 'استعلام قصير جداً'}), 400

    results = []
    conn3 = get_db_connection(DB3_PATH)
    if conn3:
        try:
            cursor = conn3.cursor()
            cursor.execute("""
                SELECT
                    qc.surah_id,
                    s.name_ar as surah_name,
                    qc.ayah_number,
                    qc.text
                FROM QuranContent qc
                JOIN Surahs s ON qc.surah_id = s.surah_id
                WHERE qc.text LIKE ?
                ORDER BY qc.surah_id, qc.ayah_number
                LIMIT 50
            """, (f'%{query}%',))
            results = [dict(row) for row in cursor.fetchall()]
            conn3.close()
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'results': results, 'count': len(results)})


@app.route('/api/stats')
def stats():
    """إحصائيات عن قواعد البيانات"""
    statistics = {
        'db1': {},
        'db2': {},
        'db3': {}
    }

    # DB1 Stats
    conn1 = get_db_connection(DB1_PATH)
    if conn1:
        try:
            cursor = conn1.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM quran_translations")
            statistics['db1']['translations_count'] = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(DISTINCT language_name) as count FROM quran_translations")
            statistics['db1']['languages_count'] = cursor.fetchone()['count']
            conn1.close()
        except:
            pass

    # DB2 Stats
    conn2 = get_db_connection(DB2_PATH)
    if conn2:
        try:
            cursor = conn2.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM ayah_words")
            statistics['db2']['words_count'] = cursor.fetchone()['count']
            conn2.close()
        except:
            pass

    # DB3 Stats
    conn3 = get_db_connection(DB3_PATH)
    if conn3:
        try:
            cursor = conn3.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM QuranContent")
            statistics['db3']['content_count'] = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(DISTINCT source_id) as count FROM QuranContent")
            statistics['db3']['sources_count'] = cursor.fetchone()['count']
            conn3.close()
        except:
            pass

    return jsonify(statistics)


if __name__ == '__main__':
    print("=" * 70)
    print("🌙 تطبيق القرآن الكريم - Quran Simple Web App")
    print("=" * 70)
    print()

    # التحقق من قواعد البيانات
    dbs = check_databases()
    print("📊 حالة قواعد البيانات:")
    print(f"  DB1 (Translations): {'✅ موجود' if dbs['db1'] else '❌ غير موجود'}")
    print(f"  DB2 (I'rab/Sarf):   {'✅ موجود' if dbs['db2'] else '❌ غير موجود'}")
    print(f"  DB3 (Content):      {'✅ موجود' if dbs['db3'] else '❌ غير موجود'}")
    print()

    if not any(dbs.values()):
        print("⚠️  تحذير: لا توجد قواعد بيانات!")
        print(f"📁 ضع قواعد البيانات في: C:\\quran11\\")
        print()

    print("🚀 التطبيق يعمل الآن على:")
    print("   http://localhost:5000")
    print()
    print("🔗 الروابط المتاحة:")
    print("   📖 الصفحة الرئيسية: http://localhost:5000/")
    print("   🔍 البحث: http://localhost:5000/api/search?q=الله")
    print("   📊 الإحصائيات: http://localhost:5000/api/stats")
    print()
    print("=" * 70)
    print()

    # تشغيل التطبيق
    app.run(debug=True, host='0.0.0.0', port=5000)
