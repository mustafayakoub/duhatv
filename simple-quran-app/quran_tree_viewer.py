#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
عارض القرآن الشجري المحسّن - Enhanced Quran Tree Viewer
تطبيق ويب تفاعلي لعرض القرآن الكريم مع الإعراب والصرف
════════════════════════════════════════════════════════════════════════════
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# مسار قاعدة البيانات
DB_PATH = r"C:\quran11\quran_unified.db"

# دالة لإزالة التشكيل للبحث الذكي
def normalize_arabic(text):
    """إزالة التشكيل من النص العربي"""
    arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    return arabic_diacritics.sub('', text)


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
    """جلب كلمات آية معينة مع الترتيب"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        # الحصول على معلومات الآية أولاً
        cursor.execute("""
            SELECT surah_id, ayah_number
            FROM ayahs
            WHERE ayah_id = ?
        """, (ayah_id,))

        ayah_info = cursor.fetchone()
        if not ayah_info:
            return jsonify({'success': False, 'error': 'Ayah not found'}), 404

        surah_id = ayah_info['surah_id']
        ayah_number = ayah_info['ayah_number']

        # حساب الترتيب في السورة
        cursor.execute("""
            SELECT COUNT(*) as position_in_surah
            FROM words w
            JOIN ayahs a ON w.ayah_id = a.ayah_id
            WHERE a.surah_id = ? AND (
                a.ayah_number < ? OR
                (a.ayah_number = ? AND w.word_position < (
                    SELECT word_position FROM words WHERE ayah_id = ? LIMIT 1
                ))
            )
        """, (surah_id, ayah_number, ayah_number, ayah_id))

        base_position_in_surah = cursor.fetchone()['position_in_surah']

        # حساب الترتيب في المصحف
        cursor.execute("""
            SELECT COUNT(*) as position_in_quran
            FROM words w
            JOIN ayahs a ON w.ayah_id = a.ayah_id
            WHERE a.surah_id < ? OR (
                a.surah_id = ? AND a.ayah_number < ?
            )
        """, (surah_id, surah_id, ayah_number))

        base_position_in_quran = cursor.fetchone()['position_in_quran']

        # جلب الكلمات
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

        words = []
        for idx, row in enumerate(cursor.fetchall()):
            word_dict = dict(row)
            word_dict['position_in_surah'] = base_position_in_surah + idx + 1
            word_dict['position_in_quran'] = base_position_in_quran + idx + 1
            words.append(word_dict)

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
    """البحث الذكي في القرآن - بدون تشكيل"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'text')  # text, root, etc.

    if len(query) < 2:
        return jsonify({
            'success': False,
            'error': 'استعلام قصير جداً'
        }), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # تطبيع النص للبحث بدون تشكيل
        normalized_query = normalize_arabic(query)

        results = []

        if search_type == 'root':
            # البحث بالجذر
            cursor.execute("""
                SELECT DISTINCT
                    a.ayah_id,
                    a.ayah_number,
                    a.text_uthmani,
                    s.surah_id,
                    s.name_arabic,
                    a.juz_number,
                    a.page_number
                FROM ayahs a
                JOIN surahs s ON a.surah_id = s.surah_id
                JOIN words w ON a.ayah_id = w.ayah_id
                WHERE w.root_text LIKE ?
                ORDER BY s.surah_id, a.ayah_number
                LIMIT 100
            """, (f'%{query}%',))
            results = [dict(row) for row in cursor.fetchall()]
        else:
            # البحث النصي الذكي - بدون تشكيل
            cursor.execute("""
                SELECT
                    a.ayah_id,
                    a.ayah_number,
                    a.text_uthmani,
                    s.surah_id,
                    s.name_arabic,
                    s.ayah_count,
                    a.juz_number,
                    a.page_number
                FROM ayahs a
                JOIN surahs s ON a.surah_id = s.surah_id
                ORDER BY s.surah_id, a.ayah_number
            """)

            # فلترة النتائج باستخدام البحث بدون تشكيل
            all_ayahs = cursor.fetchall()
            for ayah in all_ayahs:
                normalized_text = normalize_arabic(ayah['text_uthmani'])
                if normalized_query in normalized_text:
                    results.append(dict(ayah))
                    if len(results) >= 100:
                        break

        # تنظيم النتائج حسب السور
        organized_results = {}
        for result in results:
            surah_id = result['surah_id']
            if surah_id not in organized_results:
                organized_results[surah_id] = {
                    'surah_id': surah_id,
                    'name_arabic': result['name_arabic'],
                    'ayahs': []
                }
            organized_results[surah_id]['ayahs'].append({
                'ayah_id': result['ayah_id'],
                'ayah_number': result['ayah_number'],
                'text_uthmani': result['text_uthmani'],
                'juz_number': result.get('juz_number'),
                'page_number': result.get('page_number')
            })

        conn.close()

        return jsonify({
            'success': True,
            'count': len(results),
            'total_surahs': len(organized_results),
            'data': list(organized_results.values())
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print()
    print("═" * 70)
    print("  🌙 عارض القرآن الشجري المحسّن")
    print("  Enhanced Quran Tree Viewer")
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
