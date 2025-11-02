#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 QuranTajweedComponent - نظام ألوان التجويد
Tajweed Colors Component for Quran applications
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TajweedRule:
    """قاعدة تجويد"""
    id: int
    name: str
    name_en: str
    color: str
    description: str = ""
    category: str = ""


class QuranTajweedComponent:
    """
    مكون شامل لإدارة ألوان وأحكام التجويد

    Features:
    - تحويل رموز التجويد إلى HTML ملون
    - البحث عن أحكام تجويدية محددة
    - إحصائيات التجويد
    - تخصيص الألوان
    - دعم خطوط متعددة
    """

    # نظام أحكام التجويد الكامل (15 حكم)
    DEFAULT_RULES = {
        1: TajweedRule(1, 'إظهار', 'Izhar', '#696969', 'إظهار حلقي', 'نون ساكنة وتنوين'),
        2: TajweedRule(2, 'إدغام', 'Idgham', '#228B22', 'إدغام بدون غنة', 'نون ساكنة وتنوين'),
        3: TajweedRule(3, 'إدغام بغنة', 'Idgham Ghunnah', '#2E8B57', 'إدغام مع غنة', 'نون ساكنة وتنوين'),
        4: TajweedRule(4, 'مد', 'Madd', '#DC143C', 'مد طبيعي أو فرعي', 'المدود'),
        5: TajweedRule(5, 'قلقلة', 'Qalqalah', '#4169E1', 'قلقلة (قطب جد)', 'الحروف المقلقلة'),
        6: TajweedRule(6, 'سكون', 'Sukoon', '#2F4F4F', 'سكون', 'السكون'),
        7: TajweedRule(7, 'غنة', 'Ghunnah', '#FF8C00', 'غنة مشددة', 'الغنة'),
        8: TajweedRule(8, 'شدة', 'Shaddah', '#8B0000', 'تشديد', 'الشدة'),
        9: TajweedRule(9, 'إقلاب', 'Iqlab', '#9370DB', 'قلب النون إلى ميم', 'نون ساكنة وتنوين'),
        10: TajweedRule(10, 'تفخيم', 'Tafkheem', '#8B4513', 'تفخيم', 'حروف الاستعلاء'),
        11: TajweedRule(11, 'ترقيق', 'Tarqeeq', '#4682B4', 'ترقيق', 'الحروف المرققة'),
        12: TajweedRule(12, 'إخفاء', 'Ikhfa', '#D4AF37', 'إخفاء', 'نون ساكنة وتنوين'),
        13: TajweedRule(13, 'صفير', 'Safeer', '#20B2AA', 'صفير (ص ز س)', 'حروف الصفير'),
        14: TajweedRule(14, 'لين', 'Leen', '#DDA0DD', 'حرف لين', 'حروف اللين'),
        15: TajweedRule(15, 'مد لازم', 'Madd Lazim', '#B22222', 'مد لازم', 'المدود'),
    }

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.rules = self.DEFAULT_RULES.copy()
        self.custom_colors = {}
        self.apply_custom_config()

    def apply_custom_config(self):
        """تطبيق إعدادات مخصصة"""
        if 'custom_colors' in self.config:
            for rule_id, color in self.config['custom_colors'].items():
                if rule_id in self.rules:
                    self.rules[rule_id].color = color
                    self.custom_colors[rule_id] = color

    def convert_to_html(self, text: str, show_tooltips: bool = True,
                       font_family: str = "Traditional Arabic",
                       font_size: int = 18,
                       highlight_rule: Optional[int] = None) -> str:
        """
        تحويل النص من رموز التجويد الرقمية إلى HTML ملون

        Args:
            text: النص القرآني مع رموز التجويد <number>text</number>
            show_tooltips: إظهار تلميحات الأحكام عند التمرير
            font_family: نوع الخط
            font_size: حجم الخط
            highlight_rule: تمييز حكم معين (اختياري)

        Returns:
            HTML منسق مع الألوان
        """
        if not text:
            return ""

        result = text

        # نمط XML: <number>text</number>
        # مثال: <1>ٱ</1> أو <12>نّ</12>
        pattern = r'<(\d+)>([^<]+?)</\1>'

        def replace_match(match):
            """استبدال كل match بنص ملون"""
            number = int(match.group(1))
            content = match.group(2)

            if number in self.rules:
                rule = self.rules[number]
                color = rule.color

                # تمييز خاص إذا كان هذا الحكم مطلوب
                extra_style = ""
                if highlight_rule and number == highlight_rule:
                    extra_style = "background-color: #FFEB3B; padding: 2px 4px; border-radius: 3px;"

                tooltip = f'title="{rule.name} - {rule.description}"' if show_tooltips else ''

                return f'<span style="color: {color}; font-weight: bold; {extra_style}" {tooltip}>{content}</span>'
            else:
                # رقم غير معروف، أرجع النص بدون تلوين
                return content

        # استبدال جميع الأنماط
        result = re.sub(pattern, replace_match, result)

        # تغليف في div مع خصائص الخط
        html = f"""
        <div style='font-family: "{font_family}", "Traditional Arabic", "Arial";
                    font-size: {font_size}px;
                    line-height: 2.5;
                    direction: rtl;
                    text-align: justify;
                    padding: 15px;'>
            {result}
        </div>
        """

        return html

    def convert_to_plain_text(self, text: str) -> str:
        """إزالة رموز التجويد والحصول على النص النظيف"""
        if not text:
            return ""

        # إزالة الأنماط <number>text</number>
        clean_text = re.sub(r'<(\d+)>([^<]+?)</\1>', r'\2', text)

        # إزالة أي رموز متبقية
        clean_text = re.sub(r'</?[#$@|~%^o*+\d]+>', '', clean_text)

        return clean_text

    def search_by_rule(self, text: str, rule_id: int) -> List[Tuple[int, int, str]]:
        """
        البحث عن كل الكلمات التي تحتوي على حكم تجويدي معين

        Args:
            text: النص القرآني
            rule_id: رقم الحكم التجويدي

        Returns:
            قائمة بـ (start_pos, end_pos, matched_text)
        """
        if not text or rule_id not in self.rules:
            return []

        results = []
        pattern = f'<{rule_id}>([^<]+?)</{rule_id}>'

        for match in re.finditer(pattern, text):
            start = match.start()
            end = match.end()
            content = match.group(1)
            results.append((start, end, content))

        return results

    def get_tajweed_statistics(self, text: str) -> Dict[int, int]:
        """
        حساب إحصائيات أحكام التجويد في النص

        Returns:
            قاموس {rule_id: count}
        """
        stats = {rule_id: 0 for rule_id in self.rules.keys()}

        if not text:
            return stats

        # عد كل حكم
        for rule_id in self.rules.keys():
            pattern = f'<{rule_id}>([^<]+?)</{rule_id}>'
            matches = re.findall(pattern, text)
            stats[rule_id] = len(matches)

        return stats

    def format_statistics_html(self, stats: Dict[int, int]) -> str:
        """تنسيق الإحصائيات بصيغة HTML جميلة"""
        total = sum(stats.values())

        html = f"""
        <div style='direction: rtl; padding: 20px; font-family: "Traditional Arabic", Arial;'>
            <h2 style='color: #1e3c72; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px;'>
                📊 إحصائيات أحكام التجويد
            </h2>
            <p><strong>إجمالي الأحكام:</strong> {total}</p>
            <table style='width: 100%; border-collapse: collapse; margin-top: 20px;'>
                <tr style='background-color: #f5f5f5; font-weight: bold;'>
                    <th style='padding: 10px; border: 1px solid #ddd; text-align: right;'>الحكم</th>
                    <th style='padding: 10px; border: 1px solid #ddd; text-align: center;'>اللون</th>
                    <th style='padding: 10px; border: 1px solid #ddd; text-align: center;'>العدد</th>
                    <th style='padding: 10px; border: 1px solid #ddd; text-align: center;'>النسبة</th>
                </tr>
        """

        for rule_id in sorted(self.rules.keys()):
            rule = self.rules[rule_id]
            count = stats.get(rule_id, 0)
            percentage = (count / total * 100) if total > 0 else 0

            if count > 0:  # عرض الأحكام الموجودة فقط
                html += f"""
                <tr>
                    <td style='padding: 10px; border: 1px solid #ddd;'>{rule.name}</td>
                    <td style='padding: 10px; border: 1px solid #ddd; text-align: center;'>
                        <span style='display: inline-block; width: 60px; height: 20px;
                                     background-color: {rule.color}; border-radius: 4px;'></span>
                    </td>
                    <td style='padding: 10px; border: 1px solid #ddd; text-align: center;
                               font-weight: bold;'>{count}</td>
                    <td style='padding: 10px; border: 1px solid #ddd; text-align: center;'>
                        {percentage:.1f}%
                    </td>
                </tr>
                """

        html += """
            </table>
        </div>
        """

        return html

    def get_color_legend_html(self) -> str:
        """الحصول على مفتاح الألوان HTML"""
        html = """
        <div style='direction: rtl; padding: 15px; font-family: "Traditional Arabic", Arial;
                    background-color: #f9f9f9; border-radius: 8px; margin: 10px 0;'>
            <h4 style='margin: 0 0 10px 0; color: #1e3c72;'>🎨 مفتاح ألوان التجويد:</h4>
            <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
        """

        for rule_id in sorted(self.rules.keys()):
            rule = self.rules[rule_id]
            html += f"""
                <span style='padding: 5px 12px; border-radius: 6px; font-size: 12px;
                             background-color: white; border: 2px solid {rule.color};'>
                    <span style='color: {rule.color}; font-weight: bold;'>⬛</span> {rule.name}
                </span>
            """

        html += """
            </div>
        </div>
        """

        return html

    def extract_words_by_rule(self, text: str, rule_id: int) -> List[str]:
        """استخراج كل الكلمات المحتوية على حكم معين"""
        words = []
        pattern = f'<{rule_id}>([^<]+?)</{rule_id}>'

        for match in re.finditer(pattern, text):
            words.append(match.group(1))

        return words

    def highlight_rule(self, text: str, rule_id: int,
                      highlight_color: str = "#FFEB3B") -> str:
        """تمييز حكم تجويدي معين بلون خلفية"""
        if not text or rule_id not in self.rules:
            return text

        rule = self.rules[rule_id]
        pattern = f'<{rule_id}>([^<]+?)</{rule_id}>'

        def replace_with_highlight(match):
            content = match.group(1)
            return f'<span style="background-color: {highlight_color}; color: {rule.color}; font-weight: bold; padding: 2px 4px; border-radius: 3px; border: 2px solid {rule.color};">{content}</span>'

        result = re.sub(pattern, replace_with_highlight, text)
        return result

    def get_rule_info(self, rule_id: int) -> Optional[TajweedRule]:
        """الحصول على معلومات حكم تجويدي"""
        return self.rules.get(rule_id)

    def get_all_rules(self) -> Dict[int, TajweedRule]:
        """الحصول على كل الأحكام"""
        return self.rules.copy()

    def set_custom_color(self, rule_id: int, color: str):
        """تخصيص لون حكم معين"""
        if rule_id in self.rules:
            self.rules[rule_id].color = color
            self.custom_colors[rule_id] = color

    def reset_colors(self):
        """إعادة تعيين الألوان الافتراضية"""
        self.rules = self.DEFAULT_RULES.copy()
        self.custom_colors = {}

    def export_config(self) -> Dict:
        """تصدير الإعدادات الحالية"""
        return {
            'custom_colors': self.custom_colors,
            'rules': {
                rule_id: {
                    'name': rule.name,
                    'color': rule.color,
                    'description': rule.description
                }
                for rule_id, rule in self.rules.items()
            }
        }

    def import_config(self, config: Dict):
        """استيراد إعدادات"""
        if 'custom_colors' in config:
            for rule_id, color in config['custom_colors'].items():
                self.set_custom_color(int(rule_id), color)

    def get_recommended_fonts(self) -> List[str]:
        """الحصول على قائمة الخطوط الموصى بها لعرض التجويد"""
        return [
            "Traditional Arabic",
            "Arial",
            "Tahoma",
            "Segoe UI",
            "DejaVu Sans",
            "Noto Naskh Arabic",
            "Amiri",
            "Scheherazade New"
        ]

    def format_ayah_with_tajweed(self, ayah_text: str, surah_name: str = "",
                                 ayah_number: int = 0,
                                 show_legend: bool = True) -> str:
        """
        تنسيق آية كاملة مع التجويد والمعلومات

        Returns:
            HTML كامل جاهز للعرض
        """
        # تحويل النص إلى HTML ملون
        colored_html = self.convert_to_html(ayah_text)

        # معلومات الآية
        header = ""
        if surah_name or ayah_number:
            header = f"""
            <div style='text-align: center; padding: 15px;
                        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                        color: white; border-radius: 8px; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{surah_name} - الآية {ayah_number}</h3>
            </div>
            """

        # مفتاح الألوان
        legend = self.get_color_legend_html() if show_legend else ""

        # تجميع HTML
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Traditional Arabic', Arial, sans-serif;
                    background-color: white;
                    padding: 20px;
                    direction: rtl;
                }}
            </style>
        </head>
        <body>
            {header}
            {colored_html}
            {legend}
        </body>
        </html>
        """

        return html
