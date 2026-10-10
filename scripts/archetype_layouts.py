#!/usr/bin/env python3
"""
PPT Master - Multi-Archetype Layout Engine (v4.0)

Implements completely distinct visual architectures, layout construction,
and geometric components for each of the 6 art styles:
  1. Bento Grid (Apple Keynote / Vercel): Asymmetrical modular mosaic, rounded frosted glass.
  2. Swiss Academic (Müller-Brockmann): Rigid scientific grid, stepped chevrons, clinical data tables.
  3. Neo-Brutalist (Gumroad / Figma): Tilted marquee stickers, chunky 4px borders, hard black offset shadows.
  4. Warm Editorial (Kinfolk / Architectural): Arched cathedral windows, faint background serif numerals, botanical motifs.
  5. Royal Gold Noir (Art Deco / Luxury): Beveled clipped-corner octagon pedestals, gold pinstripe filigree, diamond crests.
  6. Cyber HUD (Sci-Fi / Telemetry): Chamfered tech consoles, HUD radar reticles, circular sweep dials.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional
from icon_mapper import get_icon_svg_content


def is_persian(text: str) -> bool:
    import re
    return bool(re.search(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def to_persian_digits(num: int | str) -> str:
    s = str(num)
    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    en_digits = "0123456789"
    return s.translate(str.maketrans(en_digits, fa_digits))


def escape_xml(s: str) -> str:
    if not s:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# ==============================================================================
# 1. APPLE BENTO-GRID ARCHITECTURE (Asymmetric Modular Glass Mosaic)
# ==============================================================================

class BentoGridRenderer:
    """Asymmetrical modular glass cards, sleek rounded bento mosaic, ambient glowing orbs."""

    @staticmethod
    def render_pillars(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Asymmetric Bento Mosaic: 1 Large Master Hero Card + 2 Stacked Modular Mini-Cards."""
        title = slide.get("title", "ستون‌های اصلی سیستم")
        kicker = slide.get("kicker", "معماری ماژولار بنتو")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<rect x="{title_x - 180 if rtl else title_x}" y="80" width="180" height="34" rx="17" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.2" />')
        svg.append(f'<text x="{title_x - 90 if rtl else title_x + 90}" y="103" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_count = len(cards)
        c0 = cards[0] if card_count > 0 else {"title": "ویژگی اصلی", "desc": "توضیحات"}
        c1 = cards[1] if card_count > 1 else {"title": "ماژول دوم", "desc": "توضیحات"}
        c2 = cards[2] if card_count > 2 else {"title": "ماژول سوم", "desc": "توضیحات"}

        hero_w = 980
        hero_h = 700
        hero_y = 230
        hero_x = 820 if rtl else 120

        stack_w = 680
        stack_h = 330
        stack_x = 120 if rtl else 1120
        stack_y1 = 230
        stack_y2 = 600

        # Master Bento Hero Card
        svg.append('<g id="bento_hero_card">')
        svg.append(f'<rect x="{hero_x}" y="{hero_y}" width="{hero_w}" height="{hero_h}" rx="32" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')
        svg.append(f'<rect x="{hero_x + 30}" y="{hero_y}" width="{hero_w - 60}" height="3" rx="1.5" fill="{renderer.theme["primary"]}" />')
        
        hero_icon = c0.get("icon", c0.get("title", "cpu"))
        icon_cx = (hero_x + hero_w - 90) if rtl else (hero_x + 90)
        svg.append(f'<circle cx="{icon_cx}" cy="{hero_y + 90}" r="45" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')
        svg.append(get_icon_svg_content(hero_icon, icon_cx - 24, hero_y + 66, size=48, stroke_color=renderer.theme["primary"]))

        tag_x = (hero_x + 40) if rtl else (hero_x + hero_w - 180)
        svg.append(f'<rect x="{tag_x}" y="{hero_y + 70}" width="140" height="38" rx="19" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["secondary"]}" stroke-width="1.5" />')
        tag_num = to_persian_digits("01 // FEATURE MASTER") if rtl else "01 // HERO SPEC"
        svg.append(f'<text x="{tag_x + 70}" y="{hero_y + 95}" font-family="{font}" font-size="14" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">{tag_num}</text>')

        tx_hero = (hero_x + hero_w - 60) if rtl else (hero_x + 60)
        svg.append(f'<text x="{tx_hero}" y="{hero_y + 190}" font-family="{font}" font-size="34" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(c0.get("title", ""))}</text>')

        desc_lines = c0.get("desc", "").split("\n")
        curr_y = hero_y + 260
        for l in desc_lines[:8]:
            if l.strip():
                dot_x = (tx_hero - 8) if rtl else (tx_hero + 8)
                txt_x = (tx_hero - 32) if rtl else (tx_hero + 32)
                svg.append(f'<circle cx="{dot_x}" cy="{curr_y - 6}" r="5" fill="{renderer.theme["primary"]}" />')
                svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                curr_y += 50
        svg.append('</g>')

        # Stacked Bento Mini-Card 1
        svg.append('<g id="bento_mini_1">')
        svg.append(f'<rect x="{stack_x}" y="{stack_y1}" width="{stack_w}" height="{stack_h}" rx="28" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.8" />')
        m1_icon = c1.get("icon", c1.get("title", "database"))
        m1_cx = (stack_x + stack_w - 65) if rtl else (stack_x + 65)
        svg.append(f'<circle cx="{m1_cx}" cy="{stack_y1 + 65}" r="32" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["secondary"]}" stroke-width="2" />')
        svg.append(get_icon_svg_content(m1_icon, m1_cx - 18, stack_y1 + 47, size=36, stroke_color=renderer.theme["secondary"]))
        
        m1_tx = (stack_x + stack_w - 120) if rtl else (stack_x + 120)
        svg.append(f'<text x="{m1_tx}" y="{stack_y1 + 72}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(c1.get("title", ""))}</text>')
        
        m1_lines = c1.get("desc", "").split("\n")
        my = stack_y1 + 130
        for l in m1_lines[:3]:
            if l.strip():
                svg.append(f'<text x="{m1_tx}" y="{my}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                my += 36
        svg.append('</g>')

        # Stacked Bento Mini-Card 2
        svg.append('<g id="bento_mini_2">')
        svg.append(f'<rect x="{stack_x}" y="{stack_y2}" width="{stack_w}" height="{stack_h}" rx="28" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.8" />')
        m2_icon = c2.get("icon", c2.get("title", "shield"))
        m2_cx = (stack_x + stack_w - 65) if rtl else (stack_x + 65)
        svg.append(f'<circle cx="{m2_cx}" cy="{stack_y2 + 65}" r="32" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["accent"]}" stroke-width="2" />')
        svg.append(get_icon_svg_content(m2_icon, m2_cx - 18, stack_y2 + 47, size=36, stroke_color=renderer.theme["accent"]))
        
        m2_tx = (stack_x + stack_w - 120) if rtl else (stack_x + 120)
        svg.append(f'<text x="{m2_tx}" y="{stack_y2 + 72}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(c2.get("title", ""))}</text>')
        
        m2_lines = c2.get("desc", "").split("\n")
        my = stack_y2 + 130
        for l in m2_lines[:3]:
            if l.strip():
                svg.append(f'<text x="{m2_tx}" y="{my}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                my += 36
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_process_steps(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Bento Staggered Milestone Stream with frosted glass connector bar."""
        title = slide.get("title", "فرآیند پیاده‌سازی ماژولار")
        kicker = slide.get("kicker", "نقشه راه مرحله‌ای بنتو")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 120
        gap = 36
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count

        # Staggered Card Heights
        heights = [560, 620, 560, 600]
        y_offsets = [310, 270, 310, 280]

        # Horizontal glowing frosted glass connector track
        svg.append(f'<rect x="{margin + 60}" y="280" width="{renderer.width - (2 * margin) - 120}" height="8" rx="4" fill="{renderer.theme["surface_border"]}" fill-opacity="0.4" />')
        svg.append(f'<rect x="{margin + 60}" y="280" width="{renderer.width - (2 * margin) - 120}" height="4" rx="2" fill="{renderer.theme["primary"]}" fill-opacity="0.7" />')

        for i, step in enumerate(steps):
            s_title = step.get("title", f"مرحله {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            c_h = heights[i % len(heights)]
            c_y = y_offsets[i % len(y_offsets)]

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="bento_step_{i+1}">')
            svg.append(f'<rect x="{c_x}" y="{c_y}" width="{card_w}" height="{c_h}" rx="28" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')
            
            # Step Counter Pill
            num_str = to_persian_digits(f"0{i+1}") if rtl else f"0{i+1}"
            pill_x = (c_x + card_w - 150) if rtl else (c_x + 30)
            svg.append(f'<rect x="{pill_x}" y="{c_y + 30}" width="120" height="34" rx="17" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')
            svg.append(f'<text x="{pill_x + 60}" y="{c_y + 53}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="middle">STAGE {num_str}</text>')

            # Icon Box
            icon_cx = (c_x + 60) if rtl else (c_x + card_w - 60)
            svg.append(f'<circle cx="{icon_cx}" cy="{c_y + 47}" r="28" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["secondary"]}" stroke-width="1.8" />')
            svg.append(get_icon_svg_content(icon_key, icon_cx - 16, c_y + 31, size=32, stroke_color=renderer.theme["secondary"]))

            # Title
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            svg.append(f'<text x="{tx}" y="{c_y + 125}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(s_title)}</text>')

            # Verbatim Description
            desc_lines = s_desc.split("\n")
            curr_y = c_y + 185
            for l in desc_lines[:7]:
                if l.strip():
                    svg.append(f'<circle cx="{(tx - 8) if rtl else (tx + 8)}" cy="{curr_y - 6}" r="4" fill="{renderer.theme["secondary"]}" />')
                    svg.append(f'<text x="{(tx - 26) if rtl else (tx + 26)}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 44
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_stats_kpi(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        """Bento Stat Mosaic: 1 Giant Primary KPI Hero Tile + 2 Modular Metric Pods."""
        title = slide.get("title", "شاخص‌های کلیدی و رشد عملکرد")
        kicker = slide.get("kicker", "داشبورد تحلیلی بنتو")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        k0 = kpis[0] if len(kpis) > 0 else {"number": "+85%", "title": "شاخص اصلی", "desc": "رشد", "trend": "↑ رشد"}
        k1 = kpis[1] if len(kpis) > 1 else {"number": "4.2x", "title": "شاخص دوم", "desc": "افزایش سرعت", "trend": "↑ ۲ برابر"}
        k2 = kpis[2] if len(kpis) > 2 else {"number": "99.9%", "title": "شاخص سوم", "desc": "پایداری", "trend": "✓ بهینه"}

        hero_w = 980
        hero_h = 700
        hero_y = 230
        hero_x = 820 if rtl else 120

        stack_w = 680
        stack_h = 330
        stack_x = 120 if rtl else 1120
        stack_y1 = 230
        stack_y2 = 600

        # Giant Bento KPI Hero Card
        svg.append('<g id="bento_kpi_hero">')
        svg.append(f'<rect x="{hero_x}" y="{hero_y}" width="{hero_w}" height="{hero_h}" rx="32" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')
        
        # Giant 120px Stat Numeral
        num_val0 = k0.get("number", k0.get("val", "+85%"))
        tx_hero = (hero_x + hero_w - 70) if rtl else (hero_x + 70)
        svg.append(f'<text x="{tx_hero}" y="{hero_y + 190}" font-family="{font}" font-size="120" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(num_val0)}</text>')

        # Trend pill next to hero
        trend0 = k0.get("trend", "↑ رکورد جدید")
        svg.append(f'<rect x="{hero_x + 70 if rtl else hero_x + hero_w - 250}" y="{hero_y + 110}" width="180" height="44" rx="22" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["accent"]}" stroke-width="2" />')
        svg.append(f'<text x="{hero_x + 160 if rtl else hero_x + hero_w - 160}" y="{hero_y + 138}" font-family="{font}" font-size="18" font-weight="700" fill="{renderer.theme["accent"]}" text-anchor="middle">{escape_xml(trend0)}</text>')

        # Title & Description
        svg.append(f'<text x="{tx_hero}" y="{hero_y + 270}" font-family="{font}" font-size="34" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(k0.get("title", ""))}</text>')
        desc0_lines = k0.get("desc", "").split("\n")
        dy = hero_y + 340
        for l in desc0_lines[:6]:
            if l.strip():
                svg.append(f'<text x="{tx_hero}" y="{dy}" font-family="{font}" font-size="22" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                dy += 44
        svg.append('</g>')

        # Secondary KPI Pod 1
        svg.append('<g id="bento_kpi_pod_1">')
        svg.append(f'<rect x="{stack_x}" y="{stack_y1}" width="{stack_w}" height="{stack_h}" rx="28" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.8" />')
        stx = (stack_x + stack_w - 50) if rtl else (stack_x + 50)
        svg.append(f'<text x="{stx}" y="{stack_y1 + 105}" font-family="{font}" font-size="64" font-weight="900" fill="{renderer.theme["secondary"]}" text-anchor="{align}">{escape_xml(k1.get("number", k1.get("val", "4.2x")))}</text>')
        svg.append(f'<text x="{stx}" y="{stack_y1 + 165}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(k1.get("title", ""))}</text>')
        if k1.get("desc"):
            svg.append(f'<text x="{stx}" y="{stack_y1 + 215}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(k1.get("desc", ""))}</text>')
        # Progress Bar Track
        svg.append(f'<rect x="{stack_x + 40}" y="{stack_y1 + 265}" width="{stack_w - 80}" height="12" rx="6" fill="{renderer.theme["surface_border"]}" />')
        svg.append(f'<rect x="{stack_x + 40}" y="{stack_y1 + 265}" width="{(stack_w - 80) * 0.75}" height="12" rx="6" fill="{renderer.theme["secondary"]}" />')
        svg.append('</g>')

        # Secondary KPI Pod 2
        svg.append('<g id="bento_kpi_pod_2">')
        svg.append(f'<rect x="{stack_x}" y="{stack_y2}" width="{stack_w}" height="{stack_h}" rx="28" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.8" />')
        svg.append(f'<text x="{stx}" y="{stack_y2 + 105}" font-family="{font}" font-size="64" font-weight="900" fill="{renderer.theme["accent"]}" text-anchor="{align}">{escape_xml(k2.get("number", k2.get("val", "99.9%")))}</text>')
        svg.append(f'<text x="{stx}" y="{stack_y2 + 165}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(k2.get("title", ""))}</text>')
        if k2.get("desc"):
            svg.append(f'<text x="{stx}" y="{stack_y2 + 215}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(k2.get("desc", ""))}</text>')
        # Progress Bar Track
        svg.append(f'<rect x="{stack_x + 40}" y="{stack_y2 + 265}" width="{stack_w - 80}" height="12" rx="6" fill="{renderer.theme["surface_border"]}" />')
        svg.append(f'<rect x="{stack_x + 40}" y="{stack_y2 + 265}" width="{(stack_w - 80) * 0.92}" height="12" rx="6" fill="{renderer.theme["accent"]}" />')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_comparison(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Asymmetric Bento Glass Comparison Matrix."""
        title = slide.get("title", "مقایسه معماری سنتی و نسل بعد")
        kicker = slide.get("kicker", "ارزیابی چندلایه")
        col_a = slide.get("col_a", {})
        col_b = slide.get("col_b", {})
        rtl = is_persian(title) or any(is_persian(str(x)) for x in col_a.get("items", []))
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 800
        card_h = 700
        ca_x = 1000 if rtl else 120
        cb_x = 120 if rtl else 1000
        card_y = 230

        # Column A (Legacy)
        svg.append('<g id="bento_comp_a">')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="32" fill="{renderer.theme["surface"]}" stroke="#EF4444" stroke-width="1.8" stroke-opacity="0.6" />')
        svg.append(f'<rect x="{ca_x + 50}" y="{card_y + 40}" width="160" height="36" rx="18" fill="{renderer.theme["badge_bg"]}" stroke="#EF4444" stroke-width="1.5" />')
        svg.append(f'<text x="{ca_x + 130}" y="{card_y + 64}" font-family="{font}" font-size="16" font-weight="700" fill="#EF4444" text-anchor="middle">LEGACY SYSTEM</text>')
        svg.append(f'<text x="{ca_x + card_w - 60 if rtl else ca_x + 60}" y="{card_y + 130}" font-family="{font}" font-size="30" font-weight="700" fill="#EF4444" text-anchor="{align}">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        
        curr_y = card_y + 200
        tx_a = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(get_icon_svg_content("x", (tx_a - 32) if rtl else tx_a, curr_y - 18, size=24, stroke_color="#EF4444"))
            svg.append(f'<text x="{(tx_a - 46) if rtl else (tx_a + 40)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        # Column B (Next-Gen Pro)
        svg.append('<g id="bento_comp_b">')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="32" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
        svg.append(f'<rect x="{cb_x + 50}" y="{card_y + 40}" width="170" height="36" rx="18" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')
        svg.append(f'<text x="{cb_x + 135}" y="{card_y + 64}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="middle">PRO NEXT-GEN</text>')
        svg.append(f'<text x="{cb_x + card_w - 60 if rtl else cb_x + 60}" y="{card_y + 130}" font-family="{font}" font-size="30" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">✦ {escape_xml(col_b.get("title", "هوشمند"))}</text>')

        curr_y = card_y + 200
        tx_b = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(get_icon_svg_content("check", (tx_b - 32) if rtl else tx_b, curr_y - 18, size=24, stroke_color=renderer.theme["primary"]))
            svg.append(f'<text x="{(tx_b - 46) if rtl else (tx_b + 40)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        # Central Floating Glass Pill VS
        svg.append('<g id="bento_vs_pill">')
        svg.append(f'<rect x="910" y="550" width="100" height="50" rx="25" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')
        svg.append(f'<text x="960" y="582" font-family="{font}" font-size="22" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="middle">VS</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


# ==============================================================================
# 2. SWISS ACADEMIC ARCHITECTURE (Stepped Chevron Pipeline & Clinical Matrix)
# ==============================================================================

class SwissAcademicRenderer:
    """Rigid scientific grid, horizontal chevron phase pipeline, clinical tables."""

    @staticmethod
    def render_pillars(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Structured Scientific Parameter Matrix with sharp top color rules and Roman numerals."""
        title = slide.get("title", "محورهای پژوهش و شاخص‌های تحلیلی")
        kicker = slide.get("kicker", "گزارش علمی و بالینی")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="monospace" font-size="14" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="{align}">[SECTION_02 // SYSTEMATIC_REVIEW]</text>')
        svg.append(f'<text x="{title_x}" y="150" font-family="{font}" font-size="44" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(cards))
        margin = 120
        gap = 30
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count
        card_y = 220
        card_h = 720

        roman_numerals = ["I", "II", "III", "IV", "V"]

        for i, card in enumerate(cards):
            c_title = card.get("title", f"شاخص {i+1}")
            c_desc = card.get("desc", "")
            icon_key = card.get("icon", c_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="swiss_card_{i+1}">')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="8" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.2" />')
            bar_color = renderer.theme["primary"] if i % 2 == 0 else renderer.theme["secondary"]
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="5" fill="{bar_color}" />')

            num_str = roman_numerals[i % len(roman_numerals)]
            tx = (c_x + card_w - 36) if rtl else (c_x + 36)
            svg.append(f'<text x="{tx}" y="{card_y + 45}" font-family="monospace" font-size="20" font-weight="700" fill="{bar_color}" text-anchor="{align}">PHASE {num_str}</text>')
            
            icon_x = (c_x + 36) if rtl else (c_x + card_w - 76)
            svg.append(f'<rect x="{icon_x}" y="{card_y + 25}" width="40" height="40" rx="4" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1" />')
            svg.append(get_icon_svg_content(icon_key, icon_x + 6, card_y + 31, size=28, stroke_color=bar_color))

            svg.append(f'<line x1="{c_x + 20}" y1="{card_y + 80}" x2="{c_x + card_w - 20}" y2="{card_y + 80}" stroke="{renderer.theme["surface_border"]}" stroke-width="0.8" stroke-opacity="0.6" />')

            svg.append(f'<text x="{tx}" y="{card_y + 125}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(c_title)}</text>')

            desc_lines = c_desc.split("\n")
            curr_y = card_y + 185
            for l in desc_lines[:9]:
                clean_l = l.strip()
                if clean_l:
                    dash_x = (tx - 4) if rtl else (tx + 4)
                    body_x = (tx - 24) if rtl else (tx + 24)
                    svg.append(f'<text x="{dash_x}" y="{curr_y}" font-family="monospace" font-size="18" font-weight="700" fill="{bar_color}" text-anchor="{align}">—</text>')
                    svg.append(f'<text x="{body_x}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 46
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


    @staticmethod
    def render_process_steps(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Horizontal Stepped Chevron Phase Pipeline with crisp clinical connectors."""
        title = slide.get("title", "فازبندی اجرایی و پروتکل علمی")
        kicker = slide.get("kicker", "نقشه راه سیستماتیک")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Scientific Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="monospace" font-size="14" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="{align}">[SECTION_03 // METHODOLOGY_PIPELINE]</text>')
        svg.append(f'<text x="{title_x}" y="150" font-family="{font}" font-size="44" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 120
        gap = 24
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        step_w = total_w / count
        chevron_h = 680
        c_y = 230

        for i, step in enumerate(steps):
            s_title = step.get("title", f"فاز {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * step_w) - (i * gap)
            else:
                c_x = margin + (i * (step_w + gap))

            svg.append(f'<g id="swiss_chevron_{i+1}">')
            # Clinical Card with Top Phase Header
            svg.append(f'<rect x="{c_x}" y="{c_y}" width="{step_w}" height="{chevron_h}" rx="6" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.2" />')
            
            # Phase Colored Header Block
            p_col = renderer.theme["secondary"] if i % 2 == 0 else renderer.theme["primary"]
            svg.append(f'<rect x="{c_x}" y="{c_y}" width="{step_w}" height="55" fill="{p_col}" />')
            
            phase_code = f"PHASE 0{i+1}"
            p_tx = (c_x + step_w - 20) if rtl else (c_x + 20)
            p_align = "end" if rtl else "start"
            svg.append(f'<text x="{p_tx}" y="{c_y + 35}" font-family="monospace" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="{p_align}">{phase_code}</text>')

            # Icon in square badge
            ic_x = (c_x + 20) if rtl else (c_x + step_w - 45)
            svg.append(get_icon_svg_content(icon_key, ic_x, c_y + 15, size=26, stroke_color="#FFFFFF"))

            # Phase Title
            tx = (c_x + step_w - 30) if rtl else (c_x + 30)
            svg.append(f'<text x="{tx}" y="{c_y + 115}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(s_title)}</text>')

            # Horizontal Rule
            svg.append(f'<line x1="{c_x + 20}" y1="{c_y + 140}" x2="{c_x + step_w - 20}" y2="{c_y + 140}" stroke="{renderer.theme["surface_border"]}" stroke-width="1" />')

            # Verbatim Parameters with square bullets
            desc_lines = s_desc.split("\n")
            curr_y = c_y + 195
            for l in desc_lines[:8]:
                if l.strip():
                    sq_x = (tx - 8) if rtl else tx
                    svg.append(f'<rect x="{sq_x}" y="{curr_y - 12}" width="6" height="6" fill="{p_col}" />')
                    svg.append(f'<text x="{(tx - 24) if rtl else (tx + 20)}" y="{curr_y}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_stats_kpi(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        """Clinical Scientific Data Matrix with sample sizes and confidence intervals."""
        title = slide.get("title", "تحلیل داده‌های آماری و نتایج کارآزمایی")
        kicker = slide.get("kicker", "شواهد کمی و یافته‌های بالینی")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="monospace" font-size="14" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="{align}">[EVIDENCE_LEVEL // LEVEL_1A_META_ANALYSIS]</text>')
        svg.append(f'<text x="{title_x}" y="150" font-family="{font}" font-size="44" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(kpis))
        margin = 120
        gap = 30
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 230
        card_h = 700

        for i, kpi in enumerate(kpis):
            num_val = kpi.get("number", kpi.get("val", "+85%"))
            k_label = kpi.get("title", kpi.get("label", ""))
            k_desc = kpi.get("desc", "")
            trend = kpi.get("trend", "Δ +14.2% (p < 0.001)")

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="swiss_kpi_{i+1}">')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="6" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.2" />')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="4" fill="{renderer.theme["secondary"]}" />')

            tx = (c_x + card_w - 30) if rtl else (c_x + 30)
            
            # Scientific Statistical Numeral
            svg.append(f'<text x="{tx}" y="{card_y + 110}" font-family="{font}" font-size="78" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(num_val)}</text>')

            # Statistical Confidence Interval Badge
            svg.append(f'<text x="{tx}" y="{card_y + 155}" font-family="monospace" font-size="16" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="{align}">[95% CI: 1.14 - 2.85 | {escape_xml(trend)}]</text>')

            # Rule line
            svg.append(f'<line x1="{c_x + 20}" y1="{card_y + 185}" x2="{c_x + card_w - 20}" y2="{card_y + 185}" stroke="{renderer.theme["surface_border"]}" stroke-width="1" />')

            # Metric Label
            svg.append(f'<text x="{tx}" y="{card_y + 235}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(k_label)}</text>')

            # Verbatim Description
            desc_lines = k_desc.split("\n")
            curr_y = card_y + 295
            for l in desc_lines[:6]:
                if l.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 44

            # Clinical Target Horizontal Bar
            svg.append(f'<rect x="{c_x + 25}" y="{card_y + card_h - 60}" width="{card_w - 50}" height="8" rx="4" fill="{renderer.theme["surface_border"]}" />')
            svg.append(f'<rect x="{c_x + 25}" y="{card_y + card_h - 60}" width="{(card_w - 50) * 0.85}" height="8" rx="4" fill="{renderer.theme["primary"]}" />')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_comparison(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Rigid Scientific Comparative Trial Matrix with clinical criteria."""
        title = slide.get("title", "تحلیل تطبیقی و اعتبارسنجی بالینی")
        kicker = slide.get("kicker", "مقایسه روش‌های کنترل و مداخله")
        col_a = slide.get("col_a", {})
        col_b = slide.get("col_b", {})
        rtl = is_persian(title) or any(is_persian(str(x)) for x in col_a.get("items", []))
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="monospace" font-size="14" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="{align}">[EVALUATION // COMPARATIVE_STUDY_MATRIX]</text>')
        svg.append(f'<text x="{title_x}" y="150" font-family="{font}" font-size="44" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 780
        card_h = 700
        ca_x = 1020 if rtl else 120
        cb_x = 120 if rtl else 1020
        card_y = 230

        # Col A (Control / Conventional)
        svg.append('<g id="swiss_comp_a">')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="6" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.2" />')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="55" fill="{renderer.theme["surface_border"]}" fill-opacity="0.5" />')
        svg.append(f'<text x="{ca_x + 30}" y="{card_y + 35}" font-family="monospace" font-size="15" font-weight="700" fill="{renderer.theme["text_muted"]}">[ARM A // CONVENTIONAL_STANDARD]</text>')
        svg.append(f'<text x="{ca_x + card_w - 30 if rtl else ca_x + 30}" y="{card_y + 115}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(col_a.get("title", "روش مرسوم"))}</text>')
        svg.append(f'<line x1="{ca_x + 20}" y1="{card_y + 145}" x2="{ca_x + card_w - 20}" y2="{card_y + 145}" stroke="{renderer.theme["surface_border"]}" stroke-width="1" />')

        curr_y = card_y + 205
        tx_a = (ca_x + card_w - 40) if rtl else (ca_x + 40)
        for item in col_a.get("items", []):
            svg.append(f'<text x="{(tx_a - 6) if rtl else (tx_a + 6)}" y="{curr_y}" font-family="monospace" font-size="16" font-weight="700" fill="#EF4444" text-anchor="{align}">[—]</text>')
            svg.append(f'<text x="{(tx_a - 34) if rtl else (tx_a + 34)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 68
        svg.append('</g>')

        # Col B (Intervention / Proposed Pro)
        svg.append('<g id="swiss_comp_b">')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="6" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.8" />')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="55" fill="{renderer.theme["primary"]}" />')
        svg.append(f'<text x="{cb_x + 30}" y="{card_y + 35}" font-family="monospace" font-size="15" font-weight="700" fill="#FFFFFF">[ARM B // NOVEL_INTERVENTION_OPTIMAL]</text>')
        svg.append(f'<text x="{cb_x + card_w - 30 if rtl else cb_x + 30}" y="{card_y + 115}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">★ {escape_xml(col_b.get("title", "راهکار نوین"))}</text>')
        svg.append(f'<line x1="{cb_x + 20}" y1="{card_y + 145}" x2="{cb_x + card_w - 20}" y2="{card_y + 145}" stroke="{renderer.theme["surface_border"]}" stroke-width="1" />')

        curr_y = card_y + 205
        tx_b = (cb_x + card_w - 40) if rtl else (cb_x + 40)
        for item in col_b.get("items", []):
            svg.append(f'<text x="{(tx_b - 6) if rtl else (tx_b + 6)}" y="{curr_y}" font-family="monospace" font-size="16" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">[✓]</text>')
            svg.append(f'<text x="{(tx_b - 34) if rtl else (tx_b + 34)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 68
        svg.append('</g>')

        # Center Statistical Delta Divider
        svg.append('<g id="swiss_delta_pill">')
        svg.append(f'<rect x="915" y="550" width="90" height="46" rx="4" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["secondary"]}" stroke-width="1.8" />')
        svg.append(f'<text x="960" y="580" font-family="monospace" font-size="18" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">Δ SIG</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


# ==============================================================================
# 3. NEO-BRUTALIST ARCHITECTURE (Chunky Pop Blocks & Comic Versus Battle)
# ==============================================================================

class NeoBrutalistRenderer:
    """Tilted marquee stickers, 3.5px solid black borders, hard offset black shadows."""

    @staticmethod
    def render_pillars(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Chunky Pop Blocks with hard offset black shadows & rotated sticker badges."""
        title = slide.get("title", "محورهای پرانرژی استارتاپ")
        kicker = slide.get("kicker", "ویژگی‌های انقلابی")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        svg.append('<g id="header_group">')
        stick_x = (title_x - 220) if rtl else title_x
        svg.append(f'<rect x="{stick_x}" y="70" width="220" height="46" rx="8" fill="{renderer.theme["primary"]}" stroke="#000000" stroke-width="3" transform="rotate(-3 {stick_x+110} 93)" />')
        svg.append(f'<text x="{stick_x + 110}" y="100" font-family="{font}" font-size="20" font-weight="900" fill="#000000" text-anchor="middle" transform="rotate(-3 {stick_x+110} 93)">✦ {escape_xml(kicker)} ✦</text>')
        svg.append(f'<text x="{title_x}" y="175" font-family="{font}" font-size="48" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(cards))
        margin = 120
        gap = 36
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count
        card_y = 240
        card_h = 700

        pop_colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"]]

        for i, card in enumerate(cards):
            c_title = card.get("title", f"آیتم {i+1}")
            c_desc = card.get("desc", "")
            icon_key = card.get("icon", c_title)
            accent_col = pop_colors[i % len(pop_colors)]

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="brutalist_card_{i+1}">')
            shadow_col = "#000000" if not renderer.is_dark else renderer.theme.get("primary", "#A3E635")
            svg.append(f'<rect x="{c_x + 10}" y="{card_y + 10}" width="{card_w}" height="{card_h}" rx="14" fill="{shadow_col}" />')
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{renderer.theme["surface"]}" stroke="{border_col}" stroke-width="3.5" />')

            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="110" rx="12" fill="{accent_col}" stroke="{border_col}" stroke-width="3" />')

            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            idx_x = (c_x + card_w - 70) if rtl else (c_x + 20)
            svg.append(f'<rect x="{idx_x}" y="{card_y + 25}" width="50" height="50" rx="8" fill="#000000" />')
            svg.append(f'<text x="{idx_x + 25}" y="{card_y + 60}" font-family="{font}" font-size="28" font-weight="900" fill="#FFFFFF" text-anchor="middle">{num_str}</text>')

            icon_box_x = (c_x + 25) if rtl else (c_x + card_w - 75)
            svg.append(f'<rect x="{icon_box_x}" y="{card_y + 25}" width="50" height="50" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2.5" />')
            svg.append(get_icon_svg_content(icon_key, icon_box_x + 7, card_y + 32, size=36, stroke_color="#000000"))

            center_x = c_x + (card_w / 2)
            svg.append(f'<text x="{center_x}" y="{card_y + 175}" font-family="{font}" font-size="28" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(c_title)}</text>')

            desc_lines = c_desc.split("\n")
            curr_y = card_y + 245
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:7]:
                clean_l = l.strip()
                if clean_l:
                    b_x = (tx - 8) if rtl else (tx + 8)
                    t_x = (tx - 32) if rtl else (tx + 32)
                    svg.append(f'<polygon points="{b_x},{curr_y-14} {b_x+6},{curr_y-8} {b_x},{curr_y-2} {b_x-6},{curr_y-8}" fill="{accent_col}" stroke="#000000" stroke-width="1.5" />')
                    svg.append(f'<text x="{t_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 50
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


    @staticmethod
    def render_process_steps(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Chunky Stepping Stones with lightning bolts and hard black shadows."""
        title = slide.get("title", "گام‌های پیشروی پرانرژی")
        kicker = slide.get("kicker", "اکشن پلن سریع")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        stick_x = (title_x - 220) if rtl else title_x
        svg.append(f'<rect x="{stick_x}" y="70" width="220" height="46" rx="8" fill="{renderer.theme["primary"]}" stroke="#000000" stroke-width="3" transform="rotate(-3 {stick_x+110} 93)" />')
        svg.append(f'<text x="{stick_x + 110}" y="100" font-family="{font}" font-size="20" font-weight="900" fill="#000000" text-anchor="middle" transform="rotate(-3 {stick_x+110} 93)">⚡ {escape_xml(kicker)} ⚡</text>')
        svg.append(f'<text x="{title_x}" y="175" font-family="{font}" font-size="48" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 120
        gap = 36
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 240
        card_h = 700

        pop_colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"]]

        for i, step in enumerate(steps):
            s_title = step.get("title", f"قدم {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)
            accent_col = pop_colors[i % len(pop_colors)]

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="brutalist_step_{i+1}">')
            # 10px Hard Offset Black Shadow
            svg.append(f'<rect x="{c_x + 10}" y="{card_y + 10}" width="{card_w}" height="{card_h}" rx="14" fill="#000000" />')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{renderer.theme["surface"]}" stroke="#000000" stroke-width="3.5" />')

            # Top Badge Block
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="90" rx="12" fill="{accent_col}" stroke="#000000" stroke-width="3" />')
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            svg.append(f'<text x="{c_x + (card_w/2)}" y="{card_y + 58}" font-family="{font}" font-size="36" font-weight="900" fill="#000000" text-anchor="middle">STEP {num_str} !</text>')

            # Icon Box in Body
            center_x = c_x + (card_w / 2)
            svg.append(f'<rect x="{center_x - 30}" y="{card_y + 120}" width="60" height="60" rx="10" fill="#000000" />')
            svg.append(get_icon_svg_content(icon_key, center_x - 20, card_y + 130, size=40, stroke_color="#FFFFFF"))

            # Step Title
            svg.append(f'<text x="{center_x}" y="{card_y + 230}" font-family="{font}" font-size="28" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')

            # Verbatim Description
            desc_lines = s_desc.split("\n")
            curr_y = card_y + 300
            tx = (c_x + card_w - 36) if rtl else (c_x + 36)
            for l in desc_lines[:7]:
                if l.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">👉 {escape_xml(l.strip())}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_comparison(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Versus Comic Battle with 12-pointed explosion starburst 💥 VS 💥."""
        title = slide.get("title", "نبرد سنتی در برابر مدرن")
        kicker = slide.get("kicker", "چالش انتخاب")
        col_a = slide.get("col_a", {})
        col_b = slide.get("col_b", {})
        rtl = is_persian(title) or any(is_persian(str(x)) for x in col_a.get("items", []))
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="105" font-family="{font}" font-size="20" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="{align}">💥 {escape_xml(kicker)} 💥</text>')
        svg.append(f'<text x="{title_x}" y="165" font-family="{font}" font-size="48" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 780
        card_h = 700
        ca_x = 1020 if rtl else 120
        cb_x = 120 if rtl else 1020
        card_y = 230

        # Col A
        svg.append('<g id="brutalist_col_a">')
        svg.append(f'<rect x="{ca_x + 10}" y="{card_y + 10}" width="{card_w}" height="{card_h}" rx="14" fill="#000000" />')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{renderer.theme["surface"]}" stroke="#000000" stroke-width="3.5" />')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="80" rx="12" fill="#EF4444" stroke="#000000" stroke-width="3" />')
        svg.append(f'<text x="{ca_x + (card_w/2)}" y="{card_y + 52}" font-family="{font}" font-size="32" font-weight="900" fill="#FFFFFF" text-anchor="middle">❌ {escape_xml(col_a.get("title", "سنتی"))}</text>')
        
        curr_y = card_y + 160
        tx_a = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(f'<text x="{tx_a}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="600" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">⛔ {escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        # Col B
        svg.append('<g id="brutalist_col_b">')
        svg.append(f'<rect x="{cb_x + 10}" y="{card_y + 10}" width="{card_w}" height="{card_h}" rx="14" fill="#000000" />')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{renderer.theme["surface"]}" stroke="#000000" stroke-width="3.5" />')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="80" rx="12" fill="{renderer.theme["primary"]}" stroke="#000000" stroke-width="3" />')
        svg.append(f'<text x="{cb_x + (card_w/2)}" y="{card_y + 52}" font-family="{font}" font-size="32" font-weight="900" fill="#000000" text-anchor="middle">⚡ {escape_xml(col_b.get("title", "هوشمند"))}</text>')

        curr_y = card_y + 160
        tx_b = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(f'<text x="{tx_b}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="{align}">✅ {escape_xml(item)}</text>')
            curr_y += 65
        svg.append('</g>')

        # Center Explosion Starburst VS
        svg.append('<g id="spin_brutalist_vs">')
        svg.append(f'<polygon points="960,510 985,550 1025,540 1005,580 1035,610 990,620 995,660 960,635 925,660 930,620 885,610 915,580 895,540 935,550" fill="{renderer.theme["accent"]}" stroke="#000000" stroke-width="4" />')
        svg.append(f'<text x="960" y="593" font-family="{font}" font-size="28" font-weight="900" fill="#FFFFFF" text-anchor="middle">VS</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_stats_kpi(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        """Chunky Pop Block KPI Stats with 10px offset black shadows & neon stickers."""
        title = slide.get("title", "رشد انفجاری و شاخص‌های کلیدی")
        kicker = slide.get("kicker", "آمار فوق‌العاده")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        stick_x = (title_x - 220) if rtl else title_x
        svg.append(f'<rect x="{stick_x}" y="70" width="220" height="46" rx="8" fill="{renderer.theme["primary"]}" stroke="#000000" stroke-width="3" transform="rotate(-3 {stick_x+110} 93)" />')
        svg.append(f'<text x="{stick_x + 110}" y="100" font-family="{font}" font-size="20" font-weight="900" fill="#000000" text-anchor="middle" transform="rotate(-3 {stick_x+110} 93)">🚀 {escape_xml(kicker)} 🚀</text>')
        svg.append(f'<text x="{title_x}" y="175" font-family="{font}" font-size="48" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(kpis))
        margin = 120
        gap = 36
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 240
        card_h = 700

        pop_colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"]]

        for i, kpi in enumerate(kpis):
            num_val = kpi.get("number", kpi.get("val", "+85%"))
            k_label = kpi.get("title", kpi.get("label", ""))
            k_desc = kpi.get("desc", "")
            trend = kpi.get("trend", "🔥 رکورد جدید")
            accent_col = pop_colors[i % len(pop_colors)]

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            center_x = c_x + (card_w / 2)

            svg.append(f'<g id="brutalist_kpi_{i+1}">')
            # 10px Offset Shadow
            svg.append(f'<rect x="{c_x + 10}" y="{card_y + 10}" width="{card_w}" height="{card_h}" rx="14" fill="#000000" />')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{renderer.theme["surface"]}" stroke="#000000" stroke-width="3.5" />')

            # Top Pop Header Box
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="100" rx="12" fill="{accent_col}" stroke="#000000" stroke-width="3" />')
            svg.append(f'<text x="{center_x}" y="{card_y + 60}" font-family="{font}" font-size="24" font-weight="900" fill="#000000" text-anchor="middle">METRIC 0{i+1}</text>')

            # Giant 90px Stat Numeral
            svg.append(f'<text x="{center_x}" y="{card_y + 230}" font-family="{font}" font-size="88" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(num_val)}</text>')

            # Tilted Trend Sticker
            stk_w = min(card_w - 60, 220)
            stk_x = center_x - (stk_w / 2)
            rot = 2 if i % 2 == 0 else -2
            svg.append(f'<rect x="{stk_x}" y="{card_y + 265}" width="{stk_w}" height="42" rx="8" fill="#000000" transform="rotate({rot} {center_x} {card_y+286})" />')
            svg.append(f'<text x="{center_x}" y="{card_y + 293}" font-family="{font}" font-size="18" font-weight="900" fill="{accent_col}" text-anchor="middle" transform="rotate({rot} {center_x} {card_y+286})">{escape_xml(trend)}</text>')

            # Metric Title
            svg.append(f'<text x="{center_x}" y="{card_y + 365}" font-family="{font}" font-size="28" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')

            # Description Lines
            desc_lines = k_desc.split("\n")
            curr_y = card_y + 425
            tx = (c_x + card_w - 36) if rtl else (c_x + 36)
            for l in desc_lines[:6]:
                if l.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="600" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">⚡ {escape_xml(l.strip())}</text>')
                    curr_y += 46
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


# ==============================================================================
# 4. WARM EDITORIAL ARCHITECTURE (Arched Cathedral Windows & Botanical Motifs)
# ==============================================================================

class WarmEditorialRenderer:
    """Arched cathedral window cards, faint background serif numerals, botanical motifs."""

    @staticmethod
    def render_pillars(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Arched Picture-Window Cards with giant faint background numbers and literary poise."""
        title = slide.get("title", "فصل‌های تأمل و بررسی ساختار")
        kicker = slide.get("kicker", "رویکرد انسان‌محور و ارگانیک")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Literary Magazine Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-style="italic" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(cards))
        margin = 130
        gap = 40
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count
        card_y = 230
        card_h = 710

        for i, card in enumerate(cards):
            c_title = card.get("title", f"بخش {i+1}")
            c_desc = card.get("desc", "")
            icon_key = card.get("icon", c_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            center_x = c_x + (card_w / 2)

            svg.append(f'<g id="editorial_card_{i+1}">')
            arch_r = min(card_w / 2, 100)
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="{arch_r}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')

            num_str = to_persian_digits(i + 1) if rtl else str(i + 1)
            svg.append(f'<text x="{center_x}" y="{card_y + 260}" font-family="{font}" font-size="190" font-weight="900" fill="{renderer.theme["primary"]}" fill-opacity="0.08" text-anchor="middle">{num_str}</text>')

            svg.append(f'<ellipse cx="{center_x}" cy="{card_y + 90}" rx="42" ry="48" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.8" />')
            svg.append(get_icon_svg_content(icon_key, center_x - 20, card_y + 70, size=40, stroke_color=renderer.theme["primary"]))

            svg.append(f'<text x="{center_x}" y="{card_y + 200}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(c_title)}</text>')
            svg.append(f'<line x1="{center_x - 40}" y1="{card_y + 230}" x2="{center_x + 40}" y2="{card_y + 230}" stroke="{renderer.theme["primary"]}" stroke-width="1.2" stroke-opacity="0.6" />')

            desc_lines = c_desc.split("\n")
            curr_y = card_y + 290
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:7]:
                clean_l = l.strip()
                if clean_l:
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_process_steps(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Arched Picture-Window Narrative Flow with faint giant watermark numerals."""
        title = slide.get("title", "روایت گام‌به‌گام تحول")
        kicker = slide.get("kicker", "مسیر تدریجی و پیوسته")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-style="italic" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 130
        gap = 40
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        step_w = total_w / count
        card_y = 230
        card_h = 710

        for i, step in enumerate(steps):
            s_title = step.get("title", f"مرحله {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * step_w) - (i * gap)
            else:
                c_x = margin + (i * (step_w + gap))

            center_x = c_x + (step_w / 2)

            svg.append(f'<g id="editorial_step_{i+1}">')
            arch_r = min(step_w / 2, 90)
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{step_w}" height="{card_h}" rx="{arch_r}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')

            # Faint background watermark
            num_str = to_persian_digits(i + 1) if rtl else str(i + 1)
            svg.append(f'<text x="{center_x}" y="{card_y + 260}" font-family="{font}" font-size="190" font-weight="900" fill="{renderer.theme["primary"]}" fill-opacity="0.08" text-anchor="middle">{num_str}</text>')

            # Elliptical icon badge
            svg.append(f'<ellipse cx="{center_x}" cy="{card_y + 90}" rx="42" ry="48" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="1.8" />')
            svg.append(get_icon_svg_content(icon_key, center_x - 20, card_y + 70, size=40, stroke_color=renderer.theme["primary"]))

            # Title
            svg.append(f'<text x="{center_x}" y="{card_y + 200}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')
            svg.append(f'<line x1="{center_x - 40}" y1="{card_y + 230}" x2="{center_x + 40}" y2="{card_y + 230}" stroke="{renderer.theme["primary"]}" stroke-width="1.2" stroke-opacity="0.6" />')

            # Description
            desc_lines = s_desc.split("\n")
            curr_y = card_y + 290
            tx = (c_x + step_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:7]:
                if l.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_stats_kpi(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        """Warm Literary Magazine Stats: Oversized serif numerals with botanical serenity."""
        title = slide.get("title", "شاخص‌های ماندگار و داده‌های معنادار")
        kicker = slide.get("kicker", "سنجش اثرگذاری")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-style="italic" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(kpis))
        margin = 130
        gap = 40
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 230
        card_h = 710

        for i, kpi in enumerate(kpis):
            num_val = kpi.get("number", kpi.get("val", "+85%"))
            k_label = kpi.get("title", kpi.get("label", ""))
            k_desc = kpi.get("desc", "")
            trend = kpi.get("trend", "رشد پیوسته")

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            center_x = c_x + (card_w / 2)

            svg.append(f'<g id="editorial_kpi_{i+1}">')
            arch_r = min(card_w / 2, 90)
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="{arch_r}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')

            # Oversized Serif Stat Numeral
            svg.append(f'<text x="{center_x}" y="{card_y + 160}" font-family="{font}" font-size="80" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')

            # Delicate Botanical Divider
            svg.append(f'<line x1="{center_x - 50}" y1="{card_y + 200}" x2="{center_x + 50}" y2="{card_y + 200}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" stroke-dasharray="4 6" />')

            # Metric Label
            svg.append(f'<text x="{center_x}" y="{card_y + 250}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')

            # Trend Note in Italics
            svg.append(f'<text x="{center_x}" y="{card_y + 290}" font-family="{font}" font-size="17" font-style="italic" fill="{renderer.theme["secondary"]}" text-anchor="middle">~ {escape_xml(trend)} ~</text>')

            # Description Lines
            desc_lines = k_desc.split("\n")
            curr_y = card_y + 360
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:6]:
                if l.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 46
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_comparison(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Warm Editorial Folio Comparison: Arched dual cathedral windows with literary poise."""
        title = slide.get("title", "بررسی تطبیقی و سنجش رویکردها")
        kicker = slide.get("kicker", "افق‌های پیش‌رو")
        col_a = slide.get("col_a", {})
        col_b = slide.get("col_b", {})
        rtl = is_persian(title) or any(is_persian(str(x)) for x in col_a.get("items", []))
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-style="italic" fill="{renderer.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 780
        card_h = 700
        ca_x = 1020 if rtl else 120
        cb_x = 120 if rtl else 1020
        card_y = 230

        # Col A
        svg.append('<g id="editorial_col_a">')
        svg.append(f'<rect x="{ca_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="60" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')
        svg.append(f'<text x="{ca_x + (card_w/2)}" y="{card_y + 90}" font-family="{font}" font-size="30" font-weight="700" fill="{renderer.theme["text_muted"]}" text-anchor="middle">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        svg.append(f'<line x1="{ca_x + 80}" y1="{card_y + 130}" x2="{ca_x + card_w - 80}" y2="{card_y + 130}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.2" />')

        curr_y = card_y + 200
        tx_a = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            svg.append(f'<text x="{(tx_a - 6) if rtl else (tx_a + 6)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">—  {escape_xml(item)}</text>')
            curr_y += 66
        svg.append('</g>')

        # Col B
        svg.append('<g id="editorial_col_b">')
        svg.append(f'<rect x="{cb_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="60" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
        svg.append(f'<text x="{cb_x + (card_w/2)}" y="{card_y + 90}" font-family="{font}" font-size="30" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="middle">✦ {escape_xml(col_b.get("title", "مطلوب"))} ✦</text>')
        svg.append(f'<line x1="{cb_x + 80}" y1="{card_y + 130}" x2="{cb_x + card_w - 80}" y2="{card_y + 130}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')

        curr_y = card_y + 200
        tx_b = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            svg.append(f'<text x="{(tx_b - 6) if rtl else (tx_b + 6)}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_main"]}" text-anchor="{align}">✦  {escape_xml(item)}</text>')
            curr_y += 66
        svg.append('</g>')

        # Center Botanical Medallion
        svg.append('<g id="editorial_vs_badge">')
        svg.append(f'<ellipse cx="960" cy="550" rx="45" ry="50" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')
        svg.append(f'<text x="960" y="558" font-family="{font}" font-size="22" font-style="italic" fill="{renderer.theme["primary"]}" text-anchor="middle">vs</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)


# ==============================================================================
# 5. ROYAL GOLD NOIR ARCHITECTURE (Art Deco Beveled Octagon Pedestals)
# ==============================================================================

class RoyalGoldRenderer:
    """Beveled clipped-corner octagon pedestals, gold pinstripe filigree, diamond crests."""

    @staticmethod
    def render_pillars(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        """Beveled Chamfered Pedestals with gold double pinstripes and heraldic diamond crests."""
        title = slide.get("title", "ارکان راهبردی و منشور توسعه")
        kicker = slide.get("kicker", "سند بالادستی و استراتژیک")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">◆ {escape_xml(kicker)} ◆</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(cards))
        margin = 120
        gap = 36
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count
        card_y = 230
        card_h = 710
        c_cut = 32

        for i, card in enumerate(cards):
            c_title = card.get("title", f"رکن {i+1}")
            c_desc = card.get("desc", "")
            icon_key = card.get("icon", c_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            center_x = c_x + (card_w / 2)

            svg.append(f'<g id="royal_card_{i+1}">')
            pts = f"{c_x + c_cut},{card_y} {c_x + card_w - c_cut},{card_y} {c_x + card_w},{card_y + c_cut} {c_x + card_w},{card_y + card_h - c_cut} {c_x + card_w - c_cut},{card_y + card_h} {c_x + c_cut},{card_y + card_h} {c_x},{card_y + card_h - c_cut} {c_x},{card_y + c_cut}"
            svg.append(f'<polygon points="{pts}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')

            inner_gap = 8
            i_cut = c_cut - 3
            ipts = f"{c_x + i_cut + inner_gap},{card_y + inner_gap} {c_x + card_w - i_cut - inner_gap},{card_y + inner_gap} {c_x + card_w - inner_gap},{card_y + i_cut + inner_gap} {c_x + card_w - inner_gap},{card_y + card_h - i_cut - inner_gap} {c_x + card_w - i_cut - inner_gap},{card_y + card_h - inner_gap} {c_x + i_cut + inner_gap},{card_y + card_h - inner_gap} {c_x + inner_gap},{card_y + card_h - i_cut - inner_gap} {c_x + inner_gap},{card_y + i_cut + inner_gap}"
            svg.append(f'<polygon points="{ipts}" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="0.8" stroke-opacity="0.45" stroke-dasharray="8 6" />')

            dia_cx = center_x
            dia_cy = card_y + 80
            svg.append(f'<polygon points="{dia_cx},{dia_cy-40} {dia_cx+40},{dia_cy} {dia_cx},{dia_cy+40} {dia_cx-40},{dia_cy}" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
            svg.append(get_icon_svg_content(icon_key, dia_cx - 20, dia_cy - 20, size=40, stroke_color=renderer.theme["primary"]))

            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            svg.append(f'<text x="{center_x}" y="{card_y + 155}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">◆ {num_str} ◆</text>')

            svg.append(f'<text x="{center_x}" y="{card_y + 205}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(c_title)}</text>')
            svg.append(f'<line x1="{center_x - 50}" y1="{card_y + 235}" x2="{center_x + 50}" y2="{card_y + 235}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')

            desc_lines = c_desc.split("\n")
            curr_y = card_y + 295
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:7]:
                clean_l = l.strip()
                if clean_l:
                    dia_bx = (tx - 8) if rtl else (tx + 8)
                    txt_x = (tx - 28) if rtl else (tx + 28)
                    svg.append(f'<polygon points="{dia_bx},{curr_y-12} {dia_bx+5},{curr_y-7} {dia_bx},{curr_y-2} {dia_bx-5},{curr_y-7}" fill="{renderer.theme["primary"]}" />')
                    svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(clean_l)}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_process_steps(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        """Art Deco Gold Stepped Grand Staircase with beveled pedestals and diamond markers."""
        title = slide.get("title", "مراحل توسعه راهبردی و اشرافی")
        kicker = slide.get("kicker", "مسیر طلایی رشد")
        steps = slide.get("steps", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(s)) for s in steps)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">◆ {escape_xml(kicker)} ◆</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(steps))
        margin = 120
        gap = 36
        total_w = renderer.width - (2 * margin) - ((count - 1) * gap)
        step_w = total_w / count
        card_y = 230
        card_h = 710
        c_cut = 30

        for i, step in enumerate(steps):
            s_title = step.get("title", f"مرحله {i+1}")
            s_desc = step.get("desc", "")
            icon_key = step.get("icon", s_title)

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * step_w) - (i * gap)
            else:
                c_x = margin + (i * (step_w + gap))

            center_x = c_x + (step_w / 2)

            svg.append(f'<g id="royal_step_{i+1}">')
            pts = f"{c_x + c_cut},{card_y} {c_x + step_w - c_cut},{card_y} {c_x + step_w},{card_y + c_cut} {c_x + step_w},{card_y + card_h - c_cut} {c_x + step_w - c_cut},{card_y + card_h} {c_x + c_cut},{card_y + card_h} {c_x},{card_y + card_h - c_cut} {c_x},{card_y + c_cut}"
            svg.append(f'<polygon points="{pts}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')

            # Diamond Icon Medallion
            dia_cx = center_x
            dia_cy = card_y + 80
            svg.append(f'<polygon points="{dia_cx},{dia_cy-40} {dia_cx+40},{dia_cy} {dia_cx},{dia_cy+40} {dia_cx-40},{dia_cy}" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
            svg.append(get_icon_svg_content(icon_key, dia_cx - 20, dia_cy - 20, size=40, stroke_color=renderer.theme["primary"]))

            # Step Crest Number
            num_str = to_persian_digits(i + 1) if rtl else f"0{i+1}"
            svg.append(f'<text x="{center_x}" y="{card_y + 155}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">◆ STAGE {num_str} ◆</text>')

            # Step Title
            svg.append(f'<text x="{center_x}" y="{card_y + 205}" font-family="{font}" font-size="26" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(s_title)}</text>')
            svg.append(f'<line x1="{center_x - 45}" y1="{card_y + 235}" x2="{center_x + 45}" y2="{card_y + 235}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')

            # Description
            desc_lines = s_desc.split("\n")
            curr_y = card_y + 295
            tx = (c_x + step_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:7]:
                if l.strip():
                    dia_bx = (tx - 8) if rtl else (tx + 8)
                    txt_x = (tx - 28) if rtl else (tx + 28)
                    svg.append(f'<polygon points="{dia_bx},{curr_y-12} {dia_bx+5},{curr_y-7} {dia_bx},{curr_y-2} {dia_bx-5},{curr_y-7}" fill="{renderer.theme["primary"]}" />')
                    svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_stats_kpi(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        """Art Deco Octagon Pedestal KPI Metrics with 24k gold filigree."""
        title = slide.get("title", "شاخص‌های عملکرد طلایی و رشد پایدار")
        kicker = slide.get("kicker", "معیارهای تعالی و شکوه")
        kpis = slide.get("kpis", slide.get("cards", []))
        rtl = is_persian(title) or any(is_persian(str(k)) for k in kpis)
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">◆ {escape_xml(kicker)} ◆</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        count = max(1, len(kpis))
        margin = 120
        gap = 36
        card_w = (renderer.width - (2 * margin) - ((count - 1) * gap)) / count
        card_y = 230
        card_h = 710
        c_cut = 32

        for i, kpi in enumerate(kpis):
            num_val = kpi.get("number", kpi.get("val", "+85%"))
            k_label = kpi.get("title", kpi.get("label", ""))
            k_desc = kpi.get("desc", "")
            trend = kpi.get("trend", "◆ تعالی تضمین‌شده ◆")

            if rtl:
                c_x = (renderer.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            center_x = c_x + (card_w / 2)

            svg.append(f'<g id="royal_kpi_{i+1}">')
            pts = f"{c_x + c_cut},{card_y} {c_x + card_w - c_cut},{card_y} {c_x + card_w},{card_y + c_cut} {c_x + card_w},{card_y + card_h - c_cut} {c_x + card_w - c_cut},{card_y + card_h} {c_x + c_cut},{card_y + card_h} {c_x},{card_y + card_h - c_cut} {c_x},{card_y + c_cut}"
            svg.append(f'<polygon points="{pts}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2" />')

            # Giant Gold Numeral
            svg.append(f'<text x="{center_x}" y="{card_y + 140}" font-family="{font}" font-size="78" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="middle">{escape_xml(num_val)}</text>')

            # Diamond Trend Pill
            svg.append(f'<text x="{center_x}" y="{card_y + 190}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">{escape_xml(trend)}</text>')
            svg.append(f'<line x1="{center_x - 50}" y1="{card_y + 220}" x2="{center_x + 50}" y2="{card_y + 220}" stroke="{renderer.theme["primary"]}" stroke-width="1.5" />')

            # Metric Label
            svg.append(f'<text x="{center_x}" y="{card_y + 270}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(k_label)}</text>')

            # Description Lines
            desc_lines = k_desc.split("\n")
            curr_y = card_y + 340
            tx = (c_x + card_w - 40) if rtl else (c_x + 40)
            for l in desc_lines[:6]:
                if l.strip():
                    dia_bx = (tx - 8) if rtl else (tx + 8)
                    txt_x = (tx - 28) if rtl else (tx + 28)
                    svg.append(f'<polygon points="{dia_bx},{curr_y-12} {dia_bx+5},{curr_y-7} {dia_bx},{curr_y-2} {dia_bx-5},{curr_y-7}" fill="{renderer.theme["primary"]}" />')
                    svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(l.strip())}</text>')
                    curr_y += 48
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    @staticmethod
    def render_comparison(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        """Art Deco Grand Dual Pedestal Noir Comparison with Gold Battle Crest."""
        title = slide.get("title", "سنجش برتری و تقابل استراتژیک")
        kicker = slide.get("kicker", "ارزیابی سطوح اشرافی")
        col_a = slide.get("col_a", {})
        col_b = slide.get("col_b", {})
        rtl = is_persian(title) or any(is_persian(str(x)) for x in col_a.get("items", []))
        font = renderer.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        # Header Block
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="95" font-family="{font}" font-size="18" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="{align}">◆ {escape_xml(kicker)} ◆</text>')
        svg.append(f'<text x="{title_x}" y="155" font-family="{font}" font-size="46" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        card_w = 780
        card_h = 700
        ca_x = 1020 if rtl else 120
        cb_x = 120 if rtl else 1020
        card_y = 230
        c_cut = 32

        # Col A
        svg.append('<g id="royal_comp_a">')
        pts_a = f"{ca_x + c_cut},{card_y} {ca_x + card_w - c_cut},{card_y} {ca_x + card_w},{card_y + c_cut} {ca_x + card_w},{card_y + card_h - c_cut} {ca_x + card_w - c_cut},{card_y + card_h} {ca_x + c_cut},{card_y + card_h} {ca_x},{card_y + card_h - c_cut} {ca_x},{card_y + c_cut}"
        svg.append(f'<polygon points="{pts_a}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["surface_border"]}" stroke-width="2" />')
        svg.append(f'<text x="{ca_x + (card_w/2)}" y="{card_y + 80}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["text_muted"]}" text-anchor="middle">{escape_xml(col_a.get("title", "سنتی"))}</text>')
        svg.append(f'<line x1="{ca_x + 80}" y1="{card_y + 115}" x2="{ca_x + card_w - 80}" y2="{card_y + 115}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.5" />')

        curr_y = card_y + 185
        tx_a = (ca_x + card_w - 60) if rtl else (ca_x + 60)
        for item in col_a.get("items", []):
            dia_bx = (tx_a - 6) if rtl else (tx_a + 6)
            txt_x = (tx_a - 28) if rtl else (tx_a + 28)
            svg.append(f'<polygon points="{dia_bx},{curr_y-10} {dia_bx+4},{curr_y-6} {dia_bx},{curr_y-2} {dia_bx-4},{curr_y-6}" fill="{renderer.theme["text_muted"]}" />')
            svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 66
        svg.append('</g>')

        # Col B
        svg.append('<g id="royal_comp_b">')
        pts_b = f"{cb_x + c_cut},{card_y} {cb_x + card_w - c_cut},{card_y} {cb_x + card_w},{card_y + c_cut} {cb_x + card_w},{card_y + card_h - c_cut} {cb_x + card_w - c_cut},{card_y + card_h} {cb_x + c_cut},{card_y + card_h} {cb_x},{card_y + card_h - c_cut} {cb_x},{card_y + c_cut}"
        svg.append(f'<polygon points="{pts_b}" fill="{renderer.theme["surface"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
        svg.append(f'<text x="{cb_x + (card_w/2)}" y="{card_y + 80}" font-family="{font}" font-size="28" font-weight="700" fill="{renderer.theme["primary"]}" text-anchor="middle">◆ {escape_xml(col_b.get("title", "برتر"))} ◆</text>')
        svg.append(f'<line x1="{cb_x + 80}" y1="{card_y + 115}" x2="{cb_x + card_w - 80}" y2="{card_y + 115}" stroke="{renderer.theme["primary"]}" stroke-width="1.8" />')

        curr_y = card_y + 185
        tx_b = (cb_x + card_w - 60) if rtl else (cb_x + 60)
        for item in col_b.get("items", []):
            dia_bx = (tx_b - 6) if rtl else (tx_b + 6)
            txt_x = (tx_b - 28) if rtl else (tx_b + 28)
            svg.append(f'<polygon points="{dia_bx},{curr_y-10} {dia_bx+5},{curr_y-6} {dia_bx},{curr_y-2} {dia_bx-5},{curr_y-6}" fill="{renderer.theme["primary"]}" />')
            svg.append(f'<text x="{txt_x}" y="{curr_y}" font-family="{font}" font-size="20" font-weight="600" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item)}</text>')
            curr_y += 66
        svg.append('</g>')

        # Center Royal Diamond Crest VS
        svg.append('<g id="royal_vs_crest">')
        svg.append(f'<polygon points="960,510 1000,550 960,590 920,550" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["primary"]}" stroke-width="2.5" />')
        svg.append(f'<text x="960" y="558" font-family="{font}" font-size="20" font-weight="900" fill="{renderer.theme["primary"]}" text-anchor="middle">VS</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

