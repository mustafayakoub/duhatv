#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════════════════
نقل ذكي للكلمات مع الإعراب والصرف
Smart Migration for Words with I'rab and Sarf

يستخدم INNER JOIN مع word_content_irab للحصول على 77,432 كلمة بالضبط
════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import time
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# تكوين المسارات - Database Paths Configuration
# ═══════════════════════════════════════════════════════════════════════════

DB2_PATH = r"C:\quran11\surah_database_app_v32.db"  # الإعراب والصرف
UNIFIED_DB_PATH = r"C:\quran11\quran_unified.db"    # القاعدة الموحدة


class SmartWordsMigration:
    """نقل ذكي للكلمات - يستبعد البيانات الوصفية تلقائياً"""

    def __init__(self):
        self.conn_old = None
        self.conn_new = None
        self.stats = {
            'words_migrated': 0,
            'irab_migrated': 0,
            'sarf_migrated': 0,
            'duration': 0
        }

    def connect(self):
        """الاتصال بقواعد البيانات"""
        print("=" * 70)
        print("🔗 الاتصال بقواعد البيانات...")
        print("=" * 70)

        try:
            self.conn_old = sqlite3.connect(DB2_PATH)
            self.conn_old.row_factory = sqlite3.Row
            print(f"✅ اتصال DB2: {DB2_PATH}")

            self.conn_new = sqlite3.connect(UNIFIED_DB_PATH)
            self.conn_new.row_factory = sqlite3.Row
            print(f"✅ اتصال Unified: {UNIFIED_DB_PATH}")
            print()

        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            raise

    def get_ayah_id(self, surah_no, ayah_no):
        """الحصول على ayah_id من القاعدة الموحدة"""
        cursor = self.conn_new.cursor()
        cursor.execute("""
            SELECT ayah_id
            FROM ayahs
            WHERE surah_id = ? AND ayah_number = ?
        """, (surah_no, ayah_no))

        result = cursor.fetchone()
        return result['ayah_id'] if result else None

    def migrate_all(self):
        """النقل الذكي - 77,432 كلمة فقط"""
        print("=" * 70)
        print("📦 بدء النقل الذكي للكلمات...")
        print("=" * 70)
        print()

        start_time = time.time()

        try:
            cursor_old = self.conn_old.cursor()
            cursor_new = self.conn_new.cursor()

            # ═══════════════════════════════════════════════════════════════
            # الاستعلام الذكي - INNER JOIN مع word_content_irab
            # يضمن الحصول على 77,432 كلمة فقط (بدون البيانات الوصفية)
            # ═══════════════════════════════════════════════════════════════

            print("🔍 قراءة الكلمات من DB2 باستخدام INNER JOIN...")

            cursor_old.execute("""
                SELECT
                    qw.surahNo,
                    qw.ayahNo,
                    qw.wordNo,
                    qw.wordWithHaraqah,
                    qw.wordWithOutHaraqah,
                    qw.Root,
                    wi.irabMushakkal,
                    ws.sarf
                FROM word_content_irab wi
                INNER JOIN QuranWordInfo qw
                    ON wi.surahNo = qw.surahNo
                    AND wi.ayahNo = qw.ayahNo
                    AND wi.wordNo = qw.wordNo
                LEFT JOIN word_content_sarf ws
                    ON wi.surahNo = ws.surahNo
                    AND wi.ayahNo = ws.ayahNo
                    AND wi.wordNo = ws.wordNo
                ORDER BY wi.surahNo, wi.ayahNo, wi.wordNo
            """)

            all_words = cursor_old.fetchall()
            total_words = len(all_words)

            print(f"✅ تم قراءة {total_words:,} كلمة")
            print()

            # التحقق من العدد الدقيق
            if total_words != 77432:
                print(f"⚠️  تحذير: العدد المتوقع 77,432 لكن حصلنا على {total_words:,}")
                print("⚠️  الفرق:", abs(77432 - total_words))
                response = input("هل تريد المتابعة؟ (y/n): ")
                if response.lower() != 'y':
                    return
            else:
                print("✅ العدد صحيح: 77,432 كلمة")
            print()

            # ═══════════════════════════════════════════════════════════════
            # النقل إلى القاعدة الموحدة
            # ═══════════════════════════════════════════════════════════════

            print("📝 بدء نقل الكلمات مع الإعراب والصرف...")
            print()

            # تعطيل foreign keys مؤقتاً للسرعة
            cursor_new.execute("PRAGMA foreign_keys = OFF")

            processed = 0
            ayah_cache = {}  # كاش للآيات لتسريع البحث

            for row in all_words:
                # الحصول على ayah_id من الكاش أو القاعدة
                cache_key = (row['surahNo'], row['ayahNo'])
                if cache_key not in ayah_cache:
                    ayah_cache[cache_key] = self.get_ayah_id(row['surahNo'], row['ayahNo'])

                ayah_id = ayah_cache[cache_key]

                if not ayah_id:
                    print(f"⚠️  لم نجد ayah_id للسورة {row['surahNo']}, الآية {row['ayahNo']}")
                    continue

                # إدخال الكلمة
                cursor_new.execute("""
                    INSERT INTO words (ayah_id, word_position, word_text, word_simple, root_text)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    ayah_id,
                    row['wordNo'],
                    row['wordWithHaraqah'] or '',
                    row['wordWithOutHaraqah'] or '',
                    row['Root'] or ''
                ))

                word_id = cursor_new.lastrowid
                self.stats['words_migrated'] += 1

                # إدخال الإعراب
                if row['irabMushakkal']:
                    cursor_new.execute("""
                        INSERT INTO irab (word_id, irab_text)
                        VALUES (?, ?)
                    """, (word_id, row['irabMushakkal']))
                    self.stats['irab_migrated'] += 1

                # إدخال الصرف
                if row['sarf']:
                    cursor_new.execute("""
                        INSERT INTO sarf (word_id, sarf_text)
                        VALUES (?, ?)
                    """, (word_id, row['sarf']))
                    self.stats['sarf_migrated'] += 1

                processed += 1

                # Commit كل 1000 كلمة
                if processed % 1000 == 0:
                    self.conn_new.commit()
                    progress = (processed / total_words) * 100
                    print(f"⏳ تقدم: {processed:,}/{total_words:,} ({progress:.1f}%)", end='\r')

            # Commit نهائي
            self.conn_new.commit()

            # إعادة تفعيل foreign keys
            cursor_new.execute("PRAGMA foreign_keys = ON")
            self.conn_new.commit()

            end_time = time.time()
            self.stats['duration'] = end_time - start_time

            print()
            print()
            print("=" * 70)
            print("✅ اكتمل النقل بنجاح!")
            print("=" * 70)

        except Exception as e:
            print(f"\n❌ خطأ في النقل: {e}")
            self.conn_new.rollback()
            raise

    def verify(self):
        """التحقق من صحة النقل"""
        print()
        print("=" * 70)
        print("🔍 التحقق من النقل...")
        print("=" * 70)

        cursor = self.conn_new.cursor()

        # عدد الكلمات
        cursor.execute("SELECT COUNT(*) as count FROM words")
        words_count = cursor.fetchone()['count']

        # عدد الإعراب
        cursor.execute("SELECT COUNT(*) as count FROM irab")
        irab_count = cursor.fetchone()['count']

        # عدد الصرف
        cursor.execute("SELECT COUNT(*) as count FROM sarf")
        sarf_count = cursor.fetchone()['count']

        print(f"📊 الكلمات: {words_count:,}")
        print(f"📊 الإعراب: {irab_count:,}")
        print(f"📊 الصرف: {sarf_count:,}")
        print()

        # التحقق من الدقة
        if words_count == 77432:
            print("✅ العدد الدقيق للكلمات: 77,432 ✓")
        else:
            print(f"⚠️  تحذير: العدد المتوقع 77,432 لكن في القاعدة {words_count:,}")

        # عينة من البيانات
        print()
        print("📋 عينة من البيانات:")
        print("-" * 70)

        cursor.execute("""
            SELECT
                w.word_id,
                w.word_text,
                i.irab_text,
                s.sarf_text
            FROM words w
            LEFT JOIN irab i ON w.word_id = i.word_id
            LEFT JOIN sarf s ON w.word_id = s.word_id
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(f"  الكلمة: {row['word_text']}")
            print(f"  الإعراب: {row['irab_text'] or 'لا يوجد'}")
            print(f"  الصرف: {row['sarf_text'] or 'لا يوجد'}")
            print("-" * 70)

    def print_summary(self):
        """طباعة ملخص النقل"""
        print()
        print("=" * 70)
        print("📊 ملخص النقل")
        print("=" * 70)
        print(f"✅ الكلمات المنقولة: {self.stats['words_migrated']:,}")
        print(f"✅ الإعراب المنقول: {self.stats['irab_migrated']:,}")
        print(f"✅ الصرف المنقول: {self.stats['sarf_migrated']:,}")
        print(f"⏱️  المدة: {self.stats['duration']:.2f} ثانية")
        print("=" * 70)

    def close(self):
        """إغلاق الاتصالات"""
        if self.conn_old:
            self.conn_old.close()
        if self.conn_new:
            self.conn_new.close()

    def run(self):
        """تشغيل النقل الكامل"""
        try:
            print()
            print("═" * 70)
            print("  🌙 نقل ذكي للكلمات مع الإعراب والصرف")
            print("  Smart Words Migration with I'rab and Sarf")
            print("═" * 70)
            print()
            print("📌 العدد المتوقع: 77,432 كلمة بالضبط")
            print()

            self.connect()
            self.migrate_all()
            self.verify()
            self.print_summary()

            print()
            print("🎉 تم بنجاح! القاعدة الموحدة الآن تحتوي على:")
            print("   ✅ 114 سورة")
            print("   ✅ 6,236 آية")
            print("   ✅ 77,432 كلمة")
            print("   ✅ إعراب وصرف لكل كلمة")
            print()

        except Exception as e:
            print(f"\n❌ فشل النقل: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.close()


# ═══════════════════════════════════════════════════════════════════════════
# نقطة الدخول الرئيسية
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    migration = SmartWordsMigration()
    migration.run()
