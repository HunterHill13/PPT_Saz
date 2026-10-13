#!/usr/bin/env python3
"""
PPT_Saz v5.5 — Polymorphic Art-Style Visual Skin Engine

Eliminates visual similarity across themes by transforming the 5 foundational
visual primitives for all 9 Art-Style Archetypes:
  1. Container Silhouettes (`render_card_container`)
  2. Slide Headers (`render_style_header`)
  3. Icon Badges (`render_icon_badge`)
  4. Ambient Canvas & Structural Framing (`render_ambient_canvas`)
  5. Cover Slide Posters (`render_cover_slide`)

Supported 9 Art-Style Archetypes:
  - cyber_hud           (Sci-Fi Chamfered Polygons, Radar Reticles, Hexagons, Telemetry Bars)
  - neo_brutalist       (Retro OS Windows with Traffic-Light Buttons, Hard Black Shadows, Tilted Stickers)
  - swiss_academic      (Josef Müller-Brockmann Razor Grid, rx=0 Spine Blocks, Crosshair Ticks)
  - apple_bento         (iOS Squircle Glass Cards, Specular Top Rim, Dynamic Island Header)
  - warm_editorial      (Roman Architectural Arches, Vogue Double-Rule Masthead, Botanical Medallions)
  - royal_gold          (Art-Deco Beveled Octagons, Symmetrical Imperial Wings, 8-Point Star Crests)
  - bauhaus_modern      (Weimar 1923 Constructivist Color-Blocks, Primary Circle/Triangle/Square Geometry)
  - paper_cutout        (Memphis 80s Pop Collage, Layered Cutout Polygons, Masking-Tape Strips)
  - blueprint_schematic (Architectural CAD Cyanotype, Extended Construction Lines, Title Block Stamps)
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional

from icon_mapper import get_icon_svg_content


def is_persian(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]', str(text)))


def to_persian_digits(num: int | str) -> str:
    return str(num).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


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


def _hex_points(cx: float, cy: float, r: float) -> str:
    pts = []
    for i in range(6):
        ang = math.radians(60 * i - 30)
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    return " ".join(pts)


class ArtStyleSkinEngine:
    """Polymorphic Visual Skin Engine transforming containers, headers, icons, backgrounds, and covers."""

    # ==========================================================================
    # 1. POLYMORPHIC CONTAINER SILHOUETTES (`render_card_container`)
    # ==========================================================================
    @staticmethod
    def render_card_container(
        renderer,
        x: float,
        y: float,
        w: float,
        h: float,
        rx: float = 28,
        stroke_width: float = 2.0,
        top_accent: bool = True,
    ) -> List[str]:
        arch = renderer.archetype
        th = renderer.theme
        primary = th["primary"]
        secondary = th["secondary"]
        accent = th.get("accent", primary)
        surface = th["surface"]
        border = th["surface_border"]
        out: List[str] = []

        if arch == "neo_brutalist":
            # Retro OS Window with Hard Offset Shadow, rx=0, Top Window Bar & Traffic Light Buttons
            shadow_col = "#000000" if not renderer.is_dark else primary
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            bar_h = 22
            out.append(f'<rect x="{x + 10}" y="{y + 10}" width="{w}" height="{h}" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border_col}" stroke-width="4" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{bar_h}" rx="0" fill="{primary}" stroke="{border_col}" stroke-width="3.5" />')
            # 3 Retro OS Window Traffic Light Buttons
            for b_idx, b_col in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
                bx = x + 16 + (b_idx * 18)
                by = y + 11
                out.append(f'<circle cx="{bx}" cy="{by}" r="5.5" fill="{b_col}" stroke="#000000" stroke-width="1.8" />')
            out.append(f'<line x1="{x + w - 28}" y1="{y + 11}" x2="{x + w - 12}" y2="{y + 11}" stroke="#000000" stroke-width="2.5" />')

        elif arch == "cyber_hud":
            # 45-Degree Chamfered Sci-Fi Polygon + Corner Targeting Brackets
            cut = min(26.0, h * 0.16, w * 0.12)
            notch = min(12.0, cut * 0.5)
            pts = (
                f"{x + cut},{y} "
                f"{x + w - notch},{y} "
                f"{x + w},{y + notch} "
                f"{x + w},{y + h - cut} "
                f"{x + w - cut},{y + h} "
                f"{x + notch},{y + h} "
                f"{x},{y + h - notch} "
                f"{x},{y + cut}"
            )
            out.append(f'<polygon points="{pts}" fill="{surface}" stroke="{border}" stroke-width="{stroke_width}" />')
            # Top HUD trapezoid tab
            tab_w = min(140.0, w * 0.35)
            tab_pts = f"{x + cut + 10},{y} {x + cut + 10 + tab_w},{y} {x + cut + tab_w},{y + 7} {x + cut + 2},{y + 7}"
            out.append(f'<polygon points="{tab_pts}" fill="{primary}" />')
            # Glowing HUD Corner Brackets
            bl = 24
            out.append(f'<path d="M {x},{y + cut + bl} L {x},{y + cut} L {x + cut},{y} L {x + cut + bl},{y}" fill="none" stroke="{primary}" stroke-width="3.5" />')
            out.append(f'<path d="M {x + w},{y + h - cut - bl} L {x + w},{y + h - cut} L {x + w - cut},{y + h} L {x + w - cut - bl},{y + h}" fill="none" stroke="{secondary}" stroke-width="3.5" />')
            # Bottom micro telemetry barcode ticks
            for t_i in range(4):
                tx = x + 24 + t_i * 12
                out.append(f'<rect x="{tx}" y="{y + h - 8}" width="6" height="3" fill="{primary}" fill-opacity="0.7" />')

        elif arch == "swiss_academic":
            # Razor-Sharp rx=0 International Typographic Grid Sheet + Structural Spine + Corner Ticks
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border}" stroke-width="1.5" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="0" fill="{primary}" />')
            out.append(f'<rect x="{x}" y="{y}" width="80" height="8" rx="0" fill="{secondary}" />')
            out.append(f'<line x1="{x}" y1="{y + h - 10}" x2="{x + w}" y2="{y + h - 10}" stroke="{border}" stroke-width="1" />')
            # Exposed Swiss Registration Crosshairs at 4 corners
            for cx_t, cy_t in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
                out.append(f'<line x1="{cx_t - 7}" y1="{cy_t}" x2="{cx_t + 7}" y2="{cy_t}" stroke="{secondary}" stroke-width="1.8" />')
                out.append(f'<line x1="{cx_t}" y1="{cy_t - 7}" x2="{cx_t}" y2="{cy_t + 7}" stroke="{secondary}" stroke-width="1.8" />')

        elif arch == "bauhaus_modern":
            # Weimar 1923 Constructivist Block: rx=0, Thick Structural Border, Geometric Color-Blocks
            border_col = th["surface_border"]
            out.append(f'<rect x="{x + 6}" y="{y + 6}" width="{w}" height="{h}" rx="0" fill="{secondary}" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border_col}" stroke-width="3.5" />')
            # Top Constructivist Color-Block Bar (Red + Yellow + Blue segments)
            seg1 = min(120.0, w * 0.3)
            seg2 = min(70.0, w * 0.18)
            out.append(f'<rect x="{x}" y="{y}" width="{seg1}" height="12" fill="{primary}" stroke="{border_col}" stroke-width="2" />')
            out.append(f'<rect x="{x + seg1}" y="{y}" width="{seg2}" height="12" fill="{accent}" stroke="{border_col}" stroke-width="2" />')
            # Bottom- corner Bauhaus Quarter-Circle Wedge
            wedge_r = min(36.0, h * 0.22)
            out.append(f'<path d="M {x},{y + h - wedge_r} A {wedge_r},{wedge_r} 0 0,1 {x + wedge_r},{y + h} L {x},{y + h} Z" fill="{primary}" fill-opacity="0.85" />')

        elif arch == "paper_cutout":
            # Memphis 80s Layered Paper Cutout + Contrasting Back-Sheet + Masking Tape Strip at Top
            back_pts = f"{x - 4},{y + 8} {x + w + 8},{y + 4} {x + w + 4},{y + h + 9} {x + 6},{y + h + 6}"
            out.append(f'<polygon points="{back_pts}" fill="{secondary}" fill-opacity="0.85" />')
            front_pts = f"{x + 3},{y} {x + w},{y + 2} {x + w - 3},{y + h} {x},{y + h - 2}"
            out.append(f'<polygon points="{front_pts}" fill="{surface}" stroke="{border}" stroke-width="2.8" />')
            # Translucent Masking Tape Strip holding the top center of the cutout card
            tape_w = min(110.0, w * 0.28)
            tape_x = x + (w - tape_w) / 2
            tape_pts = f"{tape_x},{y - 9} {tape_x + tape_w},{y - 6} {tape_x + tape_w - 4},{y + 11} {tape_x - 4},{y + 8}"
            out.append(f'<polygon points="{tape_pts}" fill="{accent}" fill-opacity="0.88" stroke="{border}" stroke-width="1.5" />')

        elif arch == "blueprint_schematic":
            # Architectural CAD Blueprint Box: rx=0, Extended Construction Lines, Hatch Stamp & Dimensions
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<rect x="{x + 5}" y="{y + 5}" width="{w - 10}" height="{h - 10}" rx="0" fill="none" stroke="{secondary}" stroke-width="0.8" stroke-dasharray="6 4" />')
            # Construction line extensions past all 4 corners
            ext = 14
            out.append(f'<line x1="{x - ext}" y1="{y}" x2="{x + w + ext}" y2="{y}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x - ext}" y1="{y + h}" x2="{x + w + ext}" y2="{y + h}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x}" y1="{y - ext}" x2="{x}" y2="{y + h + ext}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x + w}" y1="{y - ext}" x2="{x + w}" y2="{y + h + ext}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            # Corner CAD spec stamp
            stamp_w = min(115.0, w * 0.3)
            out.append(f'<rect x="{x}" y="{y}" width="{stamp_w}" height="16" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="1.2" />')
            out.append(f'<text x="{x + stamp_w / 2}" y="{y + 12}" font-family="monospace" font-size="10" font-weight="700" fill="{primary}" text-anchor="middle">CAD // {int(w)}x{int(h)}</text>')

        elif arch == "royal_gold":
            # Art-Deco Imperial Beveled Octagon + Double Gold Filigree + Corner Diamond Studs
            cut = min(20.0, h * 0.14, w * 0.1)
            pts_outer = (
                f"{x + cut},{y} {x + w - cut},{y} {x + w},{y + cut} {x + w},{y + h - cut} "
                f"{x + w - cut},{y + h} {x + cut},{y + h} {x},{y + h - cut} {x},{y + cut}"
            )
            ins = 7
            cut_in = max(8.0, cut - 4)
            pts_inner = (
                f"{x + ins + cut_in},{y + ins} {x + w - ins - cut_in},{y + ins} "
                f"{x + w - ins},{y + ins + cut_in} {x + w - ins},{y + h - ins - cut_in} "
                f"{x + w - ins - cut_in},{y + h - ins} {x + ins + cut_in},{y + h - ins} "
                f"{x + ins},{y + h - ins - cut_in} {x + ins},{y + ins + cut_in}"
            )
            out.append(f'<polygon points="{pts_outer}" fill="{surface}" stroke="{primary}" stroke-width="2.2" />')
            out.append(f'<polygon points="{pts_inner}" fill="none" stroke="{primary}" stroke-width="0.9" stroke-opacity="0.55" />')
            # Gold Diamond Studs on top and bottom center
            for d_x, d_y in ((x + w / 2, y), (x + w / 2, y + h)):
                out.append(f'<polygon points="{d_x},{d_y - 6} {d_x + 6},{d_y} {d_x},{d_y + 6} {d_x - 6},{d_y}" fill="{primary}" />')

        elif arch == "warm_editorial":
            # Classical Roman Arch / Scalloped Editorial Frame + Warm Paper Shadow
            out.append(f'<rect x="{x + 6}" y="{y + 8}" width="{w}" height="{h}" rx="28" fill="{th.get("wave_2", border)}" fill-opacity="0.65" />')
            arch_r = min(36.0, w * 0.15, h * 0.2)
            path_d = (
                f"M {x},{y + arch_r} "
                f"A {arch_r},{arch_r} 0 0,1 {x + arch_r},{y} "
                f"L {x + w - arch_r},{y} "
                f"A {arch_r},{arch_r} 0 0,1 {x + w},{y + arch_r} "
                f"L {x + w},{y + h - 8} "
                f"Q {x + w},{y + h} {x + w - 8},{y + h} "
                f"L {x + 8},{y + h} "
                f"Q {x},{y + h} {x},{y + h - 8} Z"
            )
            out.append(f'<path d="{path_d}" fill="{surface}" stroke="{border}" stroke-width="2.2" />')
            out.append(f'<line x1="{x + 28}" y1="{y + 10}" x2="{x + w - 28}" y2="{y + 10}" stroke="{primary}" stroke-width="2.5" />')
            out.append(f'<line x1="{x + 42}" y1="{y + 15}" x2="{x + w - 42}" y2="{y + 15}" stroke="{secondary}" stroke-width="1" />')

        else:  # apple_bento
            # iOS Squircle Glass Card with Inner Rim & Top Specular Reflection
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36" fill="{surface}" stroke="{border}" stroke-width="2" />')
            out.append(f'<rect x="{x + 5}" y="{y + 5}" width="{w - 10}" height="{h - 10}" rx="31" fill="none" stroke="{primary}" stroke-width="0.8" stroke-opacity="0.3" />')
            if top_accent:
                out.append(f'<rect x="{x + 36}" y="{y}" width="{w - 72}" height="3.5" rx="1.75" fill="{primary}" fill-opacity="0.8" />')
            out.append(f'<circle cx="{x + w - 24}" cy="{y + 22}" r="4.5" fill="{secondary}" fill-opacity="0.6" />')

        return out

    # ==========================================================================
    # 2. POLYMORPHIC ICON BADGES (`render_icon_badge`)
    # ==========================================================================
    @staticmethod
    def render_icon_badge(
        renderer,
        cx: float,
        cy: float,
        r: float,
        color: str,
        icon_key: str,
        icon_size: Optional[int] = None,
    ) -> List[str]:
        arch = renderer.archetype
        th = renderer.theme
        badge_bg = th["badge_bg"]
        sz = icon_size or int(r * 1.1)
        out: List[str] = []

        if arch == "neo_brutalist":
            # Chunky Sharp Square with Hard Offset Black Shadow
            shadow_col = "#000000" if not renderer.is_dark else color
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            out.append(f'<rect x="{cx - r + 5}" y="{cy - r + 5}" width="{r * 2}" height="{r * 2}" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{border_col}" stroke-width="3" />')

        elif arch == "cyber_hud":
            # Sci-Fi Hexagon + Dashed Outer Radar Ring
            hex_pts = _hex_points(cx, cy, r + 2)
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="{color}" stroke-width="1.4" stroke-dasharray="5 4" stroke-opacity="0.65" />')
            out.append(f'<polygon points="{hex_pts}" fill="{badge_bg}" stroke="{color}" stroke-width="2.5" />')

        elif arch == "swiss_academic":
            # Sharp Architectural Square + Top Color Strip + Corner Crosshairs
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{color}" stroke-width="2" />')
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="6" rx="0" fill="{color}" />')

        elif arch == "bauhaus_modern":
            # Bauhaus Tri-Geometry Emblem (Square + Offset Circle + Corner Triangle)
            border_col = th["surface_border"]
            out.append(f'<rect x="{cx - r + 4}" y="{cy - r + 4}" width="{r * 2}" height="{r * 2}" rx="0" fill="{color}" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{badge_bg}" stroke="{border_col}" stroke-width="3" />')

        elif arch == "paper_cutout":
            # Playful Tilted Polygon Sticker with Contrasting Paper Shadow
            s_pts = f"{cx - r + 2},{cy - r + 6} {cx + r + 6},{cy - r + 2} {cx + r + 2},{cy + r + 6} {cx - r + 6},{cy + r + 2}"
            f_pts = f"{cx - r - 2},{cy - r + 2} {cx + r + 2},{cy - r - 2} {cx + r - 2},{cy + r + 2} {cx - r + 2},{cy + r - 2}"
            out.append(f'<polygon points="{s_pts}" fill="{color}" />')
            out.append(f'<polygon points="{f_pts}" fill="{badge_bg}" stroke="{th["surface_border"]}" stroke-width="2.5" />')

        elif arch == "blueprint_schematic":
            # CAD Compass Reticle (Square + Inscribed Circle + Extended Axis Ticks)
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{color}" stroke-width="1.8" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.85}" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="4 3" />')
            out.append(f'<line x1="{cx - r - 7}" y1="{cy}" x2="{cx + r + 7}" y2="{cy}" stroke="{color}" stroke-width="1.2" stroke-opacity="0.6" />')
            out.append(f'<line x1="{cx}" y1="{cy - r - 7}" x2="{cx}" y2="{cy + r + 7}" stroke="{color}" stroke-width="1.2" stroke-opacity="0.6" />')

        elif arch == "royal_gold":
            # 8-Pointed Royal Star / Diamond Crest
            d = r * 1.12
            s = r * 0.82
            out.append(f'<rect x="{cx - s}" y="{cy - s}" width="{s * 2}" height="{s * 2}" fill="{badge_bg}" stroke="{color}" stroke-width="2" />')
            out.append(f'<polygon points="{cx},{cy - d} {cx + d},{cy} {cx},{cy + d} {cx - d},{cy}" fill="{badge_bg}" stroke="{color}" stroke-width="2.2" />')

        elif arch == "warm_editorial":
            # Roman Arch / Botanical Double Medallion
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 5}" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="3 3" />')
            out.append(f'<path d="M {cx - r},{cy + r * 0.8} L {cx - r},{cy - r * 0.2} A {r},{r} 0 0,1 {cx + r},{cy - r * 0.2} L {cx + r},{cy + r * 0.8} Z" fill="{badge_bg}" stroke="{color}" stroke-width="2.2" />')

        else:  # apple_bento
            # iOS App-Icon Squircle with Inner Glass Rim
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="{r * 0.52:.1f}" fill="{badge_bg}" stroke="{color}" stroke-width="2.2" />')
            out.append(f'<circle cx="{cx + r - 6}" cy="{cy - r + 6}" r="3.5" fill="{color}" />')

        out.append(get_icon_svg_content(icon_key, cx - sz / 2, cy - sz / 2, size=sz, stroke_color=color))
        return out

    # ==========================================================================
    # 3. POLYMORPHIC SLIDE HEADERS (`render_style_header`)
    # ==========================================================================
    @staticmethod
    def render_style_header(
        renderer,
        slide: Dict[str, Any],
        rtl: bool,
        default_kicker: str,
    ) -> List[str]:
        arch = renderer.archetype
        th = renderer.theme
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", default_kicker)
        font = th.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"
        title_x = 1800 if rtl else 120
        primary = th["primary"]
        secondary = th["secondary"]
        accent = th.get("accent", primary)

        out = ['<g id="header_group">']

        if arch == "neo_brutalist":
            # Tilted Sticker Tape Header + Hard Black Shadow + Bold Highlighter Underline
            shadow_col = "#000000" if not renderer.is_dark else secondary
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            kw = 280
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx + 6}" y="66" width="{kw}" height="40" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{kx}" y="60" width="{kw}" height="40" rx="0" fill="{primary}" stroke="{border_col}" stroke-width="3.5" />')
            k_txt_col = "#000000" if not renderer.is_dark else "#111111"
            out.append(f'<text x="{kx + kw / 2}" y="87" font-family="{font}" font-size="17" font-weight="900" fill="{k_txt_col}" text-anchor="middle">★ {escape_xml(kicker)}</text>')
            # Highlighter bar behind title
            hl_w = min(720, max(320, len(title) * 22))
            hl_x = (title_x - hl_w) if rtl else title_x
            out.append(f'<rect x="{hl_x}" y="148" width="{hl_w}" height="18" fill="{secondary}" fill-opacity="0.35" />')
            out.append(f'<text x="{title_x}" y="160" font-family="{font}" font-size="44" font-weight="900" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')

        elif arch == "cyber_hud":
            # Sci-Fi Trapezoid HUD Scanner Header + Laser Reticle Line
            kw = 290
            if rtl:
                pts = f"{title_x},{64} {title_x - kw + 22},{64} {title_x - kw},{102} {title_x},{102}"
                kx_mid = title_x - kw / 2
            else:
                pts = f"{title_x},{64} {title_x + kw - 22},{64} {title_x + kw},{102} {title_x},{102}"
                kx_mid = title_x + kw / 2
            out.append(f'<polygon points="{pts}" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<text x="{kx_mid}" y="89" font-family="{font}" font-size="16" font-weight="700" fill="{primary}" text-anchor="middle">[ {escape_xml(kicker)} ]</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            line_x1 = 1800 if rtl else 120
            line_x2 = 1100 if rtl else 820
            out.append(f'<line x1="{line_x1}" y1="180" x2="{line_x2}" y2="180" stroke="{primary}" stroke-width="2.5" />')
            out.append(f'<rect x="{(title_x - 70) if rtl else title_x}" y="176" width="70" height="8" fill="{accent}" />')

        elif arch == "swiss_academic":
            # International Grid Header: Razor Rule + Solid Classification Tag
            kw = 260
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="64" width="{kw}" height="36" rx="0" fill="{primary}" />')
            out.append(f'<text x="{kx + kw / 2}" y="88" font-family="{font}" font-size="16" font-weight="700" fill="{th["background"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="182" x2="1800" y2="182" stroke="{th["surface_border"]}" stroke-width="2" />')
            out.append(f'<rect x="{(title_x - 140) if rtl else title_x}" y="179" width="140" height="6" fill="{secondary}" />')

        elif arch == "bauhaus_modern":
            # Bauhaus Constructivist Header with ● ▲ ■ Geometric Primitives
            kw = 270
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="62" width="{kw}" height="38" rx="0" fill="{primary}" stroke="{th["surface_border"]}" stroke-width="3" />')
            out.append(f'<text x="{kx + kw / 2}" y="87" font-family="{font}" font-size="16" font-weight="900" fill="#FFFFFF" text-anchor="middle">■ ▲ ●  {escape_xml(kicker)}</text>')
            # Geometric Trio next to header
            g_x = (kx - 75) if rtl else (kx + kw + 25)
            out.append(f'<circle cx="{g_x}" cy="81" r="14" fill="{accent}" stroke="{th["surface_border"]}" stroke-width="2.5" />')
            out.append(f'<polygon points="{g_x + 36},67 {g_x + 52},95 {g_x + 20},95" fill="{secondary}" stroke="{th["surface_border"]}" stroke-width="2.5" />')
            out.append(f'<text x="{title_x}" y="160" font-family="{font}" font-size="44" font-weight="900" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<rect x="120" y="178" width="1680" height="5" fill="{th["surface_border"]}" />')

        elif arch == "paper_cutout":
            # Cutout Collage Banner + Memphis Zigzag Squiggle Underline
            kw = 270
            kx = (title_x - kw) if rtl else title_x
            pts_k = f"{kx - 6},64 {kx + kw + 4},60 {kx + kw - 4},102 {kx + 4},98"
            out.append(f'<polygon points="{pts_k}" fill="{th["badge_bg"]}" stroke="{th["surface_border"]}" stroke-width="2.5" />')
            out.append(f'<text x="{kx + kw / 2}" y="87" font-family="{font}" font-size="16" font-weight="800" fill="{th["text_main"]}" text-anchor="middle">✂ {escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            # Memphis Zigzag wave under title
            zx_start = (title_x - 320) if rtl else title_x
            zz_pts = " ".join([f"{zx_start + z_i * 20},{176 if z_i % 2 == 0 else 186}" for z_i in range(17)])
            out.append(f'<polyline points="{zz_pts}" fill="none" stroke="{primary}" stroke-width="3.5" />')

        elif arch == "blueprint_schematic":
            # CAD Engineering Title Stamp Header + Dimension Arrows
            kw = 310
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="60" width="{kw}" height="40" rx="0" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<line x1="{kx + 90}" y1="60" x2="{kx + 90}" y2="100" stroke="{primary}" stroke-width="1.5" />')
            out.append(f'<text x="{kx + 45}" y="85" font-family="monospace" font-size="14" font-weight="700" fill="{secondary}" text-anchor="middle">DWG//01</text>')
            out.append(f'<text x="{kx + 200}" y="86" font-family="{font}" font-size="15" font-weight="700" fill="{primary}" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="43" font-weight="700" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="180" x2="1800" y2="180" stroke="{primary}" stroke-width="1.5" stroke-dasharray="10 5" />')

        elif arch == "royal_gold":
            # Centered Art-Deco Imperial Winged Header
            cx = 960
            out.append(f'<polygon points="{cx - 170},64 {cx + 170},64 {cx + 190},82 {cx + 170},100 {cx - 170},100 {cx - 190},82" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<line x1="{cx - 340}" y1="82" x2="{cx - 200}" y2="82" stroke="{primary}" stroke-width="2" />')
            out.append(f'<line x1="{cx + 200}" y1="82" x2="{cx + 340}" y2="82" stroke="{primary}" stroke-width="2" />')
            out.append(f'<text x="{cx}" y="88" font-family="{font}" font-size="16" font-weight="700" fill="{primary}" text-anchor="middle">◆ {escape_xml(kicker)} ◆</text>')
            out.append(f'<text x="{cx}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="middle">{escape_xml(title)}</text>')
            out.append(f'<line x1="{cx - 260}" y1="178" x2="{cx + 260}" y2="178" stroke="{primary}" stroke-width="1.5" />')

        elif arch == "warm_editorial":
            # Vogue / Kinfolk Double-Rule Editorial Masthead
            out.append(f'<line x1="120" y1="62" x2="1800" y2="62" stroke="{primary}" stroke-width="3" />')
            out.append(f'<line x1="120" y1="68" x2="1800" y2="68" stroke="{secondary}" stroke-width="1" />')
            out.append(f'<text x="{title_x}" y="98" font-family="{font}" font-size="17" font-weight="700" fill="{primary}" text-anchor="{align}">✦ {escape_xml(kicker)} — EDITORIAL</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="700" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="180" x2="1800" y2="180" stroke="{th["surface_border"]}" stroke-width="1.5" />')

        else:  # apple_bento
            # Apple Dynamic Island Capsule with Dual Sensor Dots
            kw = 280
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="66" width="{kw}" height="40" rx="20" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="1.8" />')
            dot_x = (kx + kw - 24) if rtl else (kx + 24)
            out.append(f'<circle cx="{dot_x}" cy="86" r="6" fill="{primary}" />')
            out.append(f'<circle cx="{(dot_x - 16) if rtl else (dot_x + 16)}" cy="86" r="4" fill="{secondary}" />')
            out.append(f'<text x="{kx + kw / 2}" y="92" font-family="{font}" font-size="16" font-weight="700" fill="{primary}" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="162" font-family="{font}" font-size="45" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')

        out.append('</g>')
        return out

    # ==========================================================================
    # 4. POLYMORPHIC AMBIENT CANVAS (`render_ambient_canvas`)
    # ==========================================================================
    @staticmethod
    def render_ambient_canvas(renderer, is_rtl: bool, slide_idx: int = 1) -> List[str]:
        """Returns extra ambient SVG elements for the new art styles (Bauhaus, Paper Cutout, Blueprint)."""
        arch = renderer.archetype
        th = renderer.theme
        primary = th["primary"]
        secondary = th["secondary"]
        accent = th.get("accent", primary)
        border = th["surface_border"]
        extra: List[str] = []

        if arch == "bauhaus_modern":
            # Weimar 1923 Constructivist Geometric Blocks & Spinning Bauhaus Mobile
            extra.append(f"""
            <g id="bauhaus_ambient_geometry">
                <polygon points="0,0 260,0 0,260" fill="{primary}" fill-opacity="0.16" />
                <rect x="0" y="1040" width="1920" height="40" fill="{secondary}" fill-opacity="0.22" />
                <rect x="0" y="1034" width="640" height="6" fill="{primary}" />
                <rect x="640" y="1034" width="640" height="6" fill="{accent}" />
                <rect x="1280" y="1034" width="640" height="6" fill="{secondary}" />
                <line x1="90" y1="0" x2="90" y2="1080" stroke="{border}" stroke-width="1.5" stroke-opacity="0.2" />
                <line x1="1830" y1="0" x2="1830" y2="1080" stroke="{border}" stroke-width="1.5" stroke-opacity="0.2" />
            </g>
            """)
            mob_x = 1800 if is_rtl else 120
            mob_y = 940
            extra.append(f"""
            <g id="spin_bauhaus_mobile">
                <circle cx="{mob_x}" cy="{mob_y}" r="140" fill="none" stroke="{border}" stroke-width="3" stroke-dasharray="18 10" stroke-opacity="0.35" />
                <rect x="{mob_x - 45}" y="{mob_y - 45}" width="90" height="90" fill="none" stroke="{primary}" stroke-width="3" stroke-opacity="0.45" />
                <polygon points="{mob_x},{mob_y - 70} {mob_x + 60},{mob_y + 40} {mob_x - 60},{mob_y + 40}" fill="{accent}" fill-opacity="0.25" stroke="{border}" stroke-width="2" />
            </g>
            """)

        elif arch == "paper_cutout":
            # Memphis 80s Layered Paper Cutout Waves, Confetti & Spinning Pinwheel
            extra.append(f"""
            <g id="paper_cutout_collage_bg">
                <polygon points="0,820 480,760 980,860 1520,750 1920,830 1920,1080 0,1080" fill="{th.get('wave_1', accent)}" fill-opacity="0.45" />
                <polygon points="0,900 560,840 1180,930 1920,860 1920,1080 0,1080" fill="{th.get('wave_2', secondary)}" fill-opacity="0.65" />
                <polygon points="80,140 110,120 100,155" fill="{primary}" fill-opacity="0.5" />
                <polygon points="1820,180 1855,165 1840,200" fill="{secondary}" fill-opacity="0.5" />
                <circle cx="960" cy="70" r="10" fill="{accent}" fill-opacity="0.6" />
            </g>
            """)
            pin_x = 1790 if is_rtl else 130
            pin_y = 930
            extra.append(f"""
            <g id="spin_cutout_pinwheel">
                <polygon points="{pin_x},{pin_y} {pin_x - 90},{pin_y - 40} {pin_x - 40},{pin_y - 110}" fill="{primary}" fill-opacity="0.35" />
                <polygon points="{pin_x},{pin_y} {pin_x + 40},{pin_y - 90} {pin_x + 110},{pin_y - 40}" fill="{secondary}" fill-opacity="0.35" />
                <polygon points="{pin_x},{pin_y} {pin_x + 90},{pin_y + 40} {pin_x + 40},{pin_y + 110}" fill="{accent}" fill-opacity="0.35" />
                <polygon points="{pin_x},{pin_y} {pin_x - 40},{pin_y + 90} {pin_x - 110},{pin_y + 40}" fill="{primary}" fill-opacity="0.25" />
                <circle cx="{pin_x}" cy="{pin_y}" r="18" fill="{th['surface']}" stroke="{border}" stroke-width="3" />
            </g>
            """)

        elif arch == "blueprint_schematic":
            # Architectural CAD Blueprint Grid, Border Coordinate Frame & Vernier Caliper Rotor
            grid_svg = []
            for gx in range(160, 1840, 160):
                grid_svg.append(f'<line x1="{gx}" y1="40" x2="{gx}" y2="1040" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.22" />')
            for gy in range(140, 1020, 140):
                grid_svg.append(f'<line x1="40" y1="{gy}" x2="1880" y2="{gy}" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.22" />')
            # Outer CAD Drawing Sheet Border
            grid_svg.append(f'<rect x="32" y="32" width="1856" height="1016" fill="none" stroke="{primary}" stroke-width="2" stroke-opacity="0.55" />')
            grid_svg.append(f'<rect x="42" y="42" width="1836" height="996" fill="none" stroke="{secondary}" stroke-width="0.8" stroke-opacity="0.35" />')
            rot_x = 1790 if is_rtl else 130
            rot_y = 940
            extra.append(f'<g id="blueprint_cad_grid">{"".join(grid_svg)}</g>')
            extra.append(f"""
            <g id="spin_blueprint_rotor">
                <circle cx="{rot_x}" cy="{rot_y}" r="135" fill="none" stroke="{primary}" stroke-width="1.8" stroke-dasharray="12 4 3 4" stroke-opacity="0.45" />
                <circle cx="{rot_x}" cy="{rot_y}" r="95" fill="none" stroke="{secondary}" stroke-width="1.2" stroke-dasharray="4 6" stroke-opacity="0.4" />
                <line x1="{rot_x - 150}" y1="{rot_y}" x2="{rot_x + 150}" y2="{rot_y}" stroke="{primary}" stroke-width="1" stroke-opacity="0.4" />
                <line x1="{rot_x}" y1="{rot_y - 150}" x2="{rot_x}" y2="{rot_y + 150}" stroke="{primary}" stroke-width="1" stroke-opacity="0.4" />
            </g>
            """)

        return extra

    # ==========================================================================
    # 5. POLYMORPHIC COVER SLIDES (`render_cover_slide`)
    # ==========================================================================
    @staticmethod
    def render_cover_slide(renderer, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Renders a radically distinct Cover Slide architecture tailored to each of the 9 Art Styles."""
        arch = renderer.archetype
        th = renderer.theme
        title = slide.get("title", "عنوان ارائه")
        subtitle = slide.get("subtitle", "")
        author = slide.get("author", "")
        kicker = slide.get("kicker", "ارائه تخصصی")
        rtl = is_persian(title) or is_persian(subtitle)

        font = th.get("font_fa" if rtl else "font_en")
        align = "end" if rtl else "start"
        x_pos = 1740 if rtl else 160
        img_x = 110 if rtl else 1050

        svg = [renderer._header_svg(rtl, slide_idx=1)]

        # Style-Specific Cover Framing around the Text & Hero Area
        if arch == "neo_brutalist":
            # Giant Retro OS Desktop Window framing the cover
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, 940 if rtl else 100, 150, 860, 760))
        elif arch == "bauhaus_modern":
            # Giant Bauhaus Exhibition Poster Geometric Composition
            gx = 240 if rtl else 1320
            svg.append('<g id="bauhaus_cover_poster">')
            svg.append(f'<circle cx="{gx + 220}" cy="520" r="290" fill="{th["primary"]}" fill-opacity="0.88" stroke="{th["surface_border"]}" stroke-width="4" />')
            svg.append(f'<rect x="{gx - 60}" y="220" width="240" height="580" fill="{th["secondary"]}" stroke="{th["surface_border"]}" stroke-width="4" />')
            svg.append(f'<polygon points="{gx + 80},780 {gx + 460},780 {gx + 270},360" fill="{th["accent"]}" stroke="{th["surface_border"]}" stroke-width="4" />')
            svg.append('</g>')
        elif arch == "blueprint_schematic":
            # CAD Formal Engineering Title Block Stamp at bottom corner
            tb_x = 1220 if rtl else 120
            svg.append('<g id="cad_cover_title_block">')
            svg.append(f'<rect x="{tb_x}" y="760" width="580" height="160" fill="{th["surface"]}" stroke="{th["primary"]}" stroke-width="2.5" />')
            svg.append(f'<line x1="{tb_x}" y1="815" x2="{tb_x + 580}" y2="815" stroke="{th["primary"]}" stroke-width="1.5" />')
            svg.append(f'<line x1="{tb_x + 290}" y1="760" x2="{tb_x + 290}" y2="920" stroke="{th["primary"]}" stroke-width="1.5" />')
            svg.append(f'<text x="{tb_x + 145}" y="795" font-family="monospace" font-size="16" font-weight="700" fill="{th["primary"]}" text-anchor="middle">SCALE: 1:1 // ISO-9001</text>')
            svg.append(f'<text x="{tb_x + 435}" y="795" font-family="monospace" font-size="16" font-weight="700" fill="{th["secondary"]}" text-anchor="middle">SHEET: 01 OF DECK</text>')
            svg.append('</g>')

        # Style-aware Kicker + Title via Polymorphic Header logic scaled for Cover
        kw = max(260, len(kicker) * 18)
        kx = (x_pos - kw) if rtl else x_pos
        svg.extend(ArtStyleSkinEngine.render_card_container(renderer, kx, 200, kw, 56))
        svg.append(f'<text x="{kx + kw / 2}" y="236" font-family="{font}" font-size="20" font-weight="800" fill="{th["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')

        # Verbatim Title & Subtitle
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{x_pos}" y="355" font-family="{font}" font-size="60" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        if subtitle:
            sy = 440
            for s_line in subtitle.split("\n")[:4]:
                if s_line.strip():
                    svg.append(f'<text x="{x_pos}" y="{sy}" font-family="{font}" font-size="27" font-weight="600" fill="{th["primary"]}" text-anchor="{align}">{escape_xml(s_line.strip())}</text>')
                    sy += 44
        svg.append('</g>')

        if author:
            auth_w = max(320, len(author) * 19)
            auth_x = (x_pos - auth_w) if rtl else x_pos
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, auth_x, 600, auth_w, 72))
            svg.append(f'<text x="{auth_x + auth_w / 2}" y="645" font-family="{font}" font-size="22" font-weight="700" fill="{th["text_main"]}" text-anchor="middle">{escape_xml(author)}</text>')

        # Hero Image Frame with Style-Specific Silhouette
        if image_rel_path:
            center_hx = img_x + 375
            center_hy = 530
            svg.append('<g id="spin_hero_orbit">')
            svg.append(f'<circle cx="{center_hx}" cy="{center_hy}" r="395" fill="none" stroke="{th["primary"]}" stroke-width="2.2" stroke-opacity="0.4" stroke-dasharray="14 8" />')
            svg.append(f'<circle cx="{center_hx + 395}" cy="{center_hy}" r="8" fill="{th.get("accent", th["primary"])}" />')
            svg.append('</g>')

            svg.append('<g id="hero_image">')
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, img_x, 195, 750, 665))
            svg.append(f'<image href="{image_rel_path}" x="{img_x + 18}" y="222" width="714" height="620" preserveAspectRatio="xMidYMid slice" />')
            badge_cx = (img_x + 85) if rtl else (img_x + 665)
            svg.extend(ArtStyleSkinEngine.render_icon_badge(renderer, badge_cx, 275, 40, th["primary"], "award", icon_size=42))
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)
