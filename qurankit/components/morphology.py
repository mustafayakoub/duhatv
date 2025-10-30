#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 QuranMorphologyComponent - البحث الصرفي
Morphological Analysis Component
"""

from typing import List, Dict, Any, Optional
import re


class QuranMorphologyComponent:
    """مكون البحث الصرفي والتحليل اللغوي"""

    def __init__(self, database, config: Dict = None):
        self.database = database
        self.config = config or {}
        self.max_results = self.config.get('max_results', 100)

    def search_by_root(self, root: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """البحث بالجذر الثلاثي"""
        limit = limit or self.max_results

        if not hasattr(self.database, 'search_by_root'):
            # إذا لم تدعم قاعدة البيانات البحث بالجذر، استخدم البحث النصي
            return self.database.search_text(root, limit=limit) if hasattr(self.database, 'search_text') else []

        try:
            results = self.database.search_by_root(root, ['quran'])
            return results[:limit]
        except Exception as e:
            print(f"خطأ في البحث بالجذر: {e}")
            return []

    def search_by_pattern(self, pattern: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """البحث بالوزن الصرفي (مثل: فَعَلَ، فاعِل)"""
        limit = limit or self.max_results

        if not hasattr(self.database, 'search_by_pattern'):
            # استخدام البحث النصي كبديل
            return self.database.search_text(pattern, limit=limit) if hasattr(self.database, 'search_text') else []

        try:
            results = self.database.search_by_pattern(pattern, ['quran'])
            return results[:limit]
        except Exception as e:
            print(f"خطأ في البحث بالوزن: {e}")
            return []

    def analyze_word(self, word: str) -> Dict[str, Any]:
        """تحليل كلمة عربية (جذر، وزن، نوع)"""
        # إزالة التشكيل
        word_no_tashkeel = self.remove_tashkeel(word)

        analysis = {
            'word': word,
            'word_no_tashkeel': word_no_tashkeel,
            'length': len(word_no_tashkeel),
            'root': self.extract_root(word_no_tashkeel),
            'pattern': self.extract_pattern(word_no_tashkeel),
            'type': self.get_word_type(word_no_tashkeel)
        }

        return analysis

    def extract_root(self, word: str) -> Optional[str]:
        """استخراج الجذر من الكلمة (طريقة تقريبية)"""
        # هذه طريقة مبسطة - في التطبيقات الحقيقية يجب استخدام مكتبة متخصصة
        word = self.remove_tashkeel(word)

        # إزالة أحرف الزيادة الشائعة
        prefixes = ['ال', 'و', 'ف', 'ب', 'ك', 'ل', 'لل']
        suffixes = ['ة', 'ه', 'ها', 'هم', 'هن', 'ك', 'كم', 'كن', 'ي', 'نا']

        for prefix in prefixes:
            if word.startswith(prefix):
                word = word[len(prefix):]
                break

        for suffix in suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)]
                break

        # الجذر عادة 3 أحرف
        if len(word) >= 3:
            return word[:3]

        return word

    def extract_pattern(self, word: str) -> str:
        """استخراج الوزن الصرفي (تقريبي)"""
        # هذه طريقة مبسطة جداً
        word = self.remove_tashkeel(word)

        # استبدال الأحرف بأحرف الوزن (ف ع ل)
        pattern_chars = ['ف', 'ع', 'ل', 'ف', 'ع', 'ل']
        if len(word) <= len(pattern_chars):
            return ''.join(pattern_chars[:len(word)])

        return 'غير محدد'

    def get_word_type(self, word: str) -> str:
        """تحديد نوع الكلمة (اسم، فعل، حرف)"""
        # طريقة تقريبية بسيطة
        word = self.remove_tashkeel(word)

        # أدوات وحروف شائعة
        particles = ['في', 'من', 'إلى', 'على', 'عن', 'الى', 'و', 'ف', 'ب', 'ك', 'ل']
        if word in particles or len(word) <= 2:
            return 'حرف'

        # أنماط الأفعال
        verb_patterns = [
            r'^ي.+',  # يفعل
            r'^ت.+',  # تفعل
            r'^ن.+',  # نفعل
            r'^أ.+',  # أفعل
        ]

        for pattern in verb_patterns:
            if re.match(pattern, word):
                return 'فعل'

        return 'اسم'

    def remove_tashkeel(self, text: str) -> str:
        """إزالة التشكيل من النص العربي"""
        tashkeel_pattern = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        return tashkeel_pattern.sub('', text)

    def get_word_forms(self, root: str) -> List[str]:
        """الحصول على أشكال مختلفة من نفس الجذر"""
        # هذه وظيفة تقريبية - في التطبيقات الحقيقية تحتاج قاعدة بيانات صرفية
        if len(root) != 3:
            return [root]

        r1, r2, r3 = root[0], root[1], root[2]

        forms = [
            root,  # الجذر الأصلي
            f"{r1}{r2}ّ{r3}",  # مشدد
            f"{r1}ا{r2}{r3}",  # فاعل
            f"م{r1}{r2}و{r3}",  # مفعول
            f"{r1}{r2}ي{r3}",  # فعيل
            f"{r1}و{r2}{r3}",  # فوعل
        ]

        return forms

    def count_root_occurrences(self, root: str) -> int:
        """عد تكرارات الجذر في القرآن"""
        results = self.search_by_root(root, limit=10000)
        return len(results)

    def get_morphology_statistics(self) -> Dict[str, Any]:
        """إحصائيات صرفية عامة"""
        stats = {
            'total_words': 0,
            'unique_roots': 0,
            'verbs_count': 0,
            'nouns_count': 0,
            'particles_count': 0
        }

        # هذه تحتاج إلى قاعدة بيانات صرفية كاملة
        # يمكن تنفيذها لاحقاً مع دعم قاعدة بيانات متقدمة

        return stats
