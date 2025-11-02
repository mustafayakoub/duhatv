#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📺 QuranDisplayComponent - عرض الآيات
Display Component for formatting Quran text
"""

from typing import Dict, List, Any, Optional
import re


class QuranDisplayComponent:
    """مكون عرض وتنسيق الآيات"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.default_font = self.config.get('arabic_font', 'Arial')
        self.default_font_size = self.config.get('font_size', 18)
        self.primary_color = self.config.get('primary_color', '#1e3c72')
        self.secondary_color = self.config.get('secondary_color', '#2a5298')
        self.highlight_color = self.config.get('highlight_color', '#ffeb3b')

    def format_ayah_html(self, ayah: Dict, highlight_terms: List[str] = None) -> str:
        """تنسيق آية بصيغة HTML"""
        text = ayah.get('text', '')
        sura = ayah.get('sura', 0)
        aya_num = ayah.get('aya', 0)

        # تطبيق التظليل إذا وجد
        if highlight_terms:
            for term in highlight_terms:
                # تجاهل التشكيل عند البحث
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                text = pattern.sub(
                    f'<span style="background-color: {self.highlight_color}; font-weight: bold;">{term}</span>',
                    text
                )

        html = f"""
        <div class="ayah" style="
            font-family: '{self.default_font}', 'Traditional Arabic', 'Arial';
            font-size: {self.default_font_size}px;
            line-height: 2.0;
            text-align: right;
            direction: rtl;
            margin: 15px 0;
            padding: 15px;
            border-right: 4px solid {self.primary_color};
            background-color: #f9f9f9;
            border-radius: 8px;
        ">
            <span class="ayah-text" style="color: #212121;">{text}</span>
            <span class="ayah-number" style="
                color: {self.primary_color};
                font-weight: bold;
                margin-right: 10px;
                font-size: {self.default_font_size - 2}px;
            "> ({aya_num}) </span>
        </div>
        """

        return html

    def format_sura_html(self, sura_data: Dict, ayas: List[Dict],
                        show_basmala: bool = True) -> str:
        """تنسيق سورة كاملة بصيغة HTML"""
        sura_name = sura_data.get('name', '')
        sura_num = sura_data.get('sura', 0)
        ayas_count = sura_data.get('ayas_count', 0)
        revelation_type = sura_data.get('type_full', 'مكية')

        # البسملة
        basmala = ""
        if show_basmala and sura_num != 1 and sura_num != 9:  # ليس الفاتحة أو التوبة
            basmala = f"""
            <div class="basmala" style="
                text-align: center;
                font-size: {self.default_font_size + 6}px;
                font-family: '{self.default_font}', 'Traditional Arabic';
                color: {self.primary_color};
                margin: 25px 0;
                font-weight: bold;
            ">
                بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
            </div>
            """

        # رأس السورة
        header = f"""
        <div class="sura-header" style="
            background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h2 style="margin: 0; font-size: {self.default_font_size + 8}px;">
                سورة {sura_name}
            </h2>
            <p style="margin: 10px 0 0 0; font-size: {self.default_font_size - 2}px; opacity: 0.9;">
                {revelation_type} • {ayas_count} آية
            </p>
        </div>
        """

        # الآيات
        ayas_html = "\n".join([self.format_ayah_html(aya) for aya in ayas])

        # تجميع HTML
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: '{self.default_font}', 'Traditional Arabic', 'Arial', sans-serif;
                    background-color: white;
                    padding: 20px;
                    direction: rtl;
                }}
            </style>
        </head>
        <body>
            {header}
            {basmala}
            {ayas_html}
        </body>
        </html>
        """

        return html

    def format_search_results_html(self, results: List[Dict],
                                   query: str = None) -> str:
        """تنسيق نتائج البحث بصيغة HTML"""
        if not results:
            return f"""
            <div style="
                text-align: center;
                padding: 50px;
                color: #999;
                font-size: {self.default_font_size}px;
            ">
                <h3>لا توجد نتائج</h3>
                <p>جرب البحث بكلمات مختلفة</p>
            </div>
            """

        # عنوان النتائج
        header = f"""
        <div style="
            background-color: {self.primary_color};
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        ">
            <h3 style="margin: 0;">نتائج البحث: {len(results)}</h3>
            {f'<p style="margin: 5px 0 0 0;">البحث عن: "{query}"</p>' if query else ''}
        </div>
        """

        # النتائج
        highlight_terms = [query] if query else []
        results_html = "\n".join([
            self.format_ayah_html(result, highlight_terms)
            for result in results
        ])

        html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="
            font-family: '{self.default_font}', 'Traditional Arabic', 'Arial';
            background-color: white;
            padding: 20px;
            direction: rtl;
        ">
            {header}
            {results_html}
        </body>
        </html>
        """

        return html

    def format_plain_text(self, ayah: Dict) -> str:
        """تنسيق آية بصيغة نص عادي"""
        text = ayah.get('text', '')
        sura = ayah.get('sura', 0)
        aya = ayah.get('aya', 0)
        return f"[{sura}:{aya}] {text}"

    def format_sura_plain_text(self, sura_data: Dict, ayas: List[Dict]) -> str:
        """تنسيق سورة كاملة بصيغة نص عادي"""
        lines = []
        lines.append(f"سورة {sura_data.get('name', '')}")
        lines.append("=" * 50)

        for aya in ayas:
            lines.append(self.format_plain_text(aya))

        return "\n".join(lines)

    def remove_tashkeel(self, text: str) -> str:
        """إزالة التشكيل من النص العربي"""
        tashkeel_pattern = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        return tashkeel_pattern.sub('', text)

    def highlight_text(self, text: str, terms: List[str],
                      color: str = None) -> str:
        """تظليل كلمات محددة في النص"""
        if not terms:
            return text

        highlight_color = color or self.highlight_color

        for term in terms:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            text = pattern.sub(
                f'<span style="background-color: {highlight_color}; font-weight: bold;">{term}</span>',
                text
            )

        return text
