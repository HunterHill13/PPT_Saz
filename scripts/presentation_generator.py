#!/usr/bin/env python3
"""
PPT_Saz - Native PowerPoint Presentation Generator Orchestrator (v2.0 Slidesgo Grade)
Takes structured slide content (text, layout, images, animations) and produces
a native, editable PowerPoint (.pptx) presentation with full animations, transitions,
vector icons, Slidesgo-grade creative geometry, and native Yekan Bakh typography.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure scripts dir is on sys.path
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio
from icon_mapper import get_icon_svg_content
from image_pipeline import fetch_or_create_placeholder

configure_utf8_stdio()


def is_persian(text: str) -> bool:
    """Check if the text contains Persian/Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def to_persian_digits(num: int | str) -> str:
    """Convert English digits to Persian digits."""
    s = str(num)
    fa_digits = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    return "".join(fa_digits.get(ch, ch) for ch in s)


def load_themes() -> Dict[str, Any]:
    """Load theme definitions from presets/themes.json."""
    theme_file = _SCRIPTS_DIR.parent / "presets" / "themes.json"
    if not theme_file.exists():
        theme_file = _SCRIPTS_DIR / "themes.json"
    if theme_file.exists():
        with open(theme_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "corporate_blue": {
            "name": "Corporate Blue",
            "background": "#0B132B",
            "surface": "#1C2541",
            "surface_border": "#3A506B",
            "primary": "#48CAE4",
            "secondary": "#00B4D8",
            "accent": "#F59E0B",
            "text_main": "#F8FAFC",
            "text_muted": "#94A3B8",
            "badge_bg": "#16294a",
            "font_fa": "Yekan Bakh, Vazirmatn, Tahoma, Arial",
            "font_en": "Segoe UI, Inter, sans-serif"
        }
    }


def escape_xml(s: str) -> str:
    """Escape XML special characters."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


class SlideRenderer:
    def __init__(self, theme: Dict[str, Any], width: int = 1920, height: int = 1080):
        self.theme = theme
        self.width = width
        self.height = height

    def _header_svg(self, is_rtl: bool) -> str:
        lang = "fa" if is_rtl else "en"
        # Generate ambient geometric decorations (dot matrix + subtle accents)
        dots = []
        dot_x_base = 60 if is_rtl else 1760
        for r in range(4):
            for c in range(6):
                dx = dot_x_base + (c * 24)
                dy = 80 + (r * 24)
                dots.append(f'<circle cx="{dx}" cy="{dy}" r="3" fill="{self.theme["primary"]}" fill-opacity="0.18" />')
        dots_svg = "\n".join(dots)

        # Subtle floating ambient glow ring in corner
        glow_x = 1820 if is_rtl else 100
        glow_ring = f'<circle cx="{glow_x}" cy="1000" r="320" fill="none" stroke="{self.theme["primary"]}" stroke-width="1.5" stroke-opacity="0.12" stroke-dasharray="8 6" />'

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" lang="{lang}">
<!-- Background Base -->
<rect width="{self.width}" height="{self.height}" fill="{self.theme['background']}" />
<!-- Ambient Decorative Elements -->
<g id="decor_bg" opacity="0.8">
    {dots_svg}
    {glow_ring}
</g>
"""

    def render_title_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Archetype 1: Hero Cover with category chip, Yekan Bakh typography & framing."""
        title = slide.get("title", "عنوان ارائه")
        subtitle = slide.get("subtitle", "")
        author = slide.get("author", "")
        kicker = slide.get("kicker", "ارائه تخصصی")
        rtl = is_persian(title) or is_persian(subtitle)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        x_pos = 1720 if rtl else 160

        svg = [self._header_svg(rtl)]

        # Category / Pill Chip on top
        svg.append('<g id="kicker_pill">')
        pill_w = max(180, len(kicker) * 18)
        pill_x = (x_pos - pill_w) if rtl else x_pos
        svg.append(f'<rect x="{pill_x}" y="240" width="{pill_w}" height="44" rx="22" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="1.5" />')
        chip_tx = (pill_x + pill_w / 2)
        svg.append(f'<text x="{chip_tx}" y="269" font-family="{font}" font-size="18" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
        svg.append('</g>')

        # Title & Subtitle Group
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{x_pos}" y="380" font-family="{font}" font-size="64" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        if subtitle:
            svg.append(f'<text x="{x_pos}" y="470" font-family="{font}" font-size="28" font-weight="600" fill="{self.theme["secondary"]}" text-anchor="{align}">{escape_xml(subtitle)}</text>')
        svg.append('</g>')

        # Accent Bar
        svg.append('<g id="accent_bar">')
        bar_x = (x_pos + 20) if rtl else (x_pos - 25)
        svg.append(f'<rect x="{bar_x}" y="325" width="8" height="150" fill="{self.theme["primary"]}" rx="4" />')
        svg.append('</g>')

        # Presenter Card Pill
        if author:
            svg.append('<g id="author_chip">')
            auth_w = max(260, len(author) * 16)
            auth_x = (x_pos - auth_w) if rtl else x_pos
            svg.append(f'<rect x="{auth_x}" y="570" width="{auth_w}" height="56" rx="16" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="1.5" />')
            # User Icon
            icon_x = (auth_x + auth_w - 44) if rtl else (auth_x + 14)
            svg.append(get_icon_svg_content("user", icon_x, 584, size=26, stroke_color=self.theme["primary"]))
            auth_tx = (auth_x + auth_w - 60) if rtl else (auth_x + 50)
            svg.append(f'<text x="{auth_tx}" y="605" font-family="{font}" font-size="20" font-weight="500" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(author)}</text>')
            svg.append('</g>')

        # Hero Image Frame
        if image_rel_path:
            svg.append('<g id="hero_image">')
            img_x = 120 if rtl else 1050
            svg.append(f'<rect x="{img_x}" y="200" width="750" height="660" rx="32" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
            svg.append(f'<image href="{image_rel_path}" x="{img_x+12}" y="212" width="726" height="636" preserveAspectRatio="xMidYMid slice" />')
            # Floating Badge on Image
            svg.append(f'<rect x="{img_x+40}" y="780" width="220" height="50" rx="25" fill="{self.theme["background"]}" fill-opacity="0.9" stroke="{self.theme["secondary"]}" stroke-width="1.5" />')
            svg.append(f'<text x="{img_x+150}" y="812" font-family="{font}" font-size="18" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">✦ هوش مصنوعی ۲۰۲۶</text>')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_content_cards_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Archetype 2: Modern Icon Cards with badges and compact chunks."""
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "ارکان کلیدی")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        title_x = 1800 if rtl else 120
        align = "end" if rtl else "start"

        svg = [self._header_svg(rtl)]

        # Top Header & Kicker
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="110" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="170" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        # Cards Layout (2, 3 or 4 cards)
        count = max(1, len(cards))
        margin = 120
        gap = 40
        card_y = 240
        card_h = 690
        total_w = self.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count

        for i, card in enumerate(cards):
            c_title = card.get("title", f"مورد {i+1}")
            c_desc = card.get("desc", "")
            icon_key = card.get("icon", c_title)

            if rtl:
                c_x = (self.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="card_{i+1}">')
            # Card Container with subtle gradient border effect
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="24" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')

            # Icon Container Badge (Rounded squircle with 15% opacity tint)
            badge_size = 72
            bx = (c_x + card_w - 40 - badge_size) if rtl else (c_x + 40)
            by = card_y + 40
            svg.append(f'<rect x="{bx}" y="{by}" width="{badge_size}" height="{badge_size}" rx="20" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
            
            # Embed Vector SVG Icon!
            icon_offset = (badge_size - 40) / 2
            svg.append(get_icon_svg_content(icon_key, bx + icon_offset, by + icon_offset, size=40, stroke_color=self.theme["primary"]))

            # Step / Index Tag
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            tag_x = (c_x + 40) if rtl else (c_x + card_w - 40)
            tag_align = "start" if rtl else "end"
            svg.append(f'<text x="{tag_x}" y="{by + 46}" font-family="{font}" font-size="32" font-weight="700" fill="{self.theme["surface_border"]}" text-anchor="{tag_align}">{num_str}</text>')

            # Card Title
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            svg.append(f'<text x="{tx}" y="{card_y + 175}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(c_title)}</text>')

            # Card Description Bullet Lines
            desc_lines = c_desc.split("\n")
            curr_y = card_y + 240
            for line in desc_lines[:6]:
                if line.strip():
                    # Bullet Chip Dot
                    b_dot_x = (tx - 8) if rtl else (tx + 8)
                    t_pos_x = (tx - 28) if rtl else (tx + 28)
                    svg.append(f'<circle cx="{b_dot_x}" cy="{curr_y-7}" r="5" fill="{self.theme["secondary"]}" />')
                    svg.append(f'<text x="{t_pos_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(line.strip())}</text>')
                    curr_y += 46
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_process_steps_slide(self, slide: Dict[str, Any]) -> str:
        """Slidesgo Archetype 3: Horizontal Connected Process / Roadmap."""
        title = slide.get("title", "فرآیند پیاده‌سازی")
        kicker = slide.get("kicker", "نقشه راه گام‌به‌گام")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        title_x = 1800 if rtl else 120
        align = "end" if rtl else "start"

        svg = [self._header_svg(rtl)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="110" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="170" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 120
        gap = 40
        step_w = (self.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 300
        card_h = 580

        # Horizontal Connecting Line
        line_y = card_y - 40
        svg.append(f'<line x1="{margin + 50}" y1="{line_y}" x2="{self.width - margin - 50}" y2="{line_y}" stroke="{self.theme["surface_border"]}" stroke-width="4" stroke-dasharray="10 8" />')

        for i, step in enumerate(steps):
            s_title = step.get("title", f"مرحله {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            if rtl:
                s_x = (self.width - margin) - ((i + 1) * step_w) - (i * gap)
            else:
                s_x = margin + (i * (step_w + gap))

            center_x = s_x + (step_w / 2)

            svg.append(f'<g id="step_{i+1}">')
            # Step Node Circle on Connecting Line
            svg.append(f'<circle cx="{center_x}" cy="{line_y}" r="28" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            step_num = to_persian_digits(i + 1) if rtl else str(i + 1)
            svg.append(f'<text x="{center_x}" y="{line_y + 9}" font-family="{font}" font-size="22" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{step_num}</text>')

            # Step Card
            svg.append(f'<rect x="{s_x}" y="{card_y}" width="{step_w}" height="{card_h}" rx="24" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')

            # Icon Centered
            icon_box_size = 64
            ibx = center_x - (icon_box_size / 2)
            iby = card_y + 36
            svg.append(f'<rect x="{ibx}" y="{iby}" width="{icon_box_size}" height="{icon_box_size}" rx="18" fill="{self.theme["badge_bg"]}" stroke="{self.theme["secondary"]}" stroke-width="1.5" />')
            svg.append(get_icon_svg_content(icon_key, ibx + 14, iby + 14, size=36, stroke_color=self.theme["secondary"]))

            # Title
            svg.append(f'<text x="{center_x}" y="{card_y + 160}" font-family="{font}" font-size="26" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')

            # Description (wrapped)
            desc_lines = s_desc.split("\n")
            curr_y = card_y + 220
            tx = (s_x + step_w - 36) if rtl else (s_x + 36)
            for line in desc_lines[:6]:
                if line.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(line.strip())}</text>')
                    curr_y += 38
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_stats_kpi_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Archetype 4: Big Bold Numbers & Stats KPIs."""
        title = slide.get("title", "شاخص‌های کلیدی عملکرد")
        kicker = slide.get("kicker", "آمار و تاثیر")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="110" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="170" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        # If Image present, split layout; otherwise 3 big cards
        has_image = bool(image_rel_path)
        kpi_count = len(kpis)

        if has_image:
            img_w = 680
            img_h = 690
            img_x = 120 if rtl else 1120
            img_y = 240
            svg.append('<g id="kpi_image">')
            svg.append(f'<rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
            svg.append(f'<image href="{image_rel_path}" x="{img_x+10}" y="{img_y+10}" width="{img_w-20}" height="{img_h-20}" preserveAspectRatio="xMidYMid slice" />')
            svg.append('</g>')

            # KPI stack on the other side
            stack_x = 840 if rtl else 120
            stack_w = 960
            kpi_h = (690 - ((kpi_count - 1) * 30)) / max(1, kpi_count)

            for i, kpi in enumerate(kpis):
                ky = 240 + (i * (kpi_h + 30))
                num_val = kpi.get("number", kpi.get("val", "+85%"))
                k_label = kpi.get("title", kpi.get("label", ""))
                k_desc = kpi.get("desc", "")
                trend = kpi.get("trend", "↑ رشد شاخص")

                svg.append(f'<g id="kpi_{i+1}">')
                svg.append(f'<rect x="{stack_x}" y="{ky}" width="{stack_w}" height="{kpi_h}" rx="24" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
                
                # Big Stat Number in Yekan Bakh Bold
                num_tx = (stack_x + stack_w - 50) if rtl else (stack_x + 50)
                num_align = "end" if rtl else "start"
                svg.append(f'<text x="{num_tx}" y="{ky + 80}" font-family="{font}" font-size="64" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{num_align}">{escape_xml(num_val)}</text>')

                # Trend Pill
                pill_x = (stack_x + 50) if rtl else (stack_x + stack_w - 200)
                svg.append(f'<rect x="{pill_x}" y="{ky + 35}" width="160" height="38" rx="19" fill="{self.theme["badge_bg"]}" stroke="{self.theme["accent"]}" stroke-width="1.5" />')
                svg.append(f'<text x="{pill_x + 80}" y="{ky + 60}" font-family="{font}" font-size="16" font-weight="700" fill="{self.theme["accent"]}" text-anchor="middle">{escape_xml(trend)}</text>')

                # Label & Desc
                svg.append(f'<text x="{num_tx}" y="{ky + 130}" font-family="{font}" font-size="24" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{num_align}">{escape_xml(k_label)}</text>')
                if k_desc:
                    svg.append(f'<text x="{num_tx}" y="{ky + 165}" font-family="{font}" font-size="18" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{num_align}">{escape_xml(k_desc)}</text>')
                svg.append('</g>')
        else:
            # 3 horizontal KPI cards
            card_w = (1920 - 240 - ((kpi_count - 1) * 40)) / max(1, kpi_count)
            for i, kpi in enumerate(kpis):
                kx = 120 + (i * (card_w + 40))
                num_val = kpi.get("number", kpi.get("val", "+85%"))
                k_label = kpi.get("title", kpi.get("label", ""))
                k_desc = kpi.get("desc", "")

                svg.append(f'<g id="kpi_{i+1}">')
                svg.append(f'<rect x="{kx}" y="260" width="{card_w}" height="650" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
                center_kx = kx + (card_w / 2)
                svg.append(f'<text x="{center_kx}" y="420" font-family="{font}" font-size="76" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')
                svg.append(f'<text x="{center_kx}" y="500" font-family="{font}" font-size="30" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')
                if k_desc:
                    svg.append(f'<text x="{center_kx}" y="560" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="middle">{escape_xml(k_desc)}</text>')
                svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_comparison_slide(self, slide: Dict[str, Any]) -> str:
        """Slidesgo Archetype 5: Versus / Comparison Matrix."""
        title = slide.get("title", "مقایسه رویکرد سنتی و مدرن")
        kicker = slide.get("kicker", "تحلیل تطبیقی")
        col_a = slide.get("col_a", {"title": "روش‌های سنتی", "items": ["سرعت کند پردازش", "خطای انسانی بالا", "هزینه‌های نگهداری سنگین"]})
        col_b = slide.get("col_b", {"title": "راهکار هوش مصنوعی", "items": ["پردازش بلادرنگ و سریع", "دقت ۹۹.۲ درصدی", "کاهش ۶۰٪ هزینه‌ها"]})
        rtl = is_persian(title) or is_persian(col_a.get("title", ""))

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="110" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="170" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 800
        card_h = 680
        ca_x = 980 if rtl else 120
        cb_x = 140 if rtl else 1000
        card_y = 250

        # Column A (Muted / Traditional)
        svg.append('<g id="compare_col_a">')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
        # Header Badge
        svg.append(f'<rect x="{ca_x+40}" y="{card_y+40}" width="240" height="52" rx="26" fill="{self.theme["background"]}" stroke="{self.theme["text_muted"]}" stroke-width="1.5" />')
        svg.append(f'<text x="{ca_x+160}" y="{card_y+74}" font-family="{font}" font-size="22" font-weight="700" fill="{self.theme["text_muted"]}" text-anchor="middle">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        # Items with cross/minus icon
        curr_y = card_y + 160
        tx = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(get_icon_svg_content("circle-x", (tx - 36) if rtl else (tx), curr_y - 20, size=24, stroke_color="#EF4444"))
            item_tx = (tx - 50) if rtl else (tx + 36)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        # Column B (Vibrant / AI Powered)
        svg.append('<g id="compare_col_b">')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
        # Header Badge
        svg.append(f'<rect x="{cb_x+40}" y="{card_y+40}" width="280" height="52" rx="26" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
        svg.append(f'<text x="{cb_x+180}" y="{card_y+74}" font-family="{font}" font-size="22" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">✦ {escape_xml(col_b.get("title", "هوشمند"))}</text>')
        # Items with checkmark icon
        curr_y = card_y + 160
        tx = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(get_icon_svg_content("circle-check", (tx - 36) if rtl else (tx), curr_y - 20, size=24, stroke_color=self.theme["primary"]))
            item_tx = (tx - 50) if rtl else (tx + 36)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_split_image_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Archetype 6: Split Feature Showcase with Icon Bullets."""
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "بررسی تخصصی")
        bullets = slide.get("bullets", [])
        rtl = is_persian(title) or any(is_persian(str(b)) for b in bullets)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        text_x = 1800 if rtl else 120
        image_x = 120 if rtl else 1020
        image_y = 220
        image_w = 780
        image_h = 720

        svg = [self._header_svg(rtl)]

        # Header & Text
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{text_x}" y="110" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{text_x}" y="170" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        svg.append('<g id="bullets_group">')
        tx = text_x
        curr_y = 280
        for i, bullet in enumerate(bullets):
            svg.append(f'<g id="bullet_{i+1}">')
            # Checkmark badge icon
            icon_x = (tx - 36) if rtl else tx
            svg.append(get_icon_svg_content("rosette-check", icon_x, curr_y - 20, size=28, stroke_color=self.theme["secondary"]))
            text_pos_x = (tx - 50) if rtl else (tx + 46)
            svg.append(f'<text x="{text_pos_x}" y="{curr_y}" font-family="{font}" font-size="24" font-weight="400" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(bullet)}</text>')
            svg.append('</g>')
            curr_y += 75
        svg.append('</g>')

        # Image Container with modern frame
        svg.append('<g id="hero_image">')
        svg.append(f'<rect x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
        if image_rel_path:
            svg.append(f'<image href="{image_rel_path}" x="{image_x+10}" y="{image_y+10}" width="{image_w-20}" height="{image_h-20}" preserveAspectRatio="xMidYMid slice" />')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


def generate_presentation_project(
    deck_data: Dict[str, Any],
    project_dir: Path,
    output_pptx: Optional[Path] = None,
    theme_key: str = "corporate_blue",
    transition: str = "fade",
    animation_mode: str = "auto"
) -> Path:
    """
    Generate complete SVG deck, notes, and compile to native PPTX.
    """
    themes = load_themes()
    theme = themes.get(theme_key, list(themes.values())[0])
    renderer = SlideRenderer(theme=theme)

    project_dir = project_dir.resolve()
    svg_dir = project_dir / "svg_output"
    notes_dir = project_dir / "notes"
    images_dir = project_dir / "images"
    exports_dir = project_dir / "exports"

    svg_dir.mkdir(parents=True, exist_ok=True)
    notes_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)

    slides = deck_data.get("slides", [])
    if not slides:
        raise ValueError("No slides found in deck data!")

    print(f"Creating Slidesgo-grade presentation with {len(slides)} slides...")

    for idx, slide in enumerate(slides, start=1):
        slide_stem = f"{idx:02d}_{slide.get('slug', f'slide_{idx}')}"
        layout = slide.get("layout", "content_cards")
        
        # Sourcing Image
        img_filename = f"img_{idx:02d}.jpg"
        img_rel_for_svg = f"../images/{img_filename}"
        img_query = slide.get("image_query", slide.get("image_prompt", slide.get("title", "presentation")))
        
        # Render appropriate layout
        if layout == "title_hero" or idx == 1:
            img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))
            svg_content = renderer.render_title_slide(slide, image_rel_path=img_rel_for_svg)
        elif layout == "process_steps":
            svg_content = renderer.render_process_steps_slide(slide)
        elif layout == "stats_kpi":
            img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))
            svg_content = renderer.render_stats_kpi_slide(slide, image_rel_path=img_rel_for_svg)
        elif layout == "comparison":
            svg_content = renderer.render_comparison_slide(slide)
        elif layout == "split_image":
            img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))
            svg_content = renderer.render_split_image_slide(slide, image_rel_path=img_rel_for_svg)
        else: # default content_cards
            svg_content = renderer.render_content_cards_slide(slide, image_rel_path=img_rel_for_svg)

        svg_file = svg_dir / f"{slide_stem}.svg"
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(svg_content)

        # Speaker notes
        notes_content = slide.get("notes", slide.get("title", ""))
        note_file = notes_dir / f"{slide_stem}.md"
        with open(note_file, "w", encoding="utf-8") as f:
            f.write(f"# Notes for Slide {idx}: {slide.get('title', '')}\n\n{notes_content}\n")

    # Destination PPTX path
    if output_pptx is None:
        deck_title = re.sub(r'[^a-zA-Z0-9_\u0600-\u06FF]', '_', deck_data.get("title", "presentation")).strip("_")
        output_pptx = exports_dir / f"{deck_title}.pptx"
    else:
        output_pptx = Path(output_pptx).resolve()

    # Compile using svg_to_pptx.py
    svg_to_pptx_script = _SCRIPTS_DIR / "svg_to_pptx.py"
    cmd = [
        sys.executable,
        str(svg_to_pptx_script),
        str(project_dir),
        "-o", str(output_pptx),
        "-t", transition,
        "-a", animation_mode,
        "--animation-trigger", "after-previous",
        "--animation-stagger", "0.35"
    ]

    print(f"Compiling slides to native PPTX with transitions ({transition}) and animations ({animation_mode})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error compiling PPTX: {res.stderr}", file=sys.stderr)
        raise RuntimeError(f"svg_to_pptx failed: {res.stderr}")

    print(f"Presentation successfully generated: {output_pptx}")
    return output_pptx


def main():
    parser = argparse.ArgumentParser(description="PPT_Saz: Generate native PowerPoint presentations from JSON/Markdown.")
    parser.add_argument("input", help="Path to input JSON file or deck configuration")
    parser.add_argument("-o", "--output", help="Output .pptx path", default=None)
    parser.add_argument("-p", "--project-dir", help="Working project directory", default="./presentation_project")
    parser.add_argument("-t", "--transition", help="Slide transition (fade, push, morph, wipe, zoom)", default="fade")
    parser.add_argument("-a", "--animation", help="Animation mode (auto, mixed, none)", default="auto")
    parser.add_argument("--theme", help="Theme palette name (corporate_blue, modern_dark_indigo, clean_academic, emerald_tech, warm_terracotta)", default="corporate_blue")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out_file = generate_presentation_project(
        deck_data=data,
        project_dir=Path(args.project_dir),
        output_pptx=Path(args.output) if args.output else None,
        theme_key=args.theme,
        transition=args.transition,
        animation_mode=args.animation
    )
    print(f"Done: {out_file}")


if __name__ == "__main__":
    main()
