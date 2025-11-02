#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
عارض القرآن الشجري - Quran Tree Viewer
تطبيق ويب تفاعلي لعرض القرآن الكريم مع الإعراب والصرف
════════════════════════════════════════════════════════════════════════════
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# مسار قاعدة البيانات
DB_PATH = r"C:\quran11\quran_unified.db"


def get_db():
    """الاتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """الصفحة الرئيسية - قائمة السور"""
    return render_template('tree_index.html')


@app.route('/api/surahs')
def get_surahs():
    """جلب قائمة السور"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                surah_id,
                name_arabic,
                name_english,
                ayah_count,
                revelation_type
            FROM surahs
            ORDER BY surah_id
        """)

        surahs = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'count': len(surahs),
            'data': surahs
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/surah/<int:surah_id>/ayahs')
def get_ayahs(surah_id):
    """جلب آيات سورة معينة"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ayah_id,
                ayah_number,
                text_uthmani,
                juz_number,
                page_number
            FROM ayahs
            WHERE surah_id = ?
            ORDER BY ayah_number
        """, (surah_id,))

        ayahs = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'count': len(ayahs),
            'data': ayahs
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ayah/<int:ayah_id>/words')
def get_words(ayah_id):
    """جلب كلمات آية معينة"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                w.word_id,
                w.word_position,
                w.word_text,
                w.word_simple,
                w.root_text,
                i.irab_text,
                s.sarf_text
            FROM words w
            LEFT JOIN irab i ON w.word_id = i.word_id
            LEFT JOIN sarf s ON w.word_id = s.word_id
            WHERE w.ayah_id = ?
            ORDER BY w.word_position
        """, (ayah_id,))

        words = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'count': len(words),
            'data': words
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """إحصائيات القاعدة"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        stats = {}

        # عدد السور
        cursor.execute("SELECT COUNT(*) as count FROM surahs")
        stats['surahs'] = cursor.fetchone()['count']

        # عدد الآيات
        cursor.execute("SELECT COUNT(*) as count FROM ayahs")
        stats['ayahs'] = cursor.fetchone()['count']

        # عدد الكلمات
        cursor.execute("SELECT COUNT(*) as count FROM words")
        stats['words'] = cursor.fetchone()['count']

        # عدد الإعراب
        cursor.execute("SELECT COUNT(*) as count FROM irab")
        stats['irab'] = cursor.fetchone()['count']

        # عدد الصرف
        cursor.execute("SELECT COUNT(*) as count FROM sarf")
        stats['sarf'] = cursor.fetchone()['count']

        conn.close()

        return jsonify({
            'success': True,
            'data': stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search')
def search():
    """البحث في القرآن"""
    query = request.args.get('q', '').strip()

    if len(query) < 2:
        return jsonify({
            'success': False,
            'error': 'استعلام قصير جداً'
        }), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # البحث في نص الآيات
        cursor.execute("""
            SELECT
                a.ayah_id,
                a.ayah_number,
                a.text_uthmani,
                s.surah_id,
                s.name_arabic
            FROM ayahs a
            JOIN surahs s ON a.surah_id = s.surah_id
            WHERE a.text_uthmani LIKE ?
            ORDER BY s.surah_id, a.ayah_number
            LIMIT 50
        """, (f'%{query}%',))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'count': len(results),
            'data': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print()
    print("═" * 70)
    print("  🌙 عارض القرآن الشجري - Quran Tree Viewer")
    print("═" * 70)
    print()
    print("📊 قاعدة البيانات:", DB_PATH)
    print()
    print("🚀 التطبيق يعمل على:")
    print("   http://localhost:5000")
    print()
    print("🔗 افتح المتصفح وانتقل إلى:")
    print("   http://localhost:5000")
    print()
    print("═" * 70)
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
