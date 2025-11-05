#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Backend - Quran Clean Application
تطبيق القرآن الكريم النظيف والأنيق
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
from pathlib import Path
import json

# ═══════════════════════════════════════════════════════════════
# إعدادات التطبيق
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # دعم العربية في JSON

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "quran.db"

# ═══════════════════════════════════════════════════════════════
# دوال قاعدة البيانات
# ═══════════════════════════════════════════════════════════════

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # للحصول على النتائج كقواميس
    return conn


def dict_from_row(row):
    """تحويل صف قاعدة البيانات إلى قاموس"""
    return dict(zip(row.keys(), row))


# ═══════════════════════════════════════════════════════════════
# الصفحة الرئيسية
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')


# ═══════════════════════════════════════════════════════════════
# API: السور
# ═══════════════════════════════════════════════════════════════

@app.route('/api/surahs')
def get_surahs():
    """الحصول على قائمة السور"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name_ar, name_en, ayah_count, revelation_place,
                   page_start, category
            FROM surahs
            ORDER BY id
        """)

        surahs = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(surahs)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/surah/<int:surah_id>')
def get_surah(surah_id):
    """الحصول على تفاصيل سورة محددة"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM surahs WHERE id = ?
        """, (surah_id,))

        surah = cursor.fetchone()
        conn.close()

        if surah:
            return jsonify(dict_from_row(surah))
        else:
            return jsonify({'error': 'السورة غير موجودة'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# API: الآيات
# ═══════════════════════════════════════════════════════════════

@app.route('/api/ayahs')
def get_ayahs():
    """الحصول على آيات سورة معينة"""
    surah_id = request.args.get('surah_id', type=int)
    text_type = request.args.get('text_type', 'text_uthmani')

    if not surah_id:
        return jsonify({'error': 'surah_id مطلوب'}), 400

    # التحقق من صحة text_type
    valid_types = [
        'text_awwal', 'text_uthmani', 'text_uthmani_min',
        'text_hafs', 'text_warsh', 'text_qaloun', 'text_douri',
        'text_shuba', 'text_sousi', 'text_amiry',
        'text_imlaei', 'text_imlaei_mini', 'text_imlaei_plain',
        'text_simple_fasel', 'text_simple_tam',
        'text_ajami', 'text_latin', 'text_tajweed'
    ]

    if text_type not in valid_types:
        text_type = 'text_uthmani'

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT
                id, surah_id, ayah_id, page, juz,
                {text_type} as text
            FROM ayahs
            WHERE surah_id = ?
            ORDER BY ayah_id
        """

        cursor.execute(query, (surah_id,))
        ayahs = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(ayahs)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ayah/<int:surah_id>/<int:ayah_id>')
def get_ayah(surah_id, ayah_id):
    """الحصول على آية محددة مع جميع القراءات والأنماط"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM ayahs
            WHERE surah_id = ? AND ayah_id = ?
        """, (surah_id, ayah_id))

        ayah = cursor.fetchone()
        conn.close()

        if ayah:
            return jsonify(dict_from_row(ayah))
        else:
            return jsonify({'error': 'الآية غير موجودة'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/page/<int:page_num>')
def get_page(page_num):
    """الحصول على آيات صفحة معينة"""
    text_type = request.args.get('text_type', 'text_uthmani')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT
                a.id, a.surah_id, a.ayah_id, a.page, a.juz,
                s.name_ar as surah_name,
                {text_type} as text
            FROM ayahs a
            JOIN surahs s ON a.surah_id = s.id
            WHERE a.page = ?
            ORDER BY a.id
        """

        cursor.execute(query, (page_num,))
        ayahs = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(ayahs)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# API: الكلمات
# ═══════════════════════════════════════════════════════════════

@app.route('/api/words')
def get_words():
    """الحصول على كلمات آية معينة مع التفاصيل"""
    surah_id = request.args.get('surah_id', type=int)
    ayah_id = request.args.get('ayah_id', type=int)

    if not surah_id or not ayah_id:
        return jsonify({'error': 'surah_id و ayah_id مطلوبان'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                w.*,
                wd.irab, wd.sarf, wd.meaning, wd.rasm
            FROM words w
            LEFT JOIN word_details wd ON w.id = wd.word_id
            WHERE w.surah_id = ? AND w.ayah_id = ?
            ORDER BY w.word_no_in_ayah
        """, (surah_id, ayah_id))

        words = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(words)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/word/<int:word_id>')
def get_word(word_id):
    """الحصول على تفاصيل كلمة محددة"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                w.*,
                wd.irab, wd.sarf, wd.meaning, wd.rasm
            FROM words w
            LEFT JOIN word_details wd ON w.id = wd.word_id
            WHERE w.id = ?
        """, (word_id,))

        word = cursor.fetchone()
        conn.close()

        if word:
            return jsonify(dict_from_row(word))
        else:
            return jsonify({'error': 'الكلمة غير موجودة'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# API: البحث
# ═══════════════════════════════════════════════════════════════

@app.route('/api/search')
def search():
    """بحث متقدم في القرآن الكريم"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'text')  # text, root, irab, meaning
    text_type = request.args.get('text_type', 'text_uthmani')
    limit = request.args.get('limit', 100, type=int)

    if not query:
        return jsonify({'error': 'نص البحث مطلوب'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if search_type == 'text':
            # بحث نصي في الآيات
            sql_query = f"""
                SELECT
                    a.surah_id, a.ayah_id,
                    s.name_ar as surah_name,
                    {text_type} as text,
                    a.page, a.juz
                FROM ayahs a
                JOIN surahs s ON a.surah_id = s.id
                WHERE {text_type} LIKE ?
                ORDER BY a.surah_id, a.ayah_id
                LIMIT ?
            """
            cursor.execute(sql_query, (f'%{query}%', limit))

        elif search_type == 'root':
            # بحث بالجذر
            cursor.execute("""
                SELECT DISTINCT
                    w.surah_id, w.ayah_id,
                    s.name_ar as surah_name,
                    w.word_text,
                    w.root
                FROM words w
                JOIN surahs s ON w.surah_id = s.id
                WHERE w.root LIKE ?
                ORDER BY w.surah_id, w.ayah_id
                LIMIT ?
            """, (f'%{query}%', limit))

        elif search_type == 'irab':
            # بحث بالإعراب
            cursor.execute("""
                SELECT DISTINCT
                    w.surah_id, w.ayah_id,
                    s.name_ar as surah_name,
                    w.word_text,
                    wd.irab
                FROM words w
                JOIN word_details wd ON w.id = wd.word_id
                JOIN surahs s ON w.surah_id = s.id
                WHERE wd.irab LIKE ?
                ORDER BY w.surah_id, w.ayah_id
                LIMIT ?
            """, (f'%{query}%', limit))

        elif search_type == 'meaning':
            # بحث في المعاني
            cursor.execute("""
                SELECT DISTINCT
                    w.surah_id, w.ayah_id,
                    s.name_ar as surah_name,
                    w.word_text,
                    wd.meaning
                FROM words w
                JOIN word_details wd ON w.id = wd.word_id
                JOIN surahs s ON w.surah_id = s.id
                WHERE wd.meaning LIKE ?
                ORDER BY w.surah_id, w.ayah_id
                LIMIT ?
            """, (f'%{query}%', limit))

        else:
            return jsonify({'error': 'نوع البحث غير صحيح'}), 400

        results = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'query': query,
            'type': search_type,
            'count': len(results),
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# API: إحصائيات
# ═══════════════════════════════════════════════════════════════

@app.route('/api/stats')
def get_stats():
    """الحصول على إحصائيات عامة"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        stats = {}

        # عدد السور
        cursor.execute("SELECT COUNT(*) FROM surahs")
        stats['surahs_count'] = cursor.fetchone()[0]

        # عدد الآيات
        cursor.execute("SELECT COUNT(*) FROM ayahs")
        stats['ayahs_count'] = cursor.fetchone()[0]

        # عدد الكلمات
        cursor.execute("SELECT COUNT(*) FROM words")
        stats['words_count'] = cursor.fetchone()[0]

        # عدد الجذور الفريدة
        cursor.execute("SELECT COUNT(DISTINCT root) FROM words WHERE root IS NOT NULL")
        stats['roots_count'] = cursor.fetchone()[0]

        conn.close()

        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# تشغيل التطبيق
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # التحقق من وجود قاعدة البيانات
    if not DB_PATH.exists():
        print("❌ قاعدة البيانات غير موجودة!")
        print("   قم بتشغيل: python import_data.py")
        exit(1)

    print("╔══════════════════════════════════════════════════════════╗")
    print("║         📖 Quran Clean - التطبيق القرآني النظيف       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("🚀 التطبيق يعمل على: http://127.0.0.1:5000")
    print("📖 افتح المتصفح واذهب إلى العنوان أعلاه")
    print()
    print("💡 للإيقاف: اضغط Ctrl+C")
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
