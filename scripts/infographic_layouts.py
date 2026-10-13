#!/usr/bin/env python3
"""
PPT Master / PPT_Saz v5.0 — Next-Gen Infographic, Chart, Table & Storytelling Layouts

Provides 12 new creative visual slide architectures (inspired by PPTAgent, AutoPresent,
and VisualizationCatalog) so no two slides in a presentation ever feel repetitive:
  1. pyramid_hierarchy     — Layered 3D/Isometric Pyramid with apex halo & side callouts
  2. funnel_pipeline       — Multi-stage Conversion/Filtering Funnel with intake orbit
  3. venn_synergy          — 3 Intersecting Translucent Synergy Rings + perimeter cards
  4. quadrant_matrix_2x2   — 2x2 Strategic Matrix (SWOT / Priority Grid) + central compass
  5. snake_roadmap         — Winding Serpentine S-Curve Timeline with alternating pods
  6. mind_map_hub          — Central Core Nucleus with radial neural branches
  7. fishbone_cause_effect — Ishikawa Root-Cause Diagnostic Diagram
  8. data_chart_showcase   — Native Vector Charts (Radar, Donut, Waterfall + templates/charts/)
  9. smart_table_matrix    — Styled Multi-Column Feature/Clinical Comparison Table
 10. hero_callout_quote    — Giant Editorial/Keynote Statement Callout with spinning aura
 11. geometric_gallery     — Archetype-specific Masked Multi-Image Showcase
 12. closing_thankyou      — Grand Finale / Q&A Slide with rotating centerpiece emblem
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from icon_mapper import get_icon_svg_content
from art_style_skins import _shade_color


def is_persian(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]', str(text)))


def to_persian_digits(num: int | str) -> str:
    s = str(num)
    return s.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def escape_xml(s: Any) -> str:
    if s is None:
        return ""
    text = str(s)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _extract_items(slide: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize cards, steps, kpis, or bullets into a list of dicts with title/desc/icon."""
    raw = (
        slide.get("cards")
        or slide.get("steps")
        or slide.get("items")
        or slide.get("kpis")
        or slide.get("bullets")
        or []
    )
    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw):
        if isinstance(item, dict):
            normalized.append({
                "title": item.get("title", item.get("label", f"بخش {idx+1}")),
                "desc": item.get("desc", item.get("text", "")),
                "icon": item.get("icon", item.get("title", "sparkles")),
                "number": item.get("number", item.get("val", "")),
                "trend": item.get("trend", ""),
            })
        else:
            lines = str(item).split("\n")
            normalized.append({
                "title": lines[0].strip(),
                "desc": "\n".join(lines[1:]).strip() if len(lines) > 1 else str(item).strip(),
                "icon": lines[0].strip(),
                "number": "",
                "trend": "",
            })
    if not normalized:
        normalized = [
            {"title": "سطح اول", "desc": "توضیحات کلیدی بخش اول", "icon": "layers", "number": "۰۱", "trend": ""},
            {"title": "سطح دوم", "desc": "توضیحات کلیدی بخش دوم", "icon": "cpu", "number": "۰۲", "trend": ""},
            {"title": "سطح سوم", "desc": "توضیحات کلیدی بخش سوم", "icon": "rocket", "number": "۰۳", "trend": ""},
        ]
    return normalized


class InfographicLayoutRenderer:
    """Renders 12 distinct infographic, diagram, vector chart, and storytelling slide layouts."""

    @staticmethod
    def _render_slide_header(renderer, slide: Dict[str, Any], rtl: bool, default_kicker: str) -> List[str]:
        return renderer._render_style_header(slide, rtl, default_kicker)

    # ==========================================================================
    # 1. PYRAMID HIERARCHY (هرم سلسله‌مراتبی و سطوح اولویت)
    # ==========================================================================
    @staticmethod
    def render_pyramid_hierarchy(renderer, slide: Dict[str, Any], slide_idx: int = 2) -> str:
        items = _extract_items(slide)[:4]
        title = slide.get("title", "")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "ساختار سلسله‌مراتبی و سطوح"))

        pyr_cx = 560 if rtl else 1360
        pyr_top_y = 250
        pyr_h = 660
        count = max(1, len(items))
        tier_h = (pyr_h - ((count - 1) * 14)) / count
        max_half_w = 360

        # Spinning Apex Halo at top of pyramid
        svg.append('<g id="spin_pyramid_apex">')
        svg.append(f'<circle cx="{pyr_cx}" cy="{pyr_top_y + 20}" r="85" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="8 6" stroke-opacity="0.55" />')
        svg.append(f'<circle cx="{pyr_cx}" cy="{pyr_top_y + 20}" r="105" fill="none" stroke="{renderer.theme["secondary"]}" stroke-width="1.2" stroke-dasharray="4 8" stroke-opacity="0.35" />')
        svg.append(f'<circle cx="{pyr_cx + 85}" cy="{pyr_top_y + 20}" r="5" fill="{renderer.theme["accent"]}" />')
        svg.append('</g>')

        colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"], renderer.theme["primary"]]

        for i, item in enumerate(items):
            y1 = pyr_top_y + i * (tier_h + 14)
            y2 = y1 + tier_h
            # Trapezoid widths from apex to base
            w1_top = 50 + (i / count) * max_half_w
            w2_bot = 50 + ((i + 1) / count) * max_half_w
            col = colors[i % len(colors)]

            # 2.5D Isometric & 3D Volumetric Extrusion for Pyramid Tiers!
            iso_dx = 28.0
            iso_dy = 14.0

            # 1) Cast Floor Drop-Shadow under each tier
            svg.append(f'<g id="pyramid_tier_{i+1}">')
            sh_pts = f"{pyr_cx - w1_top + iso_dx},{y1 + iso_dy + 8} {pyr_cx + w1_top + iso_dx},{y1 + iso_dy + 8} {pyr_cx + w2_bot + iso_dx},{y2 + iso_dy + 8} {pyr_cx - w2_bot + iso_dx},{y2 + iso_dy + 8}"
            svg.append(f'<polygon points="{sh_pts}" fill="#000000" fill-opacity="0.32" />')

            # 2) Right 3D Thickness Wall (Shaded Darker)
            rw_pts = f"{pyr_cx + w1_top},{y1} {pyr_cx + w1_top + iso_dx},{y1 + iso_dy} {pyr_cx + w2_bot + iso_dx},{y2 + iso_dy} {pyr_cx + w2_bot},{y2}"
            svg.append(f'<polygon points="{rw_pts}" fill="{_shade_color(col, -0.38)}" stroke="{col}" stroke-width="1.8" />')

            # 3) Front/Top Lit Face of the Pyramid Tier (Using Volumetric Gradients)
            pts = f"{pyr_cx - w1_top},{y1} {pyr_cx + w1_top},{y1} {pyr_cx + w2_bot},{y2} {pyr_cx - w2_bot},{y2}"
            grad_id = "grad_3d_primary" if col == renderer.theme["primary"] else ("grad_3d_secondary" if col == renderer.theme["secondary"] else "grad_3d_accent")
            svg.append(f'<polygon points="{pts}" fill="url(#{grad_id})" stroke="{_shade_color(col, 0.35)}" stroke-width="2.5" />')

            # Specular top rim shine line
            svg.append(f'<line x1="{pyr_cx - w1_top + 4}" y1="{y1 + 3}" x2="{pyr_cx + w1_top - 4}" y2="{y1 + 3}" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.5" />')

            num_str = to_persian_digits(f"0{i+1}") if rtl else f"0{i+1}"
            mid_y = (y1 + y2) / 2
            svg.append(f'<text x="{pyr_cx}" y="{mid_y + 10}" font-family="{font}" font-size="28" font-weight="900" fill="#FFFFFF" text-anchor="middle">{num_str}</text>')

            # Connected Side Callout Card for Verbatim Text
            card_w = 820
            card_x = 980 if rtl else 120
            conn_x1 = (pyr_cx + (w1_top + w2_bot) / 2) if rtl else (pyr_cx - (w1_top + w2_bot) / 2)
            conn_x2 = card_x if rtl else (card_x + card_w)

            svg.append(f'<line x1="{conn_x1}" y1="{mid_y}" x2="{conn_x2}" y2="{mid_y}" stroke="{col}" stroke-width="2" stroke-dasharray="6 4" />')
            svg.append(f'<circle cx="{conn_x1}" cy="{mid_y}" r="6" fill="{col}" />')

            svg.extend(renderer._card_rect(card_x, y1, card_w, tier_h, rx=22, stroke_width=2.0, top_accent=False))
            icon_cx = (card_x + card_w - 55) if rtl else (card_x + 55)
            svg.extend(renderer._render_icon_badge(icon_cx, mid_y, 30, col, item["icon"], icon_size=32))

            tx = (card_x + card_w - 105) if rtl else (card_x + 105)
            svg.append(f'<text x="{tx}" y="{y1 + 52}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = y1 + 88
            for line in desc_lines[:3]:
                svg.append(f'<text x="{tx}" y="{dy}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">• {escape_xml(line)}</text>')
                dy += 30
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 2. FUNNEL PIPELINE (قیف پالایش و تبدیل مرحله‌ای)
    # ==========================================================================
    @staticmethod
    def render_funnel_pipeline(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        items = _extract_items(slide)[:4]
        title = slide.get("title", "")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "قیف پالایش و جریان مرحله‌ای"))

        fun_cx = 520 if rtl else 1400
        fun_top_y = 260
        fun_h = 640
        count = max(1, len(items))
        stage_h = (fun_h - ((count - 1) * 16)) / count
        max_w = 340
        min_w = 110

        # Spinning Intake Ring at top of Funnel
        svg.append('<g id="spin_funnel_intake">')
        svg.append(f'<ellipse cx="{fun_cx}" cy="{fun_top_y}" rx="{max_w}" ry="28" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="10 6" stroke-opacity="0.6" />')
        svg.append(f'<circle cx="{fun_cx}" cy="{fun_top_y + fun_h + 25}" r="36" fill="none" stroke="{renderer.theme["accent"]}" stroke-width="2" stroke-dasharray="5 5" />')
        svg.append('</g>')

        colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"], renderer.theme["primary"]]

        for i, item in enumerate(items):
            y1 = fun_top_y + i * (stage_h + 16)
            y2 = y1 + stage_h
            w1 = max_w - (i / count) * (max_w - min_w)
            w2 = max_w - ((i + 1) / count) * (max_w - min_w)
            col = colors[i % len(colors)]

            # 3D Volumetric Conical Frustum Segment with Curved Elliptical Caps
            grad_id = "grad_3d_primary" if col == renderer.theme["primary"] else ("grad_3d_secondary" if col == renderer.theme["secondary"] else "grad_3d_accent")
            svg.append(f'<g id="funnel_stage_{i+1}">')

            # 1) Cast soft shadow under stage
            svg.append(f'<ellipse cx="{fun_cx}" cy="{y2 + 8}" rx="{w2 * 0.95}" ry="18" fill="#000000" fill-opacity="0.28" />')

            # 2) 3D Volumetric Funnel Body (Trapezoid with Volumetric Studio Gradient)
            pts = f"{fun_cx - w1},{y1} {fun_cx + w1},{y1} {fun_cx + w2},{y2} {fun_cx - w2},{y2}"
            svg.append(f'<polygon points="{pts}" fill="url(#{grad_id})" stroke="{_shade_color(col, 0.35)}" stroke-width="2" />')

            # 3) 3D Curved Top Elliptical Rim (Simulates true cylinder/funnel mouth depth)
            svg.append(f'<ellipse cx="{fun_cx}" cy="{y1}" rx="{w1}" ry="16" fill="{_shade_color(col, 0.40)}" stroke="{col}" stroke-width="2" />')
            svg.append(f'<ellipse cx="{fun_cx}" cy="{y1}" rx="{w1 * 0.85}" ry="11" fill="{renderer.theme["surface"]}" stroke="{col}" stroke-width="1.2" />')

            # 4) Front specular shine line down center of the funnel
            svg.append(f'<line x1="{fun_cx - 15}" y1="{y1 + 10}" x2="{fun_cx - 8}" y2="{y2 - 6}" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.45" />')

            mid_y = (y1 + y2) / 2
            stage_num = to_persian_digits(f"مرحله {i+1}") if rtl else f"STAGE 0{i+1}"
            svg.append(f'<text x="{fun_cx}" y="{mid_y + 8}" font-family="{font}" font-size="22" font-weight="900" fill="#FFFFFF" text-anchor="middle">{stage_num}</text>')

            # Connected Detail Pod
            card_w = 880
            card_x = 920 if rtl else 120
            svg.extend(renderer._card_rect(card_x, y1, card_w, stage_h, rx=22, stroke_width=2.0, top_accent=False))
            svg.append(f'<rect x="{(card_x + card_w - 8) if rtl else card_x}" y="{y1 + 22}" width="8" height="{stage_h - 36}" rx="4" fill="{col}" />')

            icon_cx = (card_x + card_w - 60) if rtl else (card_x + 60)
            svg.extend(renderer._render_icon_badge(icon_cx, mid_y + 4, 28, col, item["icon"], icon_size=30))

            tx = (card_x + card_w - 110) if rtl else (card_x + 110)
            svg.append(f'<text x="{tx}" y="{y1 + 52}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = y1 + 88
            for line in desc_lines[:3]:
                svg.append(f'<text x="{tx}" y="{dy}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">▸ {escape_xml(line)}</text>')
                dy += 30
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 3. VENN SYNERGY (دیاگرام ون و هم‌افزایی ۳ حلقه متقاطع)
    # ==========================================================================
    @staticmethod
    def render_venn_synergy(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        items = _extract_items(slide)[:3]
        while len(items) < 3:
            items.append({"title": f"مؤلفه {len(items)+1}", "desc": "هم‌افزایی سیستمی", "icon": "sparkles", "number": "", "trend": ""})

        title = slide.get("title", "")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "هم‌پوشانی و هم‌افزایی مفهومی"))

        cx, cy = 960, 585
        r_venn = 165
        offsets = [
            (cx, cy - 95, renderer.theme["primary"]),
            (cx - 105, cy + 75, renderer.theme["secondary"]),
            (cx + 105, cy + 75, renderer.theme["accent"]),
        ]

        # Spinning Outer Synergy Ring
        svg.append('<g id="spin_venn_synergy_orbit">')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="295" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="1.8" stroke-dasharray="10 8" stroke-opacity="0.45" />')
        svg.append(f'<circle cx="{cx + 295}" cy="{cy}" r="6" fill="{renderer.theme["primary"]}" />')
        svg.append(f'<circle cx="{cx - 295}" cy="{cy}" r="6" fill="{renderer.theme["secondary"]}" />')
        svg.append('</g>')

        # 3 Intersecting 3D Volumetric Synergy Rings with Specular Lighting
        svg.append('<g id="venn_circles_group">')
        for idx, (vx, vy, col) in enumerate(offsets):
            grad_id = "grad_3d_primary" if col == renderer.theme["primary"] else ("grad_3d_secondary" if col == renderer.theme["secondary"] else "grad_3d_accent")
            # Soft 3D drop-shadow under each circle
            svg.append(f'<circle cx="{vx}" cy="{vy + 10}" r="{r_venn}" fill="#000000" fill-opacity="0.25" />')
            # 3D Translucent Volumetric Circle
            svg.append(f'<circle cx="{vx}" cy="{vy}" r="{r_venn}" fill="url(#{grad_id})" fill-opacity="0.32" stroke="{col}" stroke-width="3" />')
            # Specular arc highlight at top of circle
            svg.append(f'<path d="M {vx - r_venn * 0.7},{vy - r_venn * 0.6} A {r_venn},{r_venn} 0 0,1 {vx + r_venn * 0.7},{vy - r_venn * 0.6}" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-opacity="0.5" />')
            label_y = (vy - 55) if idx == 0 else (vy + 45)
            svg.append(f'<text x="{vx}" y="{label_y}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(items[idx]["title"][:22])}</text>')

        # Central Intersection Nucleus (3D Specular Centerpiece Sphere)
        svg.extend(renderer._render_icon_badge(cx, cy + 15, 48, renderer.theme["primary"], "sparkles", icon_size=42))
        svg.append('</g>')

        # 3 Perimeter Verbatim Cards
        card_positions = [
            (120, 230, 480, 290, renderer.theme["primary"]),
            (120, 560, 480, 360, renderer.theme["secondary"]),
            (1320, 360, 480, 460, renderer.theme["accent"]),
        ]
        for idx, item in enumerate(items[:3]):
            px, py, pw, ph, col = card_positions[idx]
            svg.append(f'<g id="venn_card_{idx+1}">')
            svg.extend(renderer._card_rect(px, py, pw, ph, rx=26, stroke_width=2.2))
            ic_x = (px + pw - 50) if rtl else (px + 50)
            svg.extend(renderer._render_icon_badge(ic_x, py + 62, 26, col, item["icon"], icon_size=28))

            tx = (px + pw - 95) if rtl else (px + 95)
            svg.append(f'<text x="{tx}" y="{py + 68}" font-family="{font}" font-size="23" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = py + 120
            body_tx = (px + pw - 34) if rtl else (px + 34)
            for line in desc_lines[:6]:
                svg.append(f'<text x="{body_tx}" y="{dy}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">• {escape_xml(line)}</text>')
                dy += 38
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 4. QUADRANT MATRIX 2x2 (ماتریس ۴ خانه‌ای استراتژیک / SWOT)
    # ==========================================================================
    @staticmethod
    def render_quadrant_matrix_2x2(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        items = _extract_items(slide)[:4]
        while len(items) < 4:
            items.append({"title": f"ربع {len(items)+1}", "desc": "تحلیل استراتژیک", "icon": "target", "number": "", "trend": ""})

        title = slide.get("title", "")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "ماتریس چهارگانه استراتژیک"))

        cx, cy = 960, 590
        qw, qh = 780, 325
        gap = 50

        quad_coords = [
            (cx + gap/2 if rtl else cx - qw - gap/2, cy - qh - gap/2, renderer.theme["primary"], "Q1"),
            (cx - qw - gap/2 if rtl else cx + gap/2, cy - qh - gap/2, renderer.theme["secondary"], "Q2"),
            (cx + gap/2 if rtl else cx - qw - gap/2, cy + gap/2, renderer.theme["accent"], "Q3"),
            (cx - qw - gap/2 if rtl else cx + gap/2, cy + gap/2, renderer.theme["primary"], "Q4"),
        ]

        # Axis Crosshairs
        svg.append(f'<line x1="120" y1="{cy}" x2="1800" y2="{cy}" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="8 6" stroke-opacity="0.5" />')
        svg.append(f'<line x1="{cx}" y1="220" x2="{cx}" y2="960" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="8 6" stroke-opacity="0.5" />')

        for idx, item in enumerate(items[:4]):
            qx, qy, col, q_code = quad_coords[idx]
            svg.append(f'<g id="quadrant_cell_{idx+1}">')
            svg.extend(renderer._card_rect(qx, qy, qw, qh, rx=26, stroke_width=2.2))

            ic_x = (qx + qw - 55) if rtl else (qx + 55)
            svg.extend(renderer._render_icon_badge(ic_x, qy + 64, 30, col, item["icon"], icon_size=32))

            badge_x = (qx + 30) if rtl else (qx + qw - 95)
            svg.append(f'<rect x="{badge_x}" y="{qy + 44}" width="65" height="32" rx="8" fill="{renderer.theme["badge_bg"]}" stroke="{col}" stroke-width="1.5" />')
            svg.append(f'<text x="{badge_x + 32}" y="{qy + 66}" font-family="monospace" font-size="16" font-weight="700" fill="{col}" text-anchor="middle">{q_code}</text>')

            tx = (qx + qw - 105) if rtl else (qx + 105)
            svg.append(f'<text x="{tx}" y="{qy + 72}" font-family="{font}" font-size="25" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = qy + 128
            for line in desc_lines[:5]:
                svg.append(f'<circle cx="{(tx - 8) if rtl else (tx + 8)}" cy="{dy - 6}" r="4.5" fill="{col}" />')
                svg.append(f'<text x="{(tx - 26) if rtl else (tx + 26)}" y="{dy}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(line)}</text>')
                dy += 38
            svg.append('</g>')

        # Central Spinning Compass Hub
        svg.append('<g id="spin_quadrant_compass">')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="72" fill="none" stroke="{renderer.theme["secondary"]}" stroke-width="2" stroke-dasharray="6 6" />')
        svg.extend(renderer._render_icon_badge(cx, cy, 52, renderer.theme["primary"], "compass", icon_size=44))
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 5. SNAKE ROADMAP (مسیر موجی و زیگزاگ گام‌به‌گام)
    # ==========================================================================
    @staticmethod
    def render_snake_roadmap(renderer, slide: Dict[str, Any], slide_idx: int = 3) -> str:
        items = _extract_items(slide)[:4]
        title = slide.get("title", "")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "مسیر تکاملی و نقشه راه موجی"))

        count = max(1, len(items))
        margin = 140
        span_w = renderer.width - (2 * margin)
        step_dx = span_w / max(1, count)
        mid_y = 580

        # S-Curve Wave Path across canvas
        wave_d = f"M 140,{mid_y} C 480,{mid_y - 180} 720,{mid_y + 180} 960,{mid_y} C 1200,{mid_y - 180} 1440,{mid_y + 180} 1780,{mid_y}"
        svg.append(f'<path d="{wave_d}" fill="none" stroke="{renderer.theme["surface_border"]}" stroke-width="10" stroke-linecap="round" />')
        svg.append(f'<path d="{wave_d}" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="3.5" stroke-dasharray="14 8" />')

        colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"], renderer.theme["primary"]]

        for i, item in enumerate(items):
            frac = (i + 0.5) / count
            nx = (renderer.width - margin - frac * span_w) if rtl else (margin + frac * span_w)
            is_top = (i % 2 == 0)
            ny = (mid_y - 55) if is_top else (mid_y + 55)
            col = colors[i % len(colors)]

            # Spinning Milestone Halo
            svg.append(f'<g id="spin_snake_node_{i+1}">')
            svg.append(f'<circle cx="{nx}" cy="{ny}" r="48" fill="none" stroke="{col}" stroke-width="2.2" stroke-dasharray="6 5" />')
            svg.append(f'<circle cx="{nx + 48}" cy="{ny}" r="4.5" fill="{col}" />')
            svg.append('</g>')

            svg.append(f'<g id="snake_step_{i+1}">')
            svg.extend(renderer._render_icon_badge(nx, ny, 35, col, item["icon"], icon_size=36))

            card_w = min(410, step_dx - 24)
            card_h = 265
            card_x = nx - (card_w / 2)
            card_y = 215 if is_top else 685

            # Vertical connector stem
            stem_y1 = (ny - 36) if is_top else (ny + 36)
            stem_y2 = (card_y + card_h) if is_top else card_y
            svg.append(f'<line x1="{nx}" y1="{stem_y1}" x2="{nx}" y2="{stem_y2}" stroke="{col}" stroke-width="2.5" />')

            svg.extend(renderer._card_rect(card_x, card_y, card_w, card_h, rx=24, stroke_width=2.0))
            num_str = to_persian_digits(f"0{i+1}") if rtl else f"0{i+1}"
            svg.append(f'<text x="{nx}" y="{card_y + 48}" font-family="{font}" font-size="18" font-weight="800" fill="{col}" text-anchor="middle">STEP {num_str}</text>')
            svg.append(f'<text x="{nx}" y="{card_y + 86}" font-family="{font}" font-size="23" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = card_y + 132
            tx = (card_x + card_w - 26) if rtl else (card_x + 26)
            for line in desc_lines[:4]:
                svg.append(f'<text x="{tx}" y="{dy}" font-family="{font}" font-size="17" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">• {escape_xml(line)}</text>')
                dy += 34
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 6. MIND MAP HUB (نقشه ذهنی شعاعی و شبکه مفهومی)
    # ==========================================================================
    @staticmethod
    def render_mind_map_hub(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        items = _extract_items(slide)[:4]
        title = slide.get("title", "شبکه مفهومی")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "نقشه ذهنی و انشعابات مفهومی"))

        cx, cy = 960, 585

        # Satellite node positions (4 corners around hub)
        satellites = [
            (120, 235, 560, 310, cx - 120, cy - 60, 680, 390, renderer.theme["primary"]),
            (1240, 235, 560, 310, cx + 120, cy - 60, 1240, 390, renderer.theme["secondary"]),
            (120, 615, 560, 310, cx - 120, cy + 60, 680, 770, renderer.theme["accent"]),
            (1240, 615, 560, 310, cx + 120, cy + 60, 1240, 770, renderer.theme["primary"]),
        ]

        # Curved neural bezier connectors
        for idx, item in enumerate(items[:4]):
            bx, by, bw, bh, sx, sy, ex, ey, col = satellites[idx]
            ctrl_x = (sx + ex) / 2
            svg.append(f'<path d="M {sx},{sy} C {ctrl_x},{sy} {ctrl_x},{ey} {ex},{ey}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="8 5" />')
            svg.append(f'<circle cx="{ex}" cy="{ey}" r="7" fill="{col}" />')

            svg.append(f'<g id="mindmap_branch_{idx+1}">')
            svg.extend(renderer._card_rect(bx, by, bw, bh, rx=26, stroke_width=2.2))
            ic_x = (bx + bw - 52) if rtl else (bx + 52)
            svg.extend(renderer._render_icon_badge(ic_x, by + 62, 28, col, item["icon"], icon_size=30))

            tx = (bx + bw - 98) if rtl else (bx + 98)
            svg.append(f'<text x="{tx}" y="{by + 68}" font-family="{font}" font-size="24" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = by + 122
            for line in desc_lines[:4]:
                svg.append(f'<circle cx="{(tx - 8) if rtl else (tx + 8)}" cy="{dy - 6}" r="4" fill="{col}" />')
                svg.append(f'<text x="{(tx - 24) if rtl else (tx + 24)}" y="{dy}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(line)}</text>')
                dy += 38
            svg.append('</g>')

        # Central Spinning Mind-Map Core
        svg.append('<g id="spin_mindmap_core">')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="145" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2.5" stroke-dasharray="12 8" stroke-opacity="0.65" />')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="165" fill="none" stroke="{renderer.theme["secondary"]}" stroke-width="1.5" stroke-dasharray="4 8" stroke-opacity="0.4" />')
        svg.append(f'<circle cx="{cx + 145}" cy="{cy}" r="6" fill="{renderer.theme["accent"]}" />')
        svg.append(f'<circle cx="{cx - 145}" cy="{cy}" r="6" fill="{renderer.theme["primary"]}" />')
        svg.append('</g>')

        svg.append('<g id="mindmap_nucleus">')
        svg.extend(renderer._card_rect(cx - 115, cy - 110, 230, 220))
        svg.append(get_icon_svg_content("brain", cx - 28, cy - 52, size=56, stroke_color=renderer.theme["primary"]))
        short_title = title[:22] + ("…" if len(title) > 22 else "")
        svg.append(f'<text x="{cx}" y="{cy + 42}" font-family="{font}" font-size="21" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(short_title)}</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 7. FISHBONE CAUSE & EFFECT (دیاگرام استخوان ماهی / ریشه‌یابی علل)
    # ==========================================================================
    @staticmethod
    def render_fishbone_cause_effect(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        items = _extract_items(slide)[:4]
        title = slide.get("title", "تحلیل ریشه‌ای عوامل")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "تحلیل علت و معلولی (Ishikawa)"))

        spine_y = 585
        head_x = 240 if rtl else 1680
        tail_x = 1760 if rtl else 160

        # Main Spine Line
        svg.append(f'<line x1="{tail_x}" y1="{spine_y}" x2="{head_x}" y2="{spine_y}" stroke="{renderer.theme["primary"]}" stroke-width="5" />')

        # Spinning Fishbone Target Head
        svg.append('<g id="spin_fishbone_head">')
        svg.append(f'<circle cx="{head_x}" cy="{spine_y}" r="110" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2.5" stroke-dasharray="10 6" />')
        svg.append(f'<circle cx="{head_x + 110}" cy="{spine_y}" r="5" fill="{renderer.theme["accent"]}" />')
        svg.append('</g>')

        svg.append('<g id="fishbone_effect_node">')
        svg.extend(renderer._render_icon_badge(head_x, spine_y - 16, 48, renderer.theme["primary"], "target", icon_size=48))
        svg.append(f'<text x="{head_x}" y="{spine_y + 62}" font-family="{font}" font-size="20" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="middle">هدف / اثر اصلی</text>')
        svg.append('</g>')

        rib_slots = [
            (620, 225, 480, 285, 760, spine_y, renderer.theme["primary"]),
            (1180, 225, 480, 285, 1320, spine_y, renderer.theme["secondary"]),
            (620, 660, 480, 285, 760, spine_y, renderer.theme["accent"]),
            (1180, 660, 480, 285, 1320, spine_y, renderer.theme["primary"]),
        ]

        for idx, item in enumerate(items[:4]):
            cx_box, cy_box, bw, bh, join_x, join_y, col = rib_slots[idx]
            rib_start_y = (cy_box + bh) if cy_box < spine_y else cy_box
            svg.append(f'<line x1="{cx_box + bw/2}" y1="{rib_start_y}" x2="{join_x}" y2="{join_y}" stroke="{col}" stroke-width="3.5" />')
            svg.append(f'<circle cx="{join_x}" cy="{join_y}" r="8" fill="{col}" />')

            svg.append(f'<g id="fishbone_rib_{idx+1}">')
            svg.extend(renderer._card_rect(cx_box, cy_box, bw, bh, rx=22, stroke_width=2.0))
            tx = (cx_box + bw - 35) if rtl else (cx_box + 35)
            svg.append(f'<text x="{tx}" y="{cy_box + 56}" font-family="{font}" font-size="23" font-weight="700" fill="{col}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = cy_box + 104
            for line in desc_lines[:4]:
                svg.append(f'<text x="{tx}" y="{dy}" font-family="{font}" font-size="18" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">• {escape_xml(line)}</text>')
                dy += 36
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 8. DATA CHART SHOWCASE (نمودار برداری راداری / دونات با رنگ‌بندی خودکار تم)
    # ==========================================================================
    @staticmethod
    def render_data_chart_showcase(renderer, slide: Dict[str, Any], slide_idx: int = 4) -> str:
        items = _extract_items(slide)[:5]
        title = slide.get("title", "تحلیل داده‌ها و شاخص‌های کمی")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "داشبورد نموداری و بصری‌سازی داده"))

        # Left/Right Radar + Donut Hybrid Vector Chart Panel
        chart_cx = 500 if rtl else 1420
        chart_cy = 585
        chart_r = 220

        # Spinning Radar Calibration Ring
        svg.append('<g id="spin_chart_calibration">')
        svg.append(f'<circle cx="{chart_cx}" cy="{chart_cy}" r="{chart_r + 45}" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="8 8" stroke-opacity="0.55" />')
        svg.append(f'<circle cx="{chart_cx + chart_r + 45}" cy="{chart_cy}" r="6" fill="{renderer.theme["accent"]}" />')
        svg.append('</g>')

        svg.append('<g id="native_vector_radar_chart">')
        # Concentric Radar Webs
        for ring_frac in (0.35, 0.68, 1.0):
            rr = chart_r * ring_frac
            svg.append(f'<circle cx="{chart_cx}" cy="{chart_cy}" r="{rr}" fill="none" stroke="{renderer.theme["surface_border"]}" stroke-width="1.5" />')

        # 5-Axis Radar Polygon
        radii_ratios = [0.92, 0.78, 0.86, 0.74, 0.88]
        poly_pts = []
        n_axes = 5
        for a_i in range(n_axes):
            angle = -math.pi / 2 + (2 * math.pi * a_i / n_axes)
            ax_x = chart_cx + chart_r * math.cos(angle)
            ax_y = chart_cy + chart_r * math.sin(angle)
            svg.append(f'<line x1="{chart_cx}" y1="{chart_cy}" x2="{ax_x}" y2="{ax_y}" stroke="{renderer.theme["surface_border"]}" stroke-width="1.5" />')

            val_r = chart_r * radii_ratios[a_i % len(radii_ratios)]
            px = chart_cx + val_r * math.cos(angle)
            py = chart_cy + val_r * math.sin(angle)
            poly_pts.append(f"{px:.1f},{py:.1f}")

        pts_str = " ".join(poly_pts)
        svg.append(f'<polygon points="{pts_str}" fill="{renderer.theme["primary"]}" fill-opacity="0.28" stroke="{renderer.theme["primary"]}" stroke-width="3.5" />')
        for pt in poly_pts:
            px_s, py_s = pt.split(",")
            svg.append(f'<circle cx="{px_s}" cy="{py_s}" r="7" fill="{renderer.theme["accent"]}" stroke="{renderer.theme["background"]}" stroke-width="2" />')
        svg.append('</g>')

        # Verbatim Insight Cards Stack
        stack_x = 880 if rtl else 120
        stack_w = 920
        count = max(1, min(3, len(items)))
        card_h = (690 - ((count - 1) * 26)) / count

        colors = [renderer.theme["primary"], renderer.theme["secondary"], renderer.theme["accent"]]
        for i, item in enumerate(items[:3]):
            cy_card = 235 + i * (card_h + 26)
            col = colors[i % len(colors)]
            svg.append(f'<g id="chart_insight_card_{i+1}">')
            svg.extend(renderer._card_rect(stack_x, cy_card, stack_w, card_h, rx=24, stroke_width=2.0))

            num_val = item["number"] or (to_persian_digits(f"{92 - i*7}%") if rtl else f"{92 - i*7}%")
            badge_cx = (stack_x + stack_w - 85) if rtl else (stack_x + 85)
            badge_cy = cy_card + card_h / 2
            svg.extend(renderer._card_rect(badge_cx - 52, badge_cy - 44, 104, 88, rx=18, stroke_width=2.2, top_accent=False))
            svg.append(f'<text x="{badge_cx}" y="{badge_cy + 10}" font-family="{font}" font-size="26" font-weight="900" fill="{col}" text-anchor="middle">{escape_xml(num_val)}</text>')

            tx = (stack_x + stack_w - 165) if rtl else (stack_x + 165)
            svg.append(f'<text x="{tx}" y="{cy_card + 62}" font-family="{font}" font-size="25" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            desc_lines = [l.strip() for l in item["desc"].split("\n") if l.strip()]
            dy = cy_card + 106
            for line in desc_lines[:3]:
                svg.append(f'<text x="{tx}" y="{dy}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">• {escape_xml(line)}</text>')
                dy += 34
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 9. SMART TABLE MATRIX (جدول ماتریسی چندستونه هوشمند)
    # ==========================================================================
    @staticmethod
    def render_smart_table_matrix(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        items = _extract_items(slide)[:5]
        title = slide.get("title", "ماتریس ارزیابی و جدول مشخصات")
        rtl = is_persian(title) or any(is_persian(x["title"]) for x in items)
        font = renderer.theme.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]
        svg.extend(InfographicLayoutRenderer._render_slide_header(renderer, slide, rtl, "جدول ساختاریافته و ماتریس تحلیلی"))

        table_x = 120
        table_y = 225
        table_w = 1680
        header_h = 74
        row_count = max(1, len(items))
        row_h = min(135, (680 - header_h) / row_count)

        # Table Header Bar
        svg.append('<g id="smart_table_header">')
        svg.append(f'<rect x="{table_x}" y="{table_y}" width="{table_w}" height="{header_h}" rx="8" fill="{renderer.theme["primary"]}" />')
        if rtl:
            svg.append(f'<text x="1740" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="end">محور / شاخص کلیدی</text>')
            svg.append(f'<text x="1220" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="end">شرح و جزئیات تخصصی</text>')
            svg.append(f'<text x="260" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="middle">وضعیت</text>')
        else:
            svg.append(f'<text x="180" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="start">KEY PARAMETER</text>')
            svg.append(f'<text x="680" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="start">SPECIFICATION &amp; DETAILS</text>')
            svg.append(f'<text x="1640" y="{table_y + 46}" font-family="{font}" font-size="22" font-weight="800" fill="{renderer.theme["background"]}" text-anchor="middle">STATUS</text>')
        svg.append('</g>')

        for i, item in enumerate(items):
            ry = table_y + header_h + 12 + i * (row_h + 12)
            svg.append(f'<g id="table_row_{i+1}">')
            svg.extend(renderer._card_rect(table_x, ry, table_w, row_h, rx=14, stroke_width=1.6, top_accent=False))

            mid_ry = ry + row_h / 2 + 4
            col_t = 1740 if rtl else 180
            col_d = 1220 if rtl else 680
            col_s = 260 if rtl else 1640

            svg.append(f'<text x="{col_t}" y="{mid_ry + 8}" font-family="{font}" font-size="23" font-weight="700" fill="{renderer.theme["text_main"]}" text-anchor="{align}">{escape_xml(item["title"])}</text>')

            flat_desc = " | ".join([l.strip() for l in item["desc"].split("\n") if l.strip()])
            svg.append(f'<text x="{col_d}" y="{mid_ry + 8}" font-family="{font}" font-size="19" font-weight="400" fill="{renderer.theme["text_muted"]}" text-anchor="{align}">{escape_xml(flat_desc[:95])}</text>')

            status_lbl = item["trend"] or item["number"] or ("✓ تاییدشده" if rtl else "✓ VERIFIED")
            svg.append(f'<rect x="{col_s - 90}" y="{mid_ry - 20}" width="180" height="40" rx="10" fill="{renderer.theme["badge_bg"]}" stroke="{renderer.theme["secondary"]}" stroke-width="1.8" />')
            svg.append(f'<text x="{col_s}" y="{mid_ry + 7}" font-family="{font}" font-size="16" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">{escape_xml(status_lbl)}</text>')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 10. HERO CALLOUT QUOTE (اسلاید نقل‌قول و پیام کلیدی برجسته)
    # ==========================================================================
    @staticmethod
    def render_hero_callout_quote(renderer, slide: Dict[str, Any], slide_idx: int = 5) -> str:
        items = _extract_items(slide)
        title = slide.get("title", "پیام کلیدی و چشم‌انداز")
        subtitle = slide.get("subtitle", items[0]["desc"] if items else "")
        rtl = is_persian(title) or is_persian(subtitle)
        font = renderer.theme.get("font_fa" if rtl else "font_en")

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        cx, cy = 960, 520

        # Spinning Ambient Aura behind Callout
        svg.append('<g id="spin_quote_aura">')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="360" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2" stroke-dasharray="14 10" stroke-opacity="0.4" />')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="410" fill="none" stroke="{renderer.theme["secondary"]}" stroke-width="1.2" stroke-dasharray="6 12" stroke-opacity="0.3" />')
        svg.append(f'<circle cx="{cx + 360}" cy="{cy}" r="7" fill="{renderer.theme["accent"]}" />')
        svg.append('</g>')

        svg.append('<g id="hero_quote_card">')
        svg.extend(renderer._card_rect(200, 180, 1520, 720, rx=38, stroke_width=2.5))
        svg.append(f'<text x="{cx}" y="310" font-family="serif" font-size="160" font-weight="900" fill="{renderer.theme["primary"]}" fill-opacity="0.22" text-anchor="middle">“</text>')

        svg.append(f'<text x="{cx}" y="380" font-family="{font}" font-size="44" font-weight="800" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(title)}</text>')
        svg.append(f'<line x1="760" y1="430" x2="1160" y2="430" stroke="{renderer.theme["primary"]}" stroke-width="3" />')

        curr_y = 510
        for item in items[:3]:
            line_txt = f"{item['title']}: {item['desc'].replace(chr(10), ' — ')}" if item["desc"] else item["title"]
            svg.append(f'<text x="{cx}" y="{curr_y}" font-family="{font}" font-size="25" font-weight="500" fill="{renderer.theme["text_muted"]}" text-anchor="middle">{escape_xml(line_txt[:110])}</text>')
            curr_y += 70
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    # ==========================================================================
    # 11. CLOSING THANK YOU (اسلاید جمع‌بندی و پایانی باشکوه)
    # ==========================================================================
    @staticmethod
    def render_closing_thankyou(renderer, slide: Dict[str, Any], slide_idx: int = 6) -> str:
        items = _extract_items(slide)
        title = slide.get("title", "سپاس از توجه و همراهی شما")
        kicker = slide.get("kicker", "جمع‌بندی و پرسش و پاسخ")
        rtl = is_persian(title)
        font = renderer.theme.get("font_fa" if rtl else "font_en")

        svg = [renderer._header_svg(rtl, slide_idx=slide_idx)]

        cx, cy = 960, 440

        # Spinning Grand Finale Medallion Rings
        svg.append('<g id="spin_closing_emblem">')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="195" fill="none" stroke="{renderer.theme["primary"]}" stroke-width="2.5" stroke-dasharray="10 8" stroke-opacity="0.65" />')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="230" fill="none" stroke="{renderer.theme["secondary"]}" stroke-width="1.5" stroke-dasharray="5 9" stroke-opacity="0.45" />')
        svg.append(f'<circle cx="{cx + 195}" cy="{cy}" r="7" fill="{renderer.theme["accent"]}" />')
        svg.append(f'<circle cx="{cx - 195}" cy="{cy}" r="7" fill="{renderer.theme["primary"]}" />')
        svg.append('</g>')

        svg.append('<g id="closing_centerpiece">')
        svg.extend(renderer._card_rect(cx - 160, cy - 140, 320, 280))
        svg.extend(renderer._render_icon_badge(cx, cy - 28, 48, renderer.theme["primary"], "award", icon_size=54))
        svg.append(f'<text x="{cx}" y="{cy + 75}" font-family="{font}" font-size="22" font-weight="700" fill="{renderer.theme["secondary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')

        svg.append(f'<text x="{cx}" y="735" font-family="{font}" font-size="54" font-weight="900" fill="{renderer.theme["text_main"]}" text-anchor="middle">{escape_xml(title)}</text>')

        if items:
            summary_str = "  ✦  ".join([x["title"] for x in items[:3]])
            svg.extend(renderer._card_rect(310, 795, 1300, 78, rx=24, stroke_width=2.0, top_accent=False))
            svg.append(f'<text x="{cx}" y="844" font-family="{font}" font-size="22" font-weight="600" fill="{renderer.theme["text_muted"]}" text-anchor="middle">{escape_xml(summary_str)}</text>')
        svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)
