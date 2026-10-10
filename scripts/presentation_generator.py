#!/usr/bin/env python3
"""
PPT Master - Presentation Generator v3.1 (Circular & Particle Motion Engine)

Features:
  - Non-minimalist rich multi-layer background with animated particle constellations and rotating dashed orbit rings.
  - Circular & organic layout archetypes breaking the square box monotony:
      * Circular Orbital Milestones with spinning calibration halos
      * Circular Radial Gauges and KPI Dial pods
      * Circular Icon Medallion crowns with rotating dashed auras
      * Circular Sun & Planet Orbit archetype (`circular_orbit`)
      * Central rotating circular "VS" battle orb in comparisons
  - Object animations:
      * Elements with id starting with `spin_` automatically spin 360 degrees into place (`entrance_spinner`).
  - Seamless Morph slide transitions (`-t morph`) by default.
  - Pure presentation attributes on all DrawingML shapes (zero CSS classes) for 100% PPTX compatibility.
  - Complete verbatim preservation of user slide titles and descriptions.
  - Native Yekan Bakh typography with Persian RTL attributes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio
from icon_mapper import get_icon_svg_content
from archetype_layouts import (
    BentoGridRenderer,
    SwissAcademicRenderer,
    NeoBrutalistRenderer,
    WarmEditorialRenderer,
    RoyalGoldRenderer,
)

configure_utf8_stdio()


def is_persian(text: str) -> bool:
    """Check if string contains Persian / Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def to_persian_digits(num: int | str) -> str:
    """Convert western digits to Persian digits."""
    s = str(num)
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    en_digits = "0123456789"
    table = str.maketrans(en_digits, fa_digits)
    return s.translate(table)


def load_themes() -> Dict[str, Dict[str, Any]]:
    """Load curated themes from presets/themes.json."""
    theme_file = _SCRIPTS_DIR.parent / "presets" / "themes.json"
    if not theme_file.exists():
        theme_file = Path("presets/themes.json")
    if theme_file.exists():
        with open(theme_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def escape_xml(s: str) -> str:
    """Escape XML special characters."""
    if not s:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


class SlideRenderer:
    """
    Renders rich, ultra-graphic presentation slides with layered ambient geometry,
    rotating dashed orbit rings, particle constellations, circular infographic pods,
    and Yekan Bakh typography.
    """
    def __init__(self, theme: Dict[str, Any], width: int = 1920, height: int = 1080):
        self.theme = theme
        self.width = width
        self.height = height
        self.archetype = theme.get("archetype", "cyber_hud")
        self.is_dark = theme.get("is_dark", True)

    def _card_rect(self, x: float, y: float, w: float, h: float, rx: float = 28, stroke_width: float = 2.0, top_accent: bool = True) -> List[str]:
        """Generate style-aware card background shape and accents tailored to current art-style."""
        out = []
        if self.archetype == "neo_brutalist":
            shadow_col = "#000000" if not self.is_dark else self.theme.get("primary", "#A3E635")
            border_col = "#000000" if not self.is_dark else "#FFFFFF"
            out.append(f'<rect x="{x + 8}" y="{y + 8}" width="{w}" height="{h}" rx="18" fill="{shadow_col}" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{self.theme["surface"]}" stroke="{border_col}" stroke-width="3.5" />')
        elif self.archetype == "swiss_academic":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="1.2" />')
            if top_accent:
                out.append(f'<rect x="{x}" y="{y}" width="{w}" height="4" rx="2" fill="{self.theme["secondary"]}" />')
        elif self.archetype == "apple_bento":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="1.5" stroke-opacity="0.85" />')
            if top_accent:
                out.append(f'<rect x="{x + 24}" y="{y}" width="{w - 48}" height="2" fill="{self.theme["primary"]}" fill-opacity="0.5" />')
        elif self.archetype == "royal_gold":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="1.5" />')
            out.append(f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="{self.theme["primary"]}" stroke-width="0.75" stroke-opacity="0.4" />')
        elif self.archetype == "warm_editorial":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="1.8" />')
            if top_accent:
                out.append(f'<rect x="{x + 30}" y="{y}" width="{w - 60}" height="3" rx="1.5" fill="{self.theme["primary"]}" />')
        else:  # cyber_hud
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="{stroke_width}" />')
            if top_accent:
                out.append(f'<rect x="{x + 40}" y="{y}" width="{w - 80}" height="5" rx="2.5" fill="{self.theme["primary"]}" />')
        return out

    def _header_svg(self, is_rtl: bool, slide_idx: int = 1) -> str:
        lang = "fa" if is_rtl else "en"
        primary = self.theme["primary"]
        secondary = self.theme["secondary"]
        wave_1 = self.theme.get("wave_1", "#0E1E45")
        wave_2 = self.theme.get("wave_2", "#1E1B4B")
        accent = self.theme.get("accent", "#EC4899")
        font = self.theme.get("font_fa" if is_rtl else "font_en")

        bg_rect = f'<rect width="{self.width}" height="{self.height}" fill="{self.theme["background"]}" />'
        extra_bg = []

        if self.archetype == "swiss_academic":
            # Precision surgical grid lines
            grid_lines = []
            for gx in range(240, 1800, 240):
                grid_lines.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="1000" stroke="{self.theme["surface_border"]}" stroke-width="0.75" stroke-opacity="0.3" />')
            for gy in range(180, 960, 180):
                grid_lines.append(f'<line x1="80" y1="{gy}" x2="1840" y2="{gy}" stroke="{self.theme["surface_border"]}" stroke-width="0.75" stroke-opacity="0.3" />')
            for gx in (480, 960, 1440):
                for gy in (360, 720):
                    grid_lines.append(f'<text x="{gx}" y="{gy+4}" font-family="monospace" font-size="14" fill="{secondary}" fill-opacity="0.5" text-anchor="middle">+</text>')
            top_rule = f'<line x1="80" y1="140" x2="1840" y2="140" stroke="{secondary}" stroke-width="1.5" stroke-opacity="0.5" />'
            compass_x = 1800 if is_rtl else 120
            compass_y = 960
            compass_svg = f"""
            <g id="spin_academic_compass">
                <circle cx="{compass_x}" cy="{compass_y}" r="110" fill="none" stroke="{secondary}" stroke-width="1.2" stroke-dasharray="3 9" stroke-opacity="0.4" />
                <circle cx="{compass_x}" cy="{compass_y}" r="80" fill="none" stroke="{primary}" stroke-width="1.5" stroke-opacity="0.5" />
                <line x1="{compass_x-95}" y1="{compass_y}" x2="{compass_x+95}" y2="{compass_y}" stroke="{secondary}" stroke-width="1" stroke-opacity="0.4" />
                <line x1="{compass_x}" y1="{compass_y-95}" x2="{compass_x}" y2="{compass_y+95}" stroke="{secondary}" stroke-width="1" stroke-opacity="0.4" />
            </g>
            """
            extra_bg.append(f'<g id="academic_grid">{"".join(grid_lines)}{top_rule}</g>')
            extra_bg.append(compass_svg)

        elif self.archetype == "neo_brutalist":
            # Retro Pop Dot Matrix & Rotating Starburst Badge
            dot_color = "#000000" if not self.is_dark else self.theme.get("primary", "#A3E635")
            dots = []
            for dx in range(120, 1820, 120):
                for dy in range(120, 980, 120):
                    dots.append(f'<circle cx="{dx}" cy="{dy}" r="2.5" fill="{dot_color}" fill-opacity="0.12" />')
            dots_svg = "".join(dots)
            corner_poly = f'<polygon points="0,0 200,0 0,200" fill="{primary}" stroke="{dot_color}" stroke-width="3" />'
            badge_x = 1760 if is_rtl else 160
            badge_y = 120
            badge_svg = f"""
            <g id="spin_brutalist_badge">
                <circle cx="{badge_x}" cy="{badge_y}" r="45" fill="{accent}" stroke="{dot_color}" stroke-width="3" />
                <text x="{badge_x}" y="{badge_y+10}" font-family="{font}" font-size="28" font-weight="900" fill="{self.theme['text_main']}" text-anchor="middle">★</text>
            </g>
            """
            extra_bg.append(f'<g id="brutalist_ambient">{dots_svg}{corner_poly}</g>')
            extra_bg.append(badge_svg)

        elif self.archetype == "apple_bento":
            # Ambient Blurred Glow Orbs & Bento Halos
            orbs = f"""
            <g id="bento_glow_orbs">
                <circle cx="280" cy="180" r="280" fill="{primary}" fill-opacity="0.10" />
                <circle cx="1640" cy="900" r="320" fill="{secondary}" fill-opacity="0.08" />
                <circle cx="960" cy="540" r="200" fill="{accent}" fill-opacity="0.05" />
            </g>
            """
            halo_x = 1800 if is_rtl else 120
            halo_y = 960
            halo_svg = f"""
            <g id="spin_bento_halo">
                <circle cx="{halo_x}" cy="{halo_y}" r="220" fill="none" stroke="{primary}" stroke-width="1.2" stroke-dasharray="8 12" stroke-opacity="0.3" />
                <circle cx="{halo_x}" cy="{halo_y}" r="150" fill="none" stroke="{secondary}" stroke-width="1.8" stroke-dasharray="4 8" stroke-opacity="0.35" />
                <circle cx="{halo_x + 150}" cy="{halo_y}" r="4" fill="{primary}" />
            </g>
            """
            extra_bg.append(orbs)
            extra_bg.append(halo_svg)

        elif self.archetype == "warm_editorial":
            # Organic flowing wave contours & Botanical Sun
            w1 = f'<path d="M0,720 C480,620 780,880 1200,760 C1620,640 1780,860 1920,800 L1920,1080 L0,1080 Z" fill="{wave_1}" fill-opacity="0.7" />'
            w2 = f'<path d="M0,840 C420,760 840,960 1300,850 C1620,770 1820,920 1920,880 L1920,1080 L0,1080 Z" fill="{wave_2}" fill-opacity="0.85" />'
            sun_x = 1800 if is_rtl else 120
            sun_y = 960
            sun_svg = f"""
            <g id="spin_botanical_sun">
                <circle cx="{sun_x}" cy="{sun_y}" r="200" fill="none" stroke="{primary}" stroke-width="1.5" stroke-dasharray="6 10" stroke-opacity="0.35" />
                <circle cx="{sun_x}" cy="{sun_y}" r="140" fill="none" stroke="{secondary}" stroke-width="2" stroke-dasharray="12 8" stroke-opacity="0.3" />
                <circle cx="{sun_x}" cy="{sun_y}" r="70" fill="{self.theme['badge_bg']}" stroke="{primary}" stroke-width="1.5" />
            </g>
            """
            extra_bg.append(f'<g id="organic_waves">{w1}{w2}</g>')
            extra_bg.append(sun_svg)

        elif self.archetype == "royal_gold":
            # Art-Deco luxury pinstripe frame & Royal Crest
            pinstripes = f"""
            <g id="royal_pinstripes">
                <rect x="36" y="36" width="1848" height="1008" fill="none" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.45" />
                <rect x="48" y="48" width="1824" height="984" fill="none" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.3" stroke-dasharray="14 10" />
                <polygon points="36,60 60,36 48,36 36,48" fill="{primary}" />
                <polygon points="1884,60 1860,36 1872,36 1884,48" fill="{primary}" />
                <polygon points="36,1020 60,1044 48,1044 36,1032" fill="{primary}" />
                <polygon points="1884,1020 1860,1044 1872,1044 1884,1032" fill="{primary}" />
            </g>
            """
            crest_x = 1800 if is_rtl else 120
            crest_y = 960
            crest_svg = f"""
            <g id="spin_royal_crest">
                <circle cx="{crest_x}" cy="{crest_y}" r="210" fill="none" stroke="{primary}" stroke-width="1.5" stroke-dasharray="4 8" stroke-opacity="0.4" />
                <circle cx="{crest_x}" cy="{crest_y}" r="150" fill="none" stroke="{secondary}" stroke-width="2" stroke-dasharray="12 12" stroke-opacity="0.45" />
                <polygon points="{crest_x},{crest_y-25} {crest_x+25},{crest_y} {crest_x},{crest_y+25} {crest_x-25},{crest_y}" fill="{primary}" fill-opacity="0.7" />
            </g>
            """
            extra_bg.append(pinstripes)
            extra_bg.append(crest_svg)

        else:  # cyber_hud
            particles = []
            part_base_x = 120 if is_rtl else 1650
            particle_coords = [
                (part_base_x, 80, 4.0, 0.6), (part_base_x + 60, 130, 2.5, 0.4),
                (part_base_x - 50, 170, 3.5, 0.5), (part_base_x + 90, 75, 2.0, 0.3),
                (part_base_x + 130, 160, 4.5, 0.7), (part_base_x - 90, 115, 3.0, 0.4),
                (part_base_x + 35, 220, 2.5, 0.35), (part_base_x - 55, 250, 4.0, 0.55),
                (960, 60, 3.0, 0.4), (910, 105, 2.0, 0.3), (1010, 95, 4.0, 0.5),
                (240, 880, 3.5, 0.45), (310, 930, 2.2, 0.3), (1680, 870, 3.8, 0.5)
            ]
            for px, py, pr, p_op in particle_coords:
                p_col = primary if pr > 3 else (secondary if pr > 2.5 else accent)
                particles.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{p_col}" fill-opacity="{p_op}" />')
            particles_svg = "\n".join(particles)

            if slide_idx % 2 == 1:
                wave_path_1 = f'<path d="M0,720 Q480,580 960,760 T1920,680 L1920,1080 L0,1080 Z" fill="{wave_1}" fill-opacity="0.6" />'
                wave_path_2 = f'<path d="M0,840 Q520,740 1080,900 T1920,820 L1920,1080 L0,1080 Z" fill="{wave_2}" fill-opacity="0.85" />'
                glow_line = f'<path d="M0,720 Q480,580 960,760 T1920,680" fill="none" stroke="{primary}" stroke-width="3" stroke-opacity="0.45" />'
            else:
                wave_path_1 = f'<path d="M0,660 Q560,820 1100,640 T1920,740 L1920,1080 L0,1080 Z" fill="{wave_1}" fill-opacity="0.6" />'
                wave_path_2 = f'<path d="M0,800 Q440,920 1020,780 T1920,860 L1920,1080 L0,1080 Z" fill="{wave_2}" fill-opacity="0.85" />'
                glow_line = f'<path d="M0,660 Q560,820 1100,640 T1920,740" fill="none" stroke="{secondary}" stroke-width="3" stroke-opacity="0.45" />'

            ring_x = 1820 if is_rtl else 100
            ring_y = 960
            satellites = []
            for angle_deg, r_dist, sat_r, sat_c in [(35, 260, 6, primary), (145, 260, 5, secondary), (260, 180, 5.5, accent), (80, 380, 7, primary)]:
                rad = math.radians(angle_deg)
                sx = ring_x + (r_dist * math.cos(rad))
                sy = ring_y + (r_dist * math.sin(rad))
                satellites.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sat_r}" fill="{sat_c}" />')
                satellites.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sat_r+5}" fill="none" stroke="{sat_c}" stroke-width="1.5" stroke-opacity="0.4" />')
            satellites_svg = "\n".join(satellites)

            ambient_rings = f"""
            <circle cx="{ring_x}" cy="{ring_y}" r="260" fill="none" stroke="{primary}" stroke-width="2.5" stroke-opacity="0.3" stroke-dasharray="14 10" />
            <circle cx="{ring_x}" cy="{ring_y}" r="180" fill="none" stroke="{secondary}" stroke-width="2" stroke-opacity="0.35" stroke-dasharray="8 6" />
            <circle cx="{ring_x}" cy="{ring_y}" r="380" fill="none" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.2" stroke-dasharray="6 14" />
            {satellites_svg}
            """
            corner_chip = f"""
            <polygon points="0,0 220,0 0,220" fill="{primary}" fill-opacity="0.08" />
            <polygon points="1920,0 1700,0 1920,220" fill="{secondary}" fill-opacity="0.08" />
            """
            extra_bg.append(f'<g id="ambient_waves">{wave_path_1}{wave_path_2}{glow_line}</g>')
            extra_bg.append(f'<g id="spin_orbit_rings">{ambient_rings}</g>')
            extra_bg.append(f'<g id="spin_particle_cluster">{particles_svg}{corner_chip}</g>')

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" lang="{lang}">
<!-- Base Background -->
{bg_rect}
{"".join(extra_bg)}
"""

    def render_title_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Slidesgo Ultra-Poster Cover with spinning circular orbit frame & verbatim typography."""
        title = slide.get("title", "عنوان ارائه")
        subtitle = slide.get("subtitle", "")
        author = slide.get("author", "")
        kicker = slide.get("kicker", "ارائه تخصصی")
        rtl = is_persian(title) or is_persian(subtitle)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        x_pos = 1720 if rtl else 140

        svg = [self._header_svg(rtl, slide_idx=1)]

        # Glowing Category Pill Chip on top
        svg.append('<g id="kicker_pill">')
        pill_w = max(240, len(kicker) * 20)
        pill_x = (x_pos - pill_w) if rtl else x_pos
        svg.append(f'<rect x="{pill_x}" y="210" width="{pill_w}" height="48" rx="24" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
        # Circular glowing dot inside pill
        dot_in_pill = (pill_x + pill_w - 24) if rtl else (pill_x + 24)
        svg.append(f'<circle cx="{dot_in_pill}" cy="234" r="6" fill="{self.theme["primary"]}" />')
        chip_tx = (pill_x + (pill_w / 2) - 10) if rtl else (pill_x + (pill_w / 2) + 10)
        svg.append(f'<text x="{chip_tx}" y="242" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
        svg.append('</g>')

        # Title & Subtitle Group (Verbatim Text)
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{x_pos}" y="350" font-family="{font}" font-size="64" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        if subtitle:
            sub_lines = subtitle.split("\n")
            sy = 440
            for s_line in sub_lines[:4]:
                if s_line.strip():
                    svg.append(f'<text x="{x_pos}" y="{sy}" font-family="{font}" font-size="28" font-weight="600" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(s_line.strip())}</text>')
                    sy += 44
        svg.append('</g>')

        # Radiant Spine Accent Bar
        svg.append('<g id="accent_spine">')
        bar_x = (x_pos + 25) if rtl else (x_pos - 30)
        svg.append(f'<rect x="{bar_x}" y="290" width="10" height="230" fill="{self.theme["primary"]}" rx="5" />')
        svg.append(f'<rect x="{bar_x-3}" y="290" width="16" height="60" fill="{self.theme["secondary"]}" rx="4" />')
        svg.append('</g>')

        # Presenter Card Pill
        if author:
            svg.append('<g id="author_chip">')
            auth_w = max(300, len(author) * 19)
            auth_x = (x_pos - auth_w) if rtl else x_pos
            svg.append(f'<rect x="{auth_x}" y="600" width="{auth_w}" height="64" rx="24" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
            icon_x = (auth_x + auth_w - 48) if rtl else (auth_x + 16)
            svg.append(get_icon_svg_content("user", icon_x, 616, size=30, stroke_color=self.theme["primary"]))
            auth_tx = (auth_x + auth_w - 65) if rtl else (auth_x + 56)
            svg.append(f'<text x="{auth_tx}" y="640" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(author)}</text>')
            svg.append('</g>')

        # Hero Image Frame with Spinning Circular Orbits & Badges
        if image_rel_path:
            img_x = 100 if rtl else 1050
            center_hero_x = img_x + 375
            center_hero_y = 530

            # Spinning Dashed Orbit Rings around the Hero Center
            svg.append('<g id="spin_hero_orbit">')
            svg.append(f'<circle cx="{center_hero_x}" cy="{center_hero_y}" r="390" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.35" stroke-dasharray="12 8" />')
            svg.append(f'<circle cx="{center_hero_x}" cy="{center_hero_y}" r="430" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.2" stroke-opacity="0.25" stroke-dasharray="6 12" />')
            # Orbital satellites
            svg.append(f'<circle cx="{center_hero_x + 390}" cy="{center_hero_y}" r="8" fill="{self.theme["accent"]}" />')
            svg.append(f'<circle cx="{center_hero_x - 390}" cy="{center_hero_y}" r="6" fill="{self.theme["primary"]}" />')
            svg.append('</g>')

            svg.append('<g id="hero_image">')
            svg.append(f'<rect x="{img_x-8}" y="192" width="766" height="676" rx="42" fill="none" stroke="{self.theme["secondary"]}" stroke-width="2" stroke-opacity="0.4" />')
            svg.append(f'<rect x="{img_x}" y="200" width="750" height="660" rx="38" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            svg.append(f'<image href="{image_rel_path}" x="{img_x+12}" y="212" width="726" height="636" preserveAspectRatio="xMidYMid slice" />')
            
            # Floating Circular Badge Medallion on Image Corner
            badge_cx = (img_x + 90) if rtl else (img_x + 660)
            badge_cy = 270
            svg.append(f'<circle cx="{badge_cx}" cy="{badge_cy}" r="38" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            svg.append(f'<circle cx="{badge_cx}" cy="{badge_cy}" r="46" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.5" stroke-dasharray="4 4" />')
            svg.append(get_icon_svg_content("award", badge_cx - 20, badge_cy - 20, size=40, stroke_color=self.theme["primary"]))

            # Lower Capsule Tag
            svg.append(f'<rect x="{img_x+40}" y="780" width="260" height="52" rx="26" fill="{self.theme["background"]}" fill-opacity="0.94" stroke="{self.theme["primary"]}" stroke-width="2" />')
            svg.append(f'<text x="{img_x+170}" y="813" font-family="{font}" font-size="19" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">✦ ارائه تاییدشده رسمی</text>')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_content_cards_slide(self, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Slidesgo Feature Cards with distinct layout architecture per archetype."""
        if self.archetype == "apple_bento":
            return BentoGridRenderer.render_pillars(self, slide, slide_idx=slide_idx)
        elif self.archetype == "swiss_academic":
            return SwissAcademicRenderer.render_pillars(self, slide, slide_idx=slide_idx)
        elif self.archetype == "neo_brutalist":
            return NeoBrutalistRenderer.render_pillars(self, slide, slide_idx=slide_idx)
        elif self.archetype == "warm_editorial":
            return WarmEditorialRenderer.render_pillars(self, slide, slide_idx=slide_idx)
        elif self.archetype == "royal_gold":
            return RoyalGoldRenderer.render_pillars(self, slide, slide_idx=slide_idx)

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
        card_y = 250
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

            center_card_x = c_x + (card_w / 2)

            # Spinning Dashed Halo around the Crown (top-level continuous motion group)
            crown_cx = center_card_x
            crown_cy = card_y + 45
            crown_r = 52
            svg.append(f'<g id="spin_card_halo_{i+1}">')
            svg.append(f'<circle cx="{crown_cx}" cy="{crown_cy}" r="{crown_r + 14}" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-dasharray="6 5" stroke-opacity="0.55" />')
            svg.append(f'<circle cx="{crown_cx}" cy="{crown_cy}" r="{crown_r + 24}" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1" stroke-dasharray="3 6" stroke-opacity="0.3" />')
            svg.append(f'<circle cx="{crown_cx + crown_r + 14}" cy="{crown_cy}" r="4" fill="{self.theme["accent"]}" />')
            svg.append('</g>')

            svg.append(f'<g id="card_{i+1}">')
            # Style-aware Card Body
            svg.extend(self._card_rect(c_x, card_y, card_w, card_h, rx=34, stroke_width=2.5))
            # Circular Medallion Disc
            svg.append(f'<circle cx="{crown_cx}" cy="{crown_cy}" r="{crown_r}" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2.8" />')
            # Vector Icon Centered in Medallion
            svg.append(get_icon_svg_content(icon_key, crown_cx - 24, crown_cy - 24, size=48, stroke_color=self.theme["primary"]))

            # Step / Index Tag Pill under crown
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            svg.append(f'<rect x="{center_card_x - 34}" y="{card_y + 115}" width="68" height="30" rx="15" fill="{self.theme["background"]}" stroke="{self.theme["secondary"]}" stroke-width="1.5" />')
            svg.append(f'<text x="{center_card_x}" y="{card_y + 137}" font-family="{font}" font-size="18" font-weight="700" fill="{self.theme["secondary"]}" text-anchor="middle">{num_str}</text>')

            # Card Title (Verbatim)
            svg.append(f'<text x="{center_card_x}" y="{card_y + 185}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(c_title)}</text>')

            # Verbatim Text Preservation: split into structured lines with circular glowing bullets
            desc_lines = c_desc.split("\n")
            curr_y = card_y + 245
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
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
        """Process Steps Slide with distinct layout architecture per archetype."""
        if self.archetype == "apple_bento":
            return BentoGridRenderer.render_process_steps(self, slide, slide_idx=slide_idx)
        elif self.archetype == "swiss_academic":
            return SwissAcademicRenderer.render_process_steps(self, slide, slide_idx=slide_idx)
        elif self.archetype == "neo_brutalist":
            return NeoBrutalistRenderer.render_process_steps(self, slide, slide_idx=slide_idx)
        elif self.archetype == "warm_editorial":
            return WarmEditorialRenderer.render_process_steps(self, slide, slide_idx=slide_idx)
        elif self.archetype == "royal_gold":
            return RoyalGoldRenderer.render_process_steps(self, slide, slide_idx=slide_idx)

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
        hub_y = 350
        pod_y = 510
        pod_h = 430

        # Glowing Pulse Connector Line
        svg.append(f'<line x1="{margin + 80}" y1="{hub_y}" x2="{self.width - margin - 80}" y2="{hub_y}" stroke="{self.theme["surface_border"]}" stroke-width="6" stroke-dasharray="14 10" />')
        svg.append(f'<line x1="{margin + 80}" y1="{hub_y}" x2="{self.width - margin - 80}" y2="{hub_y}" stroke="{self.theme["primary"]}" stroke-width="2.5" stroke-opacity="0.8" />')

        for i, step in enumerate(steps):
            s_title = step.get("title", f"مرحله {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            if rtl:
                center_x = (self.width - margin) - ((i + 0.5) * (step_w + gap))
            else:
                center_x = margin + ((i + 0.5) * (step_w + gap))

            pod_x = center_x - (step_w / 2)

            # Spinning Dashed Orbit Rings around the Circular Hub (top-level continuous motion group)
            svg.append(f'<g id="spin_step_orbit_{i+1}">')
            svg.append(f'<circle cx="{center_x}" cy="{hub_y}" r="115" fill="none" stroke="{self.theme["primary"]}" stroke-width="2.5" stroke-dasharray="8 6" stroke-opacity="0.6" />')
            svg.append(f'<circle cx="{center_x}" cy="{hub_y}" r="130" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.2" stroke-dasharray="4 8" stroke-opacity="0.4" />')
            svg.append(f'<circle cx="{center_x + 115}" cy="{hub_y}" r="5.5" fill="{self.theme["accent"]}" />')
            svg.append(f'<circle cx="{center_x - 115}" cy="{hub_y}" r="4.5" fill="{self.theme["primary"]}" />')
            svg.append('</g>')

            svg.append(f'<g id="step_node_{i+1}">')
            # Inner Glass Circular Medallion
            svg.append(f'<circle cx="{center_x}" cy="{hub_y}" r="92" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')

            # Top Step Number Bubble
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            svg.append(f'<circle cx="{center_x}" cy="{hub_y - 74}" r="26" fill="{self.theme["badge_bg"]}" stroke="{self.theme["secondary"]}" stroke-width="2.5" />')
            svg.append(f'<text x="{center_x}" y="{hub_y - 64}" font-family="{font}" font-size="22" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{num_str}</text>')

            # Vector Icon inside Circle
            svg.append(get_icon_svg_content(icon_key, center_x - 24, hub_y - 24, size=48, stroke_color=self.theme["secondary"]))

            # Step Title in Circle Bottom
            svg.append(f'<text x="{center_x}" y="{hub_y + 54}" font-family="{font}" font-size="21" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')

            # Style-aware Capsule Pod for Verbatim Description
            svg.extend(self._card_rect(pod_x, pod_y, step_w, pod_h, rx=32, stroke_width=2.0))

            # Verbatim Description with glowing circular dots
            desc_lines = s_desc.split("\n")
            curr_y = pod_y + 60
            tx = (pod_x + step_w - 36) if rtl else (pod_x + 36)
            for line in desc_lines[:7]:
                clean_l = line.strip()
                if clean_l:
                    b_dot = (tx - 8) if rtl else (tx + 8)
                    t_pos = (tx - 30) if rtl else (tx + 30)
                    svg.append(f'<circle cx="{b_dot}" cy="{curr_y-6}" r="5" fill="{self.theme["primary"]}" />')
                    svg.append(f'<text x="{t_pos}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 44
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_stats_kpi_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None, slide_idx: int = 4) -> str:
        """KPI Stats Slide with distinct layout architecture per archetype."""
        if self.archetype == "apple_bento":
            return BentoGridRenderer.render_stats_kpi(self, slide, slide_idx=slide_idx)
        elif self.archetype == "swiss_academic":
            return SwissAcademicRenderer.render_stats_kpi(self, slide, slide_idx=slide_idx)
        elif self.archetype == "neo_brutalist":
            return NeoBrutalistRenderer.render_stats_kpi(self, slide, slide_idx=slide_idx)
        elif self.archetype == "warm_editorial":
            return WarmEditorialRenderer.render_stats_kpi(self, slide, slide_idx=slide_idx)
        elif self.archetype == "royal_gold":
            return RoyalGoldRenderer.render_stats_kpi(self, slide, slide_idx=slide_idx)

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
            svg.append(f'<rect x="{img_x-6}" y="{img_y-6}" width="{img_w+12}" height="{img_h+12}" rx="36" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.35" />')
            svg.append(f'<rect x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" rx="32" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
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

                dial_cx = (stack_x + stack_w - 110) if rtl else (stack_x + 110)
                dial_cy = ky + (kpi_h / 2)
                
                # Spinning Calibration Track (top-level continuous motion group)
                svg.append(f'<g id="spin_kpi_dial_{i+1}">')
                svg.append(f'<circle cx="{dial_cx}" cy="{dial_cy}" r="78" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.8" stroke-dasharray="4 6" stroke-opacity="0.5" />')
                svg.append(f'<circle cx="{dial_cx}" cy="{dial_cy}" r="64" fill="none" stroke="{self.theme["primary"]}" stroke-width="6" stroke-dasharray="260 140" stroke-linecap="round" />')
                svg.append(f'<circle cx="{dial_cx + 78}" cy="{dial_cy}" r="4" fill="{self.theme["accent"]}" />')
                svg.append('</g>')

                svg.append(f'<g id="kpi_{i+1}">')
                # Style-aware glass card container
                svg.extend(self._card_rect(stack_x, ky, stack_w, kpi_h, rx=32, stroke_width=2.0))

                # Inner circle for dial
                svg.append(f'<circle cx="{dial_cx}" cy="{dial_cy}" r="54" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
                svg.append(f'<text x="{dial_cx}" y="{dial_cy + 12}" font-family="{font}" font-size="34" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')

                # Label & Verbatim Desc
                text_x = (stack_x + stack_w - 230) if rtl else (stack_x + 230)
                svg.append(f'<text x="{text_x}" y="{ky + 65}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(k_label)}</text>')
                if k_desc:
                    svg.append(f'<text x="{text_x}" y="{ky + 115}" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(k_desc)}</text>')

                # Trend Pill
                pill_x = (stack_x + 40) if rtl else (stack_x + stack_w - 200)
                svg.append(f'<rect x="{pill_x}" y="{ky + 45}" width="160" height="40" rx="20" fill="{self.theme["badge_bg"]}" stroke="{self.theme["accent"]}" stroke-width="1.5" />')
                svg.append(f'<text x="{pill_x + 80}" y="{ky + 71}" font-family="{font}" font-size="16" font-weight="700" fill="{self.theme["accent"]}" text-anchor="middle">{escape_xml(trend)}</text>')
                svg.append('</g>')
        else:
            # Standalone Circular Radial KPI Dials
            card_w = (1920 - 220 - ((kpi_count - 1) * 44)) / max(1, kpi_count)
            for i, kpi in enumerate(kpis):
                if rtl:
                    center_x = (self.width - 110) - ((i + 0.5) * (card_w + 44))
                else:
                    center_x = 110 + ((i + 0.5) * (card_w + 44))
                
                num_val = kpi.get("number", kpi.get("val", "+85%"))
                k_label = kpi.get("title", kpi.get("label", ""))
                k_desc = kpi.get("desc", "")
                trend = kpi.get("trend", "↑ رشد")

                dial_y = 390
                pod_y = dial_y + 160
                pod_x = center_x - (card_w / 2)
                pod_h = 390

                # Spinning Radial Calibration Gauge & Dial Rings (top-level continuous motion group)
                svg.append(f'<g id="spin_kpi_dial_{i+1}">')
                svg.append(f'<circle cx="{center_x}" cy="{dial_y}" r="140" fill="none" stroke="{self.theme["secondary"]}" stroke-width="2" stroke-opacity="0.45" stroke-dasharray="5 7" />')
                svg.append(f'<circle cx="{center_x}" cy="{dial_y}" r="118" fill="none" stroke="{self.theme["surface_border"]}" stroke-width="12" />')
                svg.append(f'<circle cx="{center_x}" cy="{dial_y}" r="118" fill="none" stroke="{self.theme["primary"]}" stroke-width="12" stroke-dasharray="520 220" stroke-linecap="round" />')
                svg.append(f'<circle cx="{center_x + 140}" cy="{dial_y}" r="6" fill="{self.theme["accent"]}" />')
                svg.append(f'<circle cx="{center_x - 140}" cy="{dial_y}" r="5" fill="{self.theme["primary"]}" />')
                svg.append('</g>')

                svg.append(f'<g id="kpi_node_{i+1}">')
                # Inner Glass Disc
                svg.append(f'<circle cx="{center_x}" cy="{dial_y}" r="98" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')

                # Giant KPI Numeral in Center of Circle
                num_font_size = 72 if len(num_val) <= 5 else 54
                svg.append(f'<text x="{center_x}" y="{dial_y + 24}" font-family="{font}" font-size="{num_font_size}" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')

                # Floating Trend Capsule attached under the circle
                svg.append(f'<rect x="{center_x - 90}" y="{dial_y + 115}" width="180" height="42" rx="21" fill="{self.theme["badge_bg"]}" stroke="{self.theme["accent"]}" stroke-width="2" />')
                svg.append(f'<text x="{center_x}" y="{dial_y + 142}" font-family="{font}" font-size="17" font-weight="700" fill="{self.theme["accent"]}" text-anchor="middle">{escape_xml(trend)}</text>')

                # Style-aware Pod for KPI Label and Verbatim Description
                svg.extend(self._card_rect(pod_x, pod_y, card_w, pod_h, rx=32, stroke_width=2.0))
                svg.append(f'<text x="{center_x}" y="{pod_y + 60}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')

                # Verbatim Description Lines
                desc_lines = k_desc.split("\n")
                curr_y = pod_y + 115
                for line in desc_lines[:6]:
                    clean_l = line.strip()
                    if clean_l:
                        svg.append(f'<text x="{center_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="middle">{escape_xml(clean_l)}</text>')
                        curr_y += 40

                svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_comparison_slide(self, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Slidesgo Versus Matrix with central rotating Circular Battle Emblem (VS)."""
        if self.archetype == "apple_bento":
            return BentoGridRenderer.render_comparison(self, slide, slide_idx=slide_idx)
        elif self.archetype == "swiss_academic":
            return SwissAcademicRenderer.render_comparison(self, slide, slide_idx=slide_idx)
        elif self.archetype == "neo_brutalist":
            return NeoBrutalistRenderer.render_comparison(self, slide, slide_idx=slide_idx)
        elif self.archetype == "warm_editorial":
            return WarmEditorialRenderer.render_comparison(self, slide, slide_idx=slide_idx)
        elif self.archetype == "royal_gold":
            return RoyalGoldRenderer.render_comparison(self, slide, slide_idx=slide_idx)

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

        card_w = 800
        card_h = 700
        ca_x = 1000 if rtl else 120
        cb_x = 120 if rtl else 1000
        card_y = 235

        # Column A (Muted / Problem / Traditional)
        svg.append('<g id="compare_col_a">')
        if self.archetype == "neo_brutalist":
            svg.append(f'<rect x="{ca_x+8}" y="{card_y+8}" width="{card_w}" height="{card_h}" rx="18" fill="#EF4444" />')
            svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="18" fill="{self.theme["surface"]}" stroke="#EF4444" stroke-width="3.5" />')
        else:
            svg.extend(self._card_rect(ca_x, card_y, card_w, card_h, rx=34, stroke_width=2.5, top_accent=False))
        # Circular Icon Badge
        svg.append(f'<circle cx="{ca_x+70}" cy="{card_y+65}" r="32" fill="{self.theme["background"]}" stroke="#EF4444" stroke-width="2" />')
        svg.append(get_icon_svg_content("x", ca_x + 54, card_y + 49, size=32, stroke_color="#EF4444"))
        svg.append(f'<text x="{ca_x+120}" y="{card_y+74}" font-family="{font}" font-size="26" font-weight="700" fill="#EF4444" text-anchor="start">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        
        # Items with circle-x icon (Verbatim)
        curr_y = card_y + 175
        tx = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(get_icon_svg_content("circle-x", (tx - 38) if rtl else tx, curr_y - 20, size=28, stroke_color="#EF4444"))
            item_tx = (tx - 54) if rtl else (tx + 44)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 72
        svg.append('</g>')

        # Column B (Vibrant / Solution / Smart)
        svg.append('<g id="compare_col_b">')
        if self.archetype == "neo_brutalist":
            shadow_b = "#000000" if not self.is_dark else self.theme.get("primary", "#A3E635")
            svg.append(f'<rect x="{cb_x+8}" y="{card_y+8}" width="{card_w}" height="{card_h}" rx="18" fill="{shadow_b}" />')
            svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="18" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3.5" />')
        else:
            svg.extend(self._card_rect(cb_x, card_y, card_w, card_h, rx=34, stroke_width=3.0, top_accent=False))
        # Circular Icon Badge
        svg.append(f'<circle cx="{cb_x+70}" cy="{card_y+65}" r="32" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
        svg.append(get_icon_svg_content("check", cb_x + 54, card_y + 49, size=32, stroke_color=self.theme["primary"]))
        svg.append(f'<text x="{cb_x+120}" y="{card_y+74}" font-family="{font}" font-size="26" font-weight="700" fill="{self.theme["primary"]}" text-anchor="start">✦ {escape_xml(col_b.get("title", "هوشمند"))}</text>')
        
        # Items with circle-check icon (Verbatim)
        curr_y = card_y + 175
        tx = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(get_icon_svg_content("circle-check", (tx - 38) if rtl else tx, curr_y - 20, size=28, stroke_color=self.theme["primary"]))
            item_tx = (tx - 54) if rtl else (tx + 44)
            svg.append(f'<text x="{item_tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 72
        svg.append('</g>')

        # Central Rotating Circular Battle Emblem (VS)
        vs_cx = 960
        vs_cy = 585
        svg.append('<g id="spin_vs_orb">')
        svg.append(f'<circle cx="{vs_cx}" cy="{vs_cy}" r="68" fill="none" stroke="{self.theme["accent"]}" stroke-width="2.5" stroke-dasharray="6 5" />')
        svg.append(f'<circle cx="{vs_cx}" cy="{vs_cy}" r="82" fill="none" stroke="{self.theme["primary"]}" stroke-width="1.2" stroke-dasharray="4 8" stroke-opacity="0.5" />')
        svg.append(f'<circle cx="{vs_cx + 68}" cy="{vs_cy}" r="5" fill="{self.theme["primary"]}" />')
        svg.append(f'<circle cx="{vs_cx - 68}" cy="{vs_cy}" r="5" fill="{self.theme["accent"]}" />')
        svg.append(f'<circle cx="{vs_cx}" cy="{vs_cy}" r="52" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
        svg.append(f'<text x="{vs_cx}" y="{vs_cy + 10}" font-family="{font}" font-size="28" font-weight="700" fill="{self.theme["primary"]}" text-anchor="middle">VS</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_circular_orbit_slide(self, slide: Dict[str, Any], slide_idx: int = 6) -> str:
        """Slidesgo Planetary Orbit: central nucleus connected to surrounding circular planetary pods."""
        title = slide.get("title", "سامانه مداری یکپارچه")
        kicker = slide.get("kicker", "معماری ارتباطی")
        pods = slide.get("pods", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(p)) for p in pods)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        nucleus_cx = 960
        nucleus_cy = 580
        nucleus_r = 135

        # Massive Spinning Orbital Galaxy Track
        svg.append('<g id="spin_galaxy_orbit">')
        svg.append(f'<circle cx="{nucleus_cx}" cy="{nucleus_cy}" r="380" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-dasharray="10 8" stroke-opacity="0.45" />')
        svg.append(f'<circle cx="{nucleus_cx}" cy="{nucleus_cy}" r="430" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.2" stroke-dasharray="6 12" stroke-opacity="0.3" />')
        svg.append('</g>')

        # Center Nucleus
        svg.append('<g id="center_nucleus">')
        svg.append(f'<circle cx="{nucleus_cx}" cy="{nucleus_cy}" r="{nucleus_r}" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="4" />')
        svg.append(f'<circle cx="{nucleus_cx}" cy="{nucleus_cy}" r="{nucleus_r - 12}" fill="{self.theme["surface"]}" stroke="{self.theme["secondary"]}" stroke-width="2" />')
        svg.append(get_icon_svg_content("atom", nucleus_cx - 28, nucleus_cy - 60, size=56, stroke_color=self.theme["primary"]))
        svg.append(f'<text x="{nucleus_cx}" y="{nucleus_cy + 25}" font-family="{font}" font-size="24" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(title)}</text>')
        svg.append(f'<text x="{nucleus_cx}" y="{nucleus_cy + 55}" font-family="{font}" font-size="17" font-weight="600" fill="{self.theme["primary"]}" text-anchor="middle">هسته مرکزی معماری</text>')
        svg.append('</g>')

        # Surrounding Planetary Pods (up to 4)
        pod_angles = [210, 330, 150, 30] if len(pods) == 4 else [180, 0, 90, 270][:len(pods)]
        for i, pod in enumerate(pods[:4]):
            p_title = pod.get("title", f"بخش {i+1}")
            p_desc = pod.get("desc", "")
            icon_key = pod.get("icon", p_title)

            ang = pod_angles[i]
            rad = math.radians(ang)
            pod_cx = nucleus_cx + (380 * math.cos(rad))
            pod_cy = nucleus_cy + (380 * math.sin(rad))

            svg.append(f'<g id="orbit_planet_{i+1}">')
            # Connecting Ray
            svg.append(f'<line x1="{nucleus_cx}" y1="{nucleus_cy}" x2="{pod_cx}" y2="{pod_cy}" stroke="{self.theme["primary"]}" stroke-width="2.5" stroke-dasharray="6 6" stroke-opacity="0.6" />')

            # Rotating Halo
            svg.append(f'<g id="spin_planet_halo_{i+1}">')
            svg.append(f'<circle cx="{pod_cx}" cy="{pod_cy}" r="115" fill="none" stroke="{self.theme["secondary"]}" stroke-width="1.8" stroke-dasharray="6 4" stroke-opacity="0.5" />')
            svg.append(f'<circle cx="{pod_cx + 115}" cy="{pod_cy}" r="4" fill="{self.theme["accent"]}" />')
            svg.append('</g>')

            # Circular Planet Pod Body
            svg.append(f'<circle cx="{pod_cx}" cy="{pod_cy}" r="96" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            svg.append(get_icon_svg_content(icon_key, pod_cx - 22, pod_cy - 50, size=44, stroke_color=self.theme["secondary"]))
            svg.append(f'<text x="{pod_cx}" y="{pod_cy + 15}" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="middle">{escape_xml(p_title)}</text>')
            
            # Short bullet or first line
            first_line = p_desc.split("\n")[0] if p_desc else ""
            if first_line:
                svg.append(f'<text x="{pod_cx}" y="{pod_cy + 42}" font-family="{font}" font-size="16" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="middle">{escape_xml(first_line[:24])}</text>')

            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_split_image_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None, slide_idx: int = 7) -> str:
        """Slidesgo Split Feature Showcase with Circular Icon Badges."""
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "بررسی تخصصی")
        bullets = slide.get("bullets", [])
        rtl = is_persian(title) or any(is_persian(str(b)) for b in bullets)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        header_x = 1800 if rtl else 120

        svg = [self._header_svg(rtl, slide_idx=slide_idx)]

        # Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{header_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{header_x}" y="165" font-family="{font}" font-size="48" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        content_x = 940 if rtl else 120
        content_w = 860
        image_x = 120 if rtl else 1060
        image_w = 740
        image_y = 230
        image_h = 700

        # Bullet List Group
        svg.append('<g id="bullets_group">')
        curr_y = 260
        for i, bullet in enumerate(bullets):
            # Style-aware Horizontal Pod
            svg.extend(self._card_rect(content_x, curr_y, content_w, 120, rx=30, stroke_width=2.0, top_accent=False))
            
            # Circular Icon Pod
            circle_x = (content_x + content_w - 65) if rtl else (content_x + 65)
            svg.append(f'<circle cx="{circle_x}" cy="{curr_y+60}" r="34" fill="{self.theme["badge_bg"]}" stroke="{self.theme["primary"]}" stroke-width="2" />')
            svg.append(get_icon_svg_content("check", circle_x - 17, curr_y + 43, size=34, stroke_color=self.theme["primary"]))

            tx = (content_x + content_w - 120) if rtl else (content_x + 120)
            if isinstance(bullet, dict):
                b_title = bullet.get("title", "")
                b_desc = bullet.get("desc", "")
                svg.append(f'<text x="{tx}" y="{curr_y+50}" font-family="{font}" font-size="24" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(b_title)}</text>')
                svg.append(f'<text x="{tx}" y="{curr_y+85}" font-family="{font}" font-size="19" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(b_desc)}</text>')
            else:
                svg.append(f'<text x="{tx}" y="{curr_y+68}" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(str(bullet))}</text>')

            curr_y += 140
        svg.append('</g>')

        # Image Showcase Frame
        svg.append('<g id="hero_image">')
        if self.archetype == "neo_brutalist":
            shadow_img = "#000000" if not self.is_dark else self.theme.get("primary", "#A3E635")
            svg.append(f'<rect x="{image_x+8}" y="{image_y+8}" width="{image_w}" height="{image_h}" rx="18" fill="{shadow_img}" />')
            svg.append(f'<rect x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" rx="18" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3.5" />')
        else:
            svg.append(f'<rect x="{image_x-6}" y="{image_y-6}" width="{image_w+12}" height="{image_h+12}" rx="36" fill="none" stroke="{self.theme["primary"]}" stroke-width="2" stroke-opacity="0.35" />')
            svg.append(f'<rect x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" rx="32" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="2.5" />')
        if image_rel_path:
            svg.append(f'<image href="{image_rel_path}" x="{image_x+10}" y="{image_y+10}" width="{image_w-20}" height="{image_h-20}" preserveAspectRatio="xMidYMid slice" />')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


def generate_deck_animations_config(project_dir: Path, transition: str = "morph", animation_mode: str = "auto") -> Dict[str, Any]:
    """
    Generate animations.json configuration that assigns infinite continuous motion
    (emphasis_spin with 999 repetitions) to all particle clusters, orbital rings, dials,
    and archetype-specific badges/compasses, while keeping titles and content on staggered entrance animations.
    """
    from svg_to_pptx.animation_config import scan_project_targets
    targets_by_slide, _ = scan_project_targets(project_dir)
    slides_cfg: Dict[str, Any] = {}
    for slide_stem, targets in targets_by_slide.items():
        slide_groups: Dict[str, Any] = {}
        for target in targets:
            gid = target.group_id
            if gid.startswith("spin_"):
                # Harmonious continuous rotational velocity based on archetype geometry
                if "particle" in gid:
                    dur = 12.0
                elif "dial" in gid or "vs" in gid:
                    dur = 4.0
                elif "compass" in gid or "royal" in gid:
                    dur = 16.0
                elif "badge" in gid:
                    dur = 6.0
                elif "sun" in gid or "orbit" in gid or "hero" in gid or "galaxy" in gid or "halo" in gid:
                    dur = 8.0
                else:
                    dur = 7.0
                slide_groups[gid] = {
                    "effect": "emphasis_spin",
                    "duration": dur,
                    "trigger": "with-previous",
                    "repeat_count": 999
                }
        slides_cfg[slide_stem] = {
            "groups": slide_groups
        }
    return {
        "version": 1,
        "defaults": {
            "transition": {
                "effect": transition,
                "duration": 0.5
            },
            "animation": {
                "effect": animation_mode,
                "duration": 0.5,
                "stagger": 0.35,
                "trigger": "after-previous"
            }
        },
        "slides": slides_cfg
    }


def generate_presentation_project(
    deck_data: Dict[str, Any],
    project_dir: Path,
    output_pptx: Optional[Path] = None,
    theme_key: str = "cyber_aurora",
    transition: str = "morph",
    animation_mode: str = "auto"
) -> Path:
    """
    Generate complete SVG deck, notes, and compile to native PPTX with intelligent Morph transitions
    and continuous looping particle & orbit animations.
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

    print(f"Creating rich, non-minimalist circular & particle presentation with {len(slides)} slides...")

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
        elif layout == "circular_orbit":
            svg_content = renderer.render_circular_orbit_slide(slide, slide_idx=idx)
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

    # Write animations.json for infinite continuous particle & orbit motion
    anim_cfg = generate_deck_animations_config(project_dir, transition=transition, animation_mode=animation_mode)
    anim_config_path = project_dir / "animations.json"
    with open(anim_config_path, "w", encoding="utf-8") as f:
        json.dump(anim_cfg, f, ensure_ascii=False, indent=2)

    # Destination PPTX path
    if output_pptx is None:
        deck_title = re.sub(r'[^a-zA-Z0-9_\u0600-\u06FF]', '_', deck_data.get("title", "presentation")).strip("_")
        output_pptx = exports_dir / f"{deck_title}.pptx"
    else:
        output_pptx = Path(output_pptx).resolve()

    # Compile to native PowerPoint PPTX
    print(f"Compiling slides to native PPTX with transitions ({transition}) and continuous looping animations ({animation_mode})...")
    from svg_to_pptx import main as svg_main
    orig_argv = sys.argv[:]
    try:
        sys.argv = [
            "svg_to_pptx",
            str(project_dir),
            "-o", str(output_pptx),
            "-t", transition,
            "-a", animation_mode,
            "--animation-trigger", "after-previous",
            "--animation-stagger", "0.35"
        ]
        ret = svg_main()
        if ret not in (0, None):
            raise RuntimeError(f"PPTX compilation failed with code {ret}")
    finally:
        sys.argv = orig_argv

    print(f"Presentation successfully generated: {output_pptx}")
    return output_pptx


def fetch_or_create_placeholder(query: str, images_dir: Path, filename: str, theme: str = "technology") -> Path:
    """Fetch high-resolution image from Unsplash or create rich gradient canvas."""
    target = images_dir / filename
    if target.exists() and target.stat().st_size > 1000:
        return target

    try:
        import urllib.request
        clean_query = re.sub(r'[^a-zA-Z0-9]', '+', query).strip('+')
        if not clean_query:
            clean_query = "technology+futuristic"
        url = f"https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1280&q=80&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            with open(target, 'wb') as f:
                f.write(response.read())
        return target
    except Exception:
        pass

    # Fallback to high-grade gradient canvas
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1280, 800), color=(14, 24, 48))
        draw = ImageDraw.Draw(img)
        for i in range(800):
            r = int(14 + (i / 800) * 20)
            g = int(24 + (i / 800) * 40)
            b = int(48 + (i / 800) * 80)
            draw.line([(0, i), (1280, i)], fill=(r, g, b))
        img.save(target, format='JPEG', quality=90)
    except Exception:
        target.write_bytes(b"")
    return target


def main():
    parser = argparse.ArgumentParser(description="PPT Master - Native Presentation Generator v3.1")
    parser.add_argument("deck_json", type=Path, help="Path to input presentation JSON specification")
    parser.add_argument("-p", "--project-dir", type=Path, default=Path("project_run"), help="Project directory")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output PPTX path")
    parser.add_argument("--theme", type=str, default="cyber_aurora", help="Theme key")
    parser.add_argument("-t", "--transition", type=str, default="morph", help="Transition effect (default: morph)")
    parser.add_argument("-a", "--animation", type=str, default="auto", help="Animation mode (default: auto)")

    args = parser.parse_args()

    with open(args.deck_json, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    out_file = generate_presentation_project(
        deck_data=deck_data,
        project_dir=args.project_dir,
        output_pptx=args.output,
        theme_key=args.theme,
        transition=args.transition,
        animation_mode=args.animation
    )
    print(f"Done: {out_file}")


if __name__ == "__main__":
    main()
