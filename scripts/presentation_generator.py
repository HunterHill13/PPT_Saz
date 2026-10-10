#!/usr/bin/env python3
"""
PPT_Saz - Native PowerPoint Presentation Generator Orchestrator (v3.0 Ultra-Graphic & Morph)
Produces rich, non-minimalist presentations with dynamic multi-layer animated backgrounds,
glowing geometry, vector icons, Morph transitions, and strict verbatim text preservation.
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
        "cyber_aurora": {
            "name": "Cyber Aurora",
            "background": "#070B19",
            "surface": "#10182F",
            "surface_border": "#2563EB",
            "surface_glow": "#38BDF8",
            "primary": "#00F0FF",
            "secondary": "#A855F7",
            "accent": "#EC4899",
            "wave_1": "#0E1E45",
            "wave_2": "#1E1B4B",
            "text_main": "#FFFFFF",
            "text_muted": "#CBD5E1",
            "badge_bg": "#132147",
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
    """
    Renders rich, ultra-graphic presentation slides with layered ambient geometry,
    animated background slices, vector icon containers, and Yekan Bakh typography.
    """
    def __init__(self, theme: Dict[str, Any], width: int = 1920, height: int = 1080):
        self.theme = theme
        self.width = width
        self.height = height

    def _header_svg(self, is_rtl: bool, slide_idx: int = 1) -> str:
        lang = "fa" if is_rtl else "en"
        primary = self.theme["primary"]
        secondary = self.theme["secondary"]
        wave_1 = self.theme.get("wave_1", "#0E1E45")
        wave_2 = self.theme.get("wave_2", "#1E1B4B")
        accent = self.theme.get("accent", "#EC4899")

        # Multi-layer dynamic background waves and geometric energy lines
        dots = []
        dot_x_base = 60 if is_rtl else 1700
        for r in range(5):
            for c in range(8):
                dx = dot_x_base + (c * 22)
                dy = 60 + (r * 22)
                dots.append(f'<circle cx="{dx}" cy="{dy}" r="2.5" fill="{primary}" fill-opacity="0.25" />')
        dots_svg = "\n".join(dots)

        # Alternating dynamic wave contours based on slide index
        if slide_idx % 2 == 1:
            wave_path_1 = f'<path d="M0,720 Q480,580 960,760 T1920,680 L1920,1080 L0,1080 Z" fill="{wave_1}" fill-opacity="0.6" />'
            wave_path_2 = f'<path d="M0,840 Q520,740 1080,900 T1920,820 L1920,1080 L0,1080 Z" fill="{wave_2}" fill-opacity="0.85" />'
            glow_line = f'<path d="M0,720 Q480,580 960,760 T1920,680" fill="none" stroke="{primary}" stroke-width="3" stroke-opacity="0.45" />'
        else:
            wave_path_1 = f'<path d="M0,660 Q560,820 1100,640 T1920,740 L1920,1080 L0,1080 Z" fill="{wave_1}" fill-opacity="0.6" />'
            wave_path_2 = f'<path d="M0,800 Q440,920 1020,780 T1920,860 L1920,1080 L0,1080 Z" fill="{wave_2}" fill-opacity="0.85" />'
            glow_line = f'<path d="M0,660 Q560,820 1100,640 T1920,740" fill="none" stroke="{secondary}" stroke-width="3" stroke-opacity="0.45" />'

        # Floating geometric rings and corner accent shapes
        ring_x = 1820 if is_rtl else 100
        ring_y = 960
        ambient_rings = f"""
        <circle cx="{ring_x}" cy="{ring_y}" r="260" fill="none" stroke="{primary}" stroke-width="2" stroke-opacity="0.2" stroke-dasharray="12 8" />
        <circle cx="{ring_x}" cy="{ring_y}" r="180" fill="none" stroke="{secondary}" stroke-width="1.5" stroke-opacity="0.25" />
        <circle cx="{ring_x}" cy="{ring_y}" r="380" fill="none" stroke="{accent}" stroke-width="1" stroke-opacity="0.12" stroke-dasharray="6 14" />
        """

        # Diagonal geometric corner chips
        corner_chip = f"""
        <polygon points="0,0 220,0 0,220" fill="{primary}" fill-opacity="0.08" />
        <polygon points="1920,0 1700,0 1920,220" fill="{secondary}" fill-opacity="0.08" />
        """

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" lang="{lang}">
<!-- Deep Base Background -->
<rect width="{self.width}" height="{self.height}" fill="{self.theme['background']}" />

<!-- Animated Ambient Background Layer 1: Waves & Contour -->
<g id="bg_ambient_waves">
    {wave_path_1}
    {wave_path_2}
    {glow_line}
</g>

<!-- Animated Ambient Background Layer 2: Geometric Accents & Rings -->
<g id="bg_geometric_accents">
    {ambient_rings}
    {corner_chip}
    {dots_svg}
</g>
"""

    def render_title_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Ultra-Poster Cover: glowing category chip, Yekan Bakh typography, author card & framed hero."""
        title = slide.get("title", "عنوان ارائه")
        subtitle = slide.get("subtitle", "")
        author = slide.get("author", "")
        kicker = slide.get("kicker", "ارائه تخصصی")
        rtl = is_persian(title) or is_persian(subtitle)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        x_pos = 1720 if rtl else 140

        svg = [self._header_svg(rtl, slide_idx=1)]

        # Glowing Category / Pill Chip on top
        svg.append('<g id="kicker_pill">')
        pill_w = max(220, len(kicker) * 20)
        pill_x = (x_pos - pill_w) if rtl else x_pos
        svg.append(f'<rect x="{pill_x}" y="220" width="{pill_w}" height="48" rx="24" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
        # Tiny glowing dot inside pill
        dot_in_pill = (pill_x + pill_w - 24) if rtl else (pill_x + 24)
        svg.append(f'<circle cx="{dot_in_pill}" cy="244" r="5" fill="{self.theme["primary"]}" />')
        chip_tx = (pill_x + (pill_w / 2) - 10) if rtl else (pill_x + (pill_w / 2) + 10)
        svg.append(f'<text x="{chip_tx}" y="252" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
        svg.append('</g>')

        # Title & Subtitle Group (Verbatim Text)
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{x_pos}" y="360" font-family="{font}" font-size="64" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        if subtitle:
            # Multi-line subtitle support without truncating
            sub_lines = subtitle.split("\n")
            sy = 450
            for s_line in sub_lines[:3]:
                if s_line.strip():
                    svg.append(f'<text x="{x_pos}" y="{sy}" font-family="{font}" font-size="28" font-weight="600" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(s_line.strip())}</text>')
                    sy += 44
        svg.append('</g>')

        # Radiant Spine Accent Bar
        svg.append('<g id="accent_spine">')
        bar_x = (x_pos + 25) if rtl else (x_pos - 30)
        svg.append(f'<rect x="{bar_x}" y="300" width="10" height="220" fill="{self.theme["primary"]}" rx="5" />')
        svg.append(f'<rect x="{bar_x-3}" y="300" width="16" height="60" fill="{self.theme["secondary"]}" rx="4" />')
        svg.append('</g>')

        # Presenter Card Pill
        if author:
            svg.append('<g id="author_chip">')
            auth_w = max(280, len(author) * 18)
            auth_x = (x_pos - auth_w) if rtl else x_pos
            svg.append(f'<rect x="{auth_x}" y="590" width="{auth_w}" height="64" rx="20" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
            icon_x = (auth_x + auth_w - 48) if rtl else (auth_x + 16)
            svg.append(get_icon_svg_content("user", icon_x, 606, size=30, stroke_color=self.theme["primary"]))
            auth_tx = (auth_x + auth_w - 65) if rtl else (auth_x + 56)
            svg.append(f'<text x="{auth_tx}" y="630" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(author)}</text>')
            svg.append('</g>')

        # Hero Image Showcase Frame with Neon Glow
        if image_rel_path:
            svg.append('<g id="hero_image">')
            img_x = 100 if rtl else 1050
            # Double glowing border frame
            svg.append(f'<rect x="{img_x-8}" y="192" width="766" height="676" rx="36" fill="none" stroke="{self.theme["secondary"]}" stroke-width="2" stroke-opacity="0.4" />')
            svg.append(f'<rect x="{img_x}" y="200" width="750" height="660" rx="32" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            svg.append(f'<image href="{image_rel_path}" x="{img_x+12}" y="212" width="726" height="636" preserveAspectRatio="xMidYMid slice" />')
            # Floating Badge on Image
            svg.append(f'<rect x="{img_x+40}" y="780" width="240" height="52" rx="26" fill="{self.theme["background"]}" fill-opacity="0.92" stroke="{self.theme["primary"]}" stroke-width="2" />')
            svg.append(f'<text x="{img_x+160}" y="813" font-family="{font}" font-size="19" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">✦ ارائه رسمی و تاییدشده</text>')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_content_cards_slide(self, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Slidesgo Multi-Level Feature Cards with illuminated icon squircle badges."""
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "ارکان کلیدی")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        title_x = 1800 if rtl else 120
        align = "end" if rtl else "start"

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(cards))
        margin = 110
        gap = 36
        card_y = 230
        card_h = 710
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
            # Multi-layer card: subtle glow outline + glass surface
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="26" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2.5" />')
            # Top neon accent cap line
            svg.append(f'<rect x="{c_x+30}" y="{card_y}" width="{card_w-60}" height="5" rx="2.5" fill="{self.theme["primary"]}" />')

            # Icon Squircle Badge with concentric aura
            badge_size = 76
            bx = (c_x + card_w - 40 - badge_size) if rtl else (c_x + 40)
            by = card_y + 40
            svg.append(f'<rect x="{bx-4}" y="{by-4}" width="{badge_size+8}" height="{badge_size+8}" rx="24" fill="none" stroke="{self.theme["primary"]}" stroke-width="1.5" stroke-opacity="0.3" stroke-dasharray="6 4" />')
            svg.append(f'<rect x="{bx}" y="{by}" width="{badge_size}" height="{badge_size}" rx="22" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
            
            # Embed Vector Icon
            icon_offset = (badge_size - 44) / 2
            svg.append(get_icon_svg_content(icon_key, bx + icon_offset, by + icon_offset, size=44, stroke_color=self.theme["primary"]))

            # Step / Index Pill
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            tag_x = (c_x + 40) if rtl else (c_x + card_w - 40)
            tag_align = "start" if rtl else "end"
            svg.append(f'<text x="{tag_x}" y="{by + 50}" font-family="{font}" font-size="34" font-weight="700" fill="{self.theme["secondary"]}" fill-opacity="0.4" text-anchor="{tag_align}">{num_str}</text>')

            # Card Title (Verbatim)
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            svg.append(f'<text x="{tx}" y="{card_y + 180}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(c_title)}</text>')

            # Verbatim Text Preservation: split into structured lines without shortening
            desc_lines = c_desc.split("\n")
            curr_y = card_y + 245
            for line in desc_lines[:7]:
                clean_l = line.strip()
                if clean_l:
                    b_dot_x = (tx - 8) if rtl else (tx + 8)
                    t_pos_x = (tx - 30) if rtl else (tx + 30)
                    svg.append(f'<circle cx="{b_dot_x}" cy="{curr_y-7}" r="5" fill="{self.theme["secondary"]}" />')
                    svg.append(f'<text x="{t_pos_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_process_steps_slide(self, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Slidesgo Circuit/Roadmap Process: illuminated connecting pulse line & milestone cards."""
        title = slide.get("title", "فرآیند پیاده‌سازی")
        kicker = slide.get("kicker", "نقشه راه گام‌به‌گام")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        title_x = 1800 if rtl else 120
        align = "end" if rtl else "start"

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 110
        gap = 36
        step_w = (self.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 310
        card_h = 610
        line_y = card_y - 50

        # Glowing Pulse Connector Line
        svg.append(f'<line x1="{margin + 60}" y1="{line_y}" x2="{self.width - margin - 60}" y2="{line_y}" stroke="{self.theme["surface_border"]}" stroke-width="5" stroke-dasharray="12 8" />')
        svg.append(f'<line x1="{margin + 60}" y1="{line_y}" x2="{self.width - margin - 60}" y2="{line_y}" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.8" />')

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
            # Glowing Node on pulse line
            svg.append(f'<circle cx="{center_x}" cy="{line_y}" r="34" fill="{self.theme["background"]}" stroke="{self.theme["primary"]}" stroke-width="3.5" />')
            svg.append(f'<circle cx="{center_x}" cy="{line_y}" r="42" fill="none" stroke="{self.theme["primary"]}" stroke-width="1.5" stroke-opacity="0.35" stroke-dasharray="4 4" />')
            step_num = to_persian_digits(i + 1) if rtl else str(i + 1)
            svg.append(f'<text x="{center_x}" y="{line_y + 10}" font-family="{font}" font-size="24" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{step_num}</text>')

            # Stage Milestone Card
            svg.append(f'<rect x="{s_x}" y="{card_y}" width="{step_w}" height="{card_h}" rx="26" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')

            # Icon Box
            icon_box_size = 68
            ibx = center_x - (icon_box_size / 2)
            iby = card_y + 40
            svg.append(f'<rect x="{ibx}" y="{iby}" width="{icon_box_size}" height="{icon_box_size}" rx="20" fill="{self.theme["badge_bg"]}" stroke="{self.theme["secondary"]}" stroke-width="2" />')
            svg.append(get_icon_svg_content(icon_key, ibx + 14, iby + 14, size=40, stroke_color=self.theme["secondary"]))

            # Title (Verbatim)
            svg.append(f'<text x="{center_x}" y="{card_y + 175}" font-family="{font}" font-size="26" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')

            # Verbatim Description Lines
            desc_lines = s_desc.split("\n")
            curr_y = card_y + 240
            tx = (s_x + step_w - 36) if rtl else (s_x + 36)
            for line in desc_lines[:6]:
                clean_l = line.strip()
                if clean_l:
                    b_dot = (tx - 6) if rtl else (tx + 6)
                    t_pos = (tx - 26) if rtl else (tx + 26)
                    svg.append(f'<circle cx="{b_dot}" cy="{curr_y-6}" r="4" fill="{self.theme["primary"]}" />')
                    svg.append(f'<text x="{t_pos}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 42
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_stats_kpi_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None, slide_idx: int = 4) -> str:
        """Slidesgo Big KPI Numerals with radiating auras, trend chips & contextual layout."""
        title = slide.get("title", "شاخص‌های کلیدی عملکرد")
        kicker = slide.get("kicker", "آمار و تاثیر")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        has_image = bool(image_rel_path)
        kpi_count = len(kpis)

        if has_image:
            img_w = 680
            img_h = 700
            img_x = 110 if rtl else 1130
            img_y = 230
            svg.append('<g id="kpi_image">')
            svg.append(f'<rect x="{img_x-6}" y="{img_y-6}" width="{img_w+12}" height="{img_h+12}" rx="32" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.35" />')
            svg.append(f'<rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
            svg.append(f'<image href="{image_rel_path}" x="{img_x+10}" y="{img_y+10}" width="{img_w-20}" height="{img_h-20}" preserveAspectRatio="xMidYMid slice" />')
            svg.append('</g>')

            stack_x = 840 if rtl else 110
            stack_w = 970
            kpi_h = (700 - ((kpi_count - 1) * 32)) / max(1, kpi_count)

            for i, kpi in enumerate(kpis):
                ky = 230 + (i * (kpi_h + 32))
                num_val = kpi.get("number", kpi.get("val", "+85%"))
                k_label = kpi.get("title", kpi.get("label", ""))
                k_desc = kpi.get("desc", "")
                trend = kpi.get("trend", "↑ رشد شاخص")

                svg.append(f'<g id="kpi_{i+1}">')
                # Glass card container
                svg.append(f'<rect x="{stack_x}" y="{ky}" width="{stack_w}" height="{kpi_h}" rx="26" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
                # Glow accent edge
                svg.append(f'<rect x="{stack_x}" y="{ky}" width="8" height="{kpi_h}" rx="4" fill="{self.theme["primary"]}" />')

                # Massive KPI Numeral
                num_tx = (stack_x + stack_w - 60) if rtl else (stack_x + 60)
                num_align = "end" if rtl else "start"
                svg.append(f'<text x="{num_tx}" y="{ky + 85}" font-family="{font}" font-size="70" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{num_align}">{escape_xml(num_val)}</text>')

                # Trend Pill Badge
                pill_x = (stack_x + 50) if rtl else (stack_x + stack_w - 210)
                svg.append(f'<rect x="{pill_x}" y="{ky + 40}" width="170" height="42" rx="21" fill="{self.theme["badge_bg"]}" stroke="{self.theme["accent"]}" stroke-width="2" />')
                svg.append(f'<text x="{pill_x + 85}" y="{ky + 67}" font-family="{font}" font-size="17" font-weight="700" fill="{self.theme["accent"]}" text-anchor="middle">{escape_xml(trend)}</text>')

                # Label & Verbatim Desc
                svg.append(f'<text x="{num_tx}" y="{ky + 140}" font-family="{font}" font-size="26" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{num_align}">{escape_xml(k_label)}</text>')
                if k_desc:
                    svg.append(f'<text x="{num_tx}" y="{ky + 178}" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{num_align}">{escape_xml(k_desc)}</text>')
                svg.append('</g>')
        else:
            card_w = (1920 - 220 - ((kpi_count - 1) * 36)) / max(1, kpi_count)
            for i, kpi in enumerate(kpis):
                kx = 110 + (i * (card_w + 36))
                num_val = kpi.get("number", kpi.get("val", "+85%"))
                k_label = kpi.get("title", kpi.get("label", ""))
                k_desc = kpi.get("desc", "")
                trend = kpi.get("trend", "↑ رشد")

                svg.append(f'<g id="kpi_{i+1}">')
                svg.append(f'<rect x="{kx}" y="250" width="{card_w}" height="{card_w*1.1}" rx="30" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2.5" />')
                center_kx = kx + (card_w / 2)
                # Radiating aura circle behind numeral
                svg.append(f'<circle cx="{center_kx}" cy="380" r="110" fill="{self.theme["primary"]}" fill-opacity="0.12" />')
                svg.append(f'<text x="{center_kx}" y="420" font-family="{font}" font-size="82" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')
                # Trend pill
                svg.append(f'<rect x="{center_kx-80}" y="470" width="160" height="38" rx="19" fill="{self.theme["badge_bg"]}" stroke="{self.theme["accent"]}" stroke-width="1.5" />')
                svg.append(f'<text x="{center_kx}" y="495" font-family="{font}" font-size="16" font-weight="700" fill="{self.theme["accent"]}" text-anchor="middle">{escape_xml(trend)}</text>')
                svg.append(f'<text x="{center_kx}" y="560" font-family="{font}" font-size="30" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')
                if k_desc:
                    svg.append(f'<text x="{center_kx}" y="615" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="middle">{escape_xml(k_desc)}</text>')
                svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_comparison_slide(self, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Slidesgo Versus Matrix: high-contrast duel cards with red-cross vs neon-check."""
        title = slide.get("title", "مقایسه رویکرد سنتی و مدرن")
        kicker = slide.get("kicker", "تحلیل تطبیقی")
        col_a = slide.get("col_a", {"title": "روش‌های سنتی", "items": ["سرعت کند پردازش", "خطای انسانی بالا", "هزینه‌های نگهداری سنگین"]})
        col_b = slide.get("col_b", {"title": "راهکار هوش مصنوعی", "items": ["پردازش بلادرنگ و سریع", "دقت ۹۹.۲ درصدی", "کاهش ۶۰٪ هزینه‌ها"]})
        rtl = is_persian(title) or is_persian(col_a.get("title", ""))

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 810
        card_h = 700
        ca_x = 990 if rtl else 110
        cb_x = 110 if rtl else 990
        card_y = 235

        # Column A (Muted / Problem / Traditional)
        svg.append('<g id="compare_col_a">')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="30" fill="{self.theme["surface"]}" stroke="#EF4444" stroke-width="2" stroke-opacity="0.5" />')
        # Header Badge
        svg.append(f'<rect x="{ca_x+40}" y="{card_y+40}" width="260" height="56" rx="28" fill="{self.theme["background"]}" stroke="#EF4444" stroke-width="2" />')
        svg.append(f'<text x="{ca_x+170}" y="{card_y+76}" font-family="{font}" font-size="22" font-weight="700" fill="#EF4444" text-anchor="middle">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        # Items with circle-x icon (Verbatim)
        curr_y = card_y + 170
        tx = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(get_icon_svg_content("circle-x", (tx - 38) if rtl else tx, curr_y - 20, size=28, stroke_color="#EF4444"))
            item_tx = (tx - 54) if rtl else (tx + 44)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 72
        svg.append('</g>')

        # Column B (Vibrant / Solution / Smart)
        svg.append('<g id="compare_col_b">')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="30" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
        # Header Badge
        svg.append(f'<rect x="{cb_x+40}" y="{card_y+40}" width="300" height="56" rx="28" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
        svg.append(f'<text x="{cb_x+190}" y="{card_y+76}" font-family="{font}" font-size="22" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">✦ {escape_xml(col_b.get("title", "هوشمند"))}</text>')
        # Items with circle-check icon (Verbatim)
        curr_y = card_y + 170
        tx = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(get_icon_svg_content("circle-check", (tx - 38) if rtl else tx, curr_y - 20, size=28, stroke_color=self.theme["primary"]))
            item_tx = (tx - 54) if rtl else (tx + 44)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 72
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_split_image_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None, slide_idx: int = 6) -> str:
        """Slidesgo Split Feature Showcase with Icon Bullets."""
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "بررسی تخصصی")
        bullets = slide.get("bullets", [])
        rtl = is_persian(title) or any(is_persian(str(b)) for b in bullets)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        text_x = 1800 if rtl else 120
        image_x = 110 if rtl else 1020
        image_y = 220
        image_w = 790
        image_h = 720

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header & Text
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{text_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{text_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        svg.append('<g id="bullets_group">')
        tx = text_x
        curr_y = 280
        for i, bullet in enumerate(bullets):
            svg.append(f'<g id="bullet_{i+1}">')
            icon_x = (tx - 38) if rtl else tx
            svg.append(get_icon_svg_content("rosette-check", icon_x, curr_y - 20, size=30, stroke_color=self.theme["secondary"]))
            text_pos_x = (tx - 54) if rtl else (tx + 48)
            svg.append(f'<text x="{text_pos_x}" y="{curr_y}" font-family="{font}" font-size="24" font-weight="500" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(bullet)}</text>')
            svg.append('</g>')
            curr_y += 85
        svg.append('</g>')

        # Image Container
        svg.append('<g id="hero_image">')
        svg.append(f'<rect x="{image_x-6}" y="{image_y-6}" width="{image_w+12}" height="{image_h+12}" rx="32" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.35" />')
        svg.append(f'<rect x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
        if image_rel_path:
            svg.append(f'<image href="{image_rel_path}" x="{image_x+10}" y="{image_y+10}" width="{image_w-20}" height="{image_h-20}" preserveAspectRatio="xMidYMid slice" />')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


def generate_presentation_project(
    deck_data: Dict[str, Any],
    project_dir: Path,
    output_pptx: Optional[Path] = None,
    theme_key: str = "cyber_aurora",
    transition: str = "morph",
    animation_mode: str = "auto"
) -> Path:
    """
    Generate complete SVG deck, notes, and compile to native PPTX with intelligent Morph transitions.
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

    print(f"Creating rich, non-minimalist presentation with {len(slides)} slides...")

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
            svg_content = renderer.render_process_steps_slide(slide, slide_idx=idx)
        elif layout == "stats_kpi":
            img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))
            svg_content = renderer.render_stats_kpi_slide(slide, image_rel_path=img_rel_for_svg, slide_idx=idx)
        elif layout == "comparison":
            svg_content = renderer.render_comparison_slide(slide, slide_idx=idx)
        elif layout == "split_image":
            img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))
            svg_content = renderer.render_split_image_slide(slide, image_rel_path=img_rel_for_svg, slide_idx=idx)
        else: # default content_cards
            svg_content = renderer.render_content_cards_slide(slide, slide_idx=idx)

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

    # Compile using svg_to_pptx.py with native Morph and element entrance builds
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
    parser = argparse.ArgumentParser(description="PPT_Saz: Generate ultra-graphic native PowerPoint presentations.")
    parser.add_argument("input", help="Path to input JSON file or deck configuration")
    parser.add_argument("-o", "--output", help="Output .pptx path", default=None)
    parser.add_argument("-p", "--project-dir", help="Working project directory", default="./presentation_project")
    parser.add_argument("-t", "--transition", help="Slide transition (morph, fade, push, wipe, zoom)", default="morph")
    parser.add_argument("-a", "--animation", help="Animation mode (auto, mixed, none)", default="auto")
    parser.add_argument("--theme", help="Theme palette name (cyber_aurora, royal_gold_navy, deep_emerald, dark_violet_pulse, sunset_crimson)", default="cyber_aurora")

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
