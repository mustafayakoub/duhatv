#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔖 QuranBookmarksComponent - الإشارات المرجعية
Bookmarks Component for managing user bookmarks
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path


class QuranBookmarksComponent:
    """مكون إدارة الإشارات المرجعية"""

    def __init__(self, database=None, config: Dict = None):
        self.database = database
        self.config = config or {}
        self.bookmarks = []
        self.bookmarks_file = Path(self.config.get('bookmarks_file', Path.home() / '.qurankit' / 'bookmarks.json'))

        # تحميل الإشارات من الملف
        self.load_bookmarks()

    def add_bookmark(self, sura: int, ayah: int, note: str = "") -> bool:
        """إضافة إشارة مرجعية"""
        # التحقق من عدم وجود إشارة مكررة
        if self.has_bookmark(sura, ayah):
            return False

        bookmark = {
            'id': len(self.bookmarks) + 1,
            'sura': sura,
            'ayah': ayah,
            'note': note,
            'created_at': datetime.now().isoformat(),
            'sura_name': self._get_sura_name(sura)
        }

        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        return True

    def remove_bookmark(self, bookmark_id: int) -> bool:
        """حذف إشارة مرجعية"""
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark['id'] == bookmark_id:
                self.bookmarks.pop(i)
                self.save_bookmarks()
                return True
        return False

    def remove_bookmark_by_location(self, sura: int, ayah: int) -> bool:
        """حذف إشارة حسب الموقع"""
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark['sura'] == sura and bookmark['ayah'] == ayah:
                self.bookmarks.pop(i)
                self.save_bookmarks()
                return True
        return False

    def update_bookmark_note(self, bookmark_id: int, note: str) -> bool:
        """تحديث ملاحظة إشارة"""
        for bookmark in self.bookmarks:
            if bookmark['id'] == bookmark_id:
                bookmark['note'] = note
                bookmark['updated_at'] = datetime.now().isoformat()
                self.save_bookmarks()
                return True
        return False

    def has_bookmark(self, sura: int, ayah: int) -> bool:
        """التحقق من وجود إشارة"""
        return any(b['sura'] == sura and b['ayah'] == ayah for b in self.bookmarks)

    def get_bookmark(self, bookmark_id: int) -> Optional[Dict[str, Any]]:
        """الحصول على إشارة محددة"""
        for bookmark in self.bookmarks:
            if bookmark['id'] == bookmark_id:
                return bookmark
        return None

    def get_all_bookmarks(self) -> List[Dict[str, Any]]:
        """الحصول على كل الإشارات"""
        return sorted(self.bookmarks, key=lambda x: (x['sura'], x['ayah']))

    def get_bookmarks_by_sura(self, sura: int) -> List[Dict[str, Any]]:
        """الحصول على إشارات سورة معينة"""
        return [b for b in self.bookmarks if b['sura'] == sura]

    def get_recent_bookmarks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """الحصول على أحدث الإشارات"""
        sorted_bookmarks = sorted(
            self.bookmarks,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )
        return sorted_bookmarks[:limit]

    def search_bookmarks(self, query: str) -> List[Dict[str, Any]]:
        """البحث في الإشارات"""
        query = query.lower()
        results = []

        for bookmark in self.bookmarks:
            # البحث في الملاحظات واسم السورة
            if (query in bookmark.get('note', '').lower() or
                query in bookmark.get('sura_name', '').lower() or
                query in str(bookmark.get('sura', '')) or
                query in str(bookmark.get('ayah', ''))):
                results.append(bookmark)

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """إحصائيات الإشارات"""
        stats = {
            'total_bookmarks': len(self.bookmarks),
            'with_notes': sum(1 for b in self.bookmarks if b.get('note')),
            'without_notes': sum(1 for b in self.bookmarks if not b.get('note')),
            'suras_bookmarked': len(set(b['sura'] for b in self.bookmarks)),
        }

        # السورة الأكثر إشارات
        if self.bookmarks:
            sura_counts = {}
            for bookmark in self.bookmarks:
                sura = bookmark['sura']
                sura_counts[sura] = sura_counts.get(sura, 0) + 1

            most_bookmarked_sura = max(sura_counts, key=sura_counts.get)
            stats['most_bookmarked_sura'] = most_bookmarked_sura
            stats['most_bookmarked_sura_name'] = self._get_sura_name(most_bookmarked_sura)
            stats['most_bookmarked_count'] = sura_counts[most_bookmarked_sura]

        return stats

    def export_bookmarks(self, file_path: Path = None) -> bool:
        """تصدير الإشارات إلى ملف"""
        try:
            export_path = file_path or Path.home() / 'quran_bookmarks_export.json'
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في تصدير الإشارات: {e}")
            return False

    def import_bookmarks(self, file_path: Path) -> bool:
        """استيراد إشارات من ملف"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)

            # إضافة الإشارات المستوردة
            for bookmark in imported:
                if not self.has_bookmark(bookmark['sura'], bookmark['ayah']):
                    self.bookmarks.append(bookmark)

            self.save_bookmarks()
            return True
        except Exception as e:
            print(f"خطأ في استيراد الإشارات: {e}")
            return False

    def clear_all_bookmarks(self) -> bool:
        """حذف كل الإشارات"""
        self.bookmarks = []
        self.save_bookmarks()
        return True

    def save_bookmarks(self):
        """حفظ الإشارات إلى ملف"""
        try:
            self.bookmarks_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ الإشارات: {e}")

    def load_bookmarks(self):
        """تحميل الإشارات من ملف"""
        try:
            if self.bookmarks_file.exists():
                with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                    self.bookmarks = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل الإشارات: {e}")
            self.bookmarks = []

    def _get_sura_name(self, sura: int) -> str:
        """الحصول على اسم السورة"""
        if self.database and hasattr(self.database, 'get_sura_info'):
            try:
                info = self.database.get_sura_info(sura)
                return info.get('name', f'السورة {sura}')
            except:
                pass
        return f'السورة {sura}'
