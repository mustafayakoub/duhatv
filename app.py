#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق القرآن الرقمي - Offline
==============================
تطبيق Flask بسيط لعرض القرآن الكريم
"""

from flask import Flask, render_template, jsonify, request, send_file
import sqlite3
from pathlib import Path
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

DB_PATH = Path("databases/AYAHS_DATABASE_ENHANCED.db")


def get_db():
    """الحصول على اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')


@app.route('/download')
def download_page():
    """صفحة التحميل"""
    return render_template('download.html')


@app.route('/api/surahs')
def get_surahs():
    """الحصول على قائمة السور"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT
            a.sura_no,
            t.aya_text_emlaey as sura_name
        FROM ayahs a
        JOIN ayah_texts t ON a.id = t.ayah_id
        ORDER BY a.sura_no
    """)

    surahs = []
    current_surah = None

    for row in cursor.fetchall():
        if current_surah != row['sura_no']:
            current_surah = row['sura_no']

            # عد الآيات
            count = cursor.execute(
                "SELECT COUNT(*) FROM ayahs WHERE sura_no = ?",
                (current_surah,)
            ).fetchone()[0]

            surahs.append({
                'number': current_surah,
                'name': 'الفاتحة' if current_surah == 1 else 'البقرة',
                'ayah_count': count
            })

    conn.close()
    return jsonify(surahs)


@app.route('/api/versions')
def get_versions():
    """الحصول على قائمة القراءات المتاحة"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            version_code,
            version_name_ar,
            version_name_en,
            qiraa,
            script_type,
            is_default
        FROM text_versions
        WHERE qiraa IS NOT NULL
        ORDER BY
            CASE
                WHEN is_default = 1 THEN 0
                ELSE 1
            END,
            id
    """)

    versions = []
    for row in cursor.fetchall():
        versions.append({
            'code': row['version_code'],
            'name_ar': row['version_name_ar'],
            'name_en': row['version_name_en'],
            'qiraa': row['qiraa'],
            'script_type': row['script_type'],
            'is_default': bool(row['is_default'])
        })

    conn.close()
    return jsonify(versions)


@app.route('/api/surah/<int:surah_no>')
def get_surah(surah_no):
    """الحصول على آيات سورة معينة"""
    version_code = request.args.get('version', 'hafs_smart_v8')

    conn = get_db()
    cursor = conn.cursor()

    # الحصول على version_id
    version_id = cursor.execute(
        "SELECT id FROM text_versions WHERE version_code = ?",
        (version_code,)
    ).fetchone()

    if not version_id:
        conn.close()
        return jsonify({'error': 'Version not found'}), 404

    version_id = version_id[0]

    cursor.execute("""
        SELECT
            a.sura_no,
            a.aya_no,
            a.jozz,
            a.page,
            t.aya_text,
            t.aya_text_emlaey,
            t.word_count,
            t.letter_count
        FROM ayahs a
        JOIN ayah_texts t ON a.id = t.ayah_id
        WHERE a.sura_no = ? AND t.version_id = ?
        ORDER BY a.aya_no
    """, (surah_no, version_id))

    ayahs = []
    for row in cursor.fetchall():
        ayahs.append({
            'sura_no': row['sura_no'],
            'aya_no': row['aya_no'],
            'jozz': row['jozz'],
            'page': row['page'],
            'text': row['aya_text'],
            'text_emlaey': row['aya_text_emlaey'],
            'word_count': row['word_count'],
            'letter_count': row['letter_count']
        })

    conn.close()
    return jsonify(ayahs)


@app.route('/api/search')
def search():
    """البحث في القرآن"""
    query = request.args.get('q', '')

    if not query:
        return jsonify([])

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.sura_no,
            a.aya_no,
            t.aya_text,
            t.aya_text_emlaey
        FROM ayahs a
        JOIN ayah_texts t ON a.id = t.ayah_id
        WHERE t.search_text LIKE ?
        ORDER BY a.sura_no, a.aya_no
        LIMIT 50
    """, (f'%{query}%',))

    results = []
    for row in cursor.fetchall():
        results.append({
            'sura_no': row['sura_no'],
            'aya_no': row['aya_no'],
            'text': row['aya_text'],
            'text_emlaey': row['aya_text_emlaey']
        })

    conn.close()
    return jsonify(results)


@app.route('/api/stats')
def get_stats():
    """إحصائيات عامة"""
    conn = get_db()
    cursor = conn.cursor()

    total_ayahs = cursor.execute("SELECT COUNT(*) FROM ayahs").fetchone()[0]
    total_words = cursor.execute("SELECT SUM(word_count) FROM ayah_texts").fetchone()[0]
    total_letters = cursor.execute("SELECT SUM(letter_count) FROM ayah_texts").fetchone()[0]

    conn.close()

    return jsonify({
        'total_ayahs': total_ayahs,
        'total_words': total_words,
        'total_letters': total_letters
    })


@app.route('/download/updates')
def download_updates():
    """تحميل ملف التحديثات المضغوط"""
    # البحث عن أحدث ملف zip
    import glob
    zip_files = glob.glob('duhatv_updates_*.zip')

    if not zip_files:
        return jsonify({'error': 'ملف التحديثات غير موجود'}), 404

    # أحدث ملف
    latest_zip = sorted(zip_files)[-1]

    return send_file(
        latest_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name=os.path.basename(latest_zip)
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
