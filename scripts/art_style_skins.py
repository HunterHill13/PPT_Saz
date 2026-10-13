#!/usr/bin/env python3
"""
PPT_Saz v6.0 — Multi-Dimensional Visual Rendering Engine (2.5D, 3D Volumetric, Photorealistic, & 2D Constructivist)

Eliminates flat 2D visual homogeneity across themes by introducing 4 fundamentally
distinct Dimensional Rendering Paradigms:
  1. 2.5D Isometric Projection (`cyber_hud`, `bauhaus_modern`, `isometric_25d`)
     - Tri-planar extruded 3D slabs (Top Face +22% lit, Right Thickness Wall -25% shaded,
       Bottom Thickness Wall -42% deep shadow, Cast Isometric Floor Shadow, 3D Isometric Cube Badges)
  2. 3D Volumetric & Claymorphism Studio (`apple_bento`, `paper_cutout`, `clay_3d`)
     - Multi-stop Phong specular linear & radial gradients (`<defs>`), inflated 3D soft-body capsules,
       3D glossy spheres with off-center studio softbox highlights, and deep ambient occlusion shadows
  3. Photorealistic & Material Texture Art (`royal_gold`, `warm_editorial`, `photorealistic_art`)
     - Procedural & high-res material substrates (Dark Italian Obsidian Marble with gold veins,
       Luxury Archival Linen with realistic botanical chiaroscuro lighting, Frosted Glassmorphism)
  4. 2D Technical & Constructivist (`blueprint_schematic`, `swiss_academic`, `neo_brutalist`)
     - Crisp architectural CAD blueprints, Swiss typographic grids, and Retro OS windows
"""

from __future__ import annotations

import base64
import hashlib
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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


def _hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    h = str(hex_str).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return (128, 128, 128)
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return (128, 128, 128)


def _rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return f"#{max(0, min(255, int(rgb[0]))):02X}{max(0, min(255, int(rgb[1]))):02X}{max(0, min(255, int(rgb[2]))):02X}"


def _shade_color(hex_str: str, factor: float) -> str:
    """
    Adjust color luminance for 2.5D and 3D lighting faces:
      factor > 0 -> blend toward white (+0.35 = +35% brighter top face)
      factor < 0 -> blend toward black (-0.35 = -35% darker side/bottom extrusion wall)
    """
    r, g, b = _hex_to_rgb(hex_str)
    if factor >= 0:
        r = int(r + (255 - r) * min(1.0, factor))
        g = int(g + (255 - g) * min(1.0, factor))
        b = int(b + (255 - b) * min(1.0, factor))
    else:
        f = max(0.0, 1.0 + factor)
        r = int(r * f)
        g = int(g * f)
        b = int(b * f)
    return _rgb_to_hex((r, g, b))


def _mix_colors(hex1: str, hex2: str, weight: float = 0.5) -> str:
    r1, g1, b1 = _hex_to_rgb(hex1)
    r2, g2, b2 = _hex_to_rgb(hex2)
    w = max(0.0, min(1.0, weight))
    return _rgb_to_hex((
        int(r1 * (1 - w) + r2 * w),
        int(g1 * (1 - w) + g2 * w),
        int(b1 * (1 - w) + b2 * w),
    ))


def _hex_points(cx: float, cy: float, r: float) -> str:
    pts = []
    for i in range(6):
        ang = math.radians(60 * i - 30)
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    return " ".join(pts)


def _iso_cube_faces(cx: float, cy: float, r: float) -> Tuple[str, str, str]:
    """
    Returns (top_face_pts, left_face_pts, right_face_pts) for a true 30-degree
    2.5D Isometric Cube centered at (cx, cy) with radius r.
    """
    dx = r * 0.866
    dy = r * 0.5
    top_v = f"{cx:.1f},{cy - r:.1f}"
    right_v = f"{cx + dx:.1f},{cy - dy:.1f}"
    center_v = f"{cx:.1f},{cy:.1f}"
    left_v = f"{cx - dx:.1f},{cy - dy:.1f}"
    bot_right_v = f"{cx + dx:.1f},{cy + dy:.1f}"
    bot_v = f"{cx:.1f},{cy + r:.1f}"
    bot_left_v = f"{cx - dx:.1f},{cy + dy:.1f}"

    top_face = f"{top_v} {right_v} {center_v} {left_v}"
    left_face = f"{left_v} {center_v} {bot_v} {bot_left_v}"
    right_face = f"{center_v} {right_v} {bot_right_v} {bot_v}"
    return top_face, left_face, right_face


def ensure_photorealistic_texture(theme_name: str, th: Dict[str, Any], arch: str) -> Optional[str]:
    """
    Procedurally generates high-resolution realistic material textures (Marble with gold veins,
    Warm Archival Linen with Chiaroscuro spotlight, or Studio Bokeh) using Pillow and caches
    them under scripts/assets/textures/ so DrawingML embeds real photographic material substrates.
    Returns an absolute POSIX path suitable for SVG <image href="..."/> or None if PIL unavailable.
    """
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        return None

    tex_dir = Path(__file__).resolve().parent.parent / "assets" / "textures"
    tex_dir.mkdir(parents=True, exist_ok=True)
    key_hash = hashlib.md5(f"{theme_name}_{arch}_{th.get('background')}_{th.get('primary')}".encode()).hexdigest()[:10]
    tex_path = tex_dir / f"material_{arch}_{key_hash}.png"

    if tex_path.exists() and tex_path.stat().st_size > 1000:
        data = tex_path.read_bytes()
        b64_str = base64.b64encode(data).decode("ascii")
        return f"data:image/png;base64,{b64_str}"

    w, h = 960, 540  # Half-HD high-speed procedural material canvas (scales cleanly to 1920x1080)
    bg_rgb = _hex_to_rgb(th.get("background", "#0F172A"))
    pri_rgb = _hex_to_rgb(th.get("primary", "#F59E0B"))
    sec_rgb = _hex_to_rgb(th.get("secondary", "#38BDF8"))
    surf_rgb = _hex_to_rgb(th.get("surface", "#1E293B"))

    img = Image.new("RGB", (w, h), bg_rgb)
    draw = ImageDraw.Draw(img, "RGBA")

    if arch == "royal_gold":
        # Realistic Italian Nero Marquina / Calacatta Marble with organic veins & spotlight
        for i in range(18):
            angle = (i * 37) % 360
            x0 = (i * 113) % w
            y0 = 0
            pts = []
            curr_x, curr_y = float(x0), float(y0)
            for step in range(28):
                pts.append((curr_x, curr_y))
                curr_x += math.sin(step * 0.45 + i) * 22 + (12 if i % 2 == 0 else -10)
                curr_y += h / 26.0
            vein_col = (*pri_rgb, 42 if i % 3 == 0 else 20)
            draw.line(pts, fill=vein_col, width=3 if i % 3 == 0 else 1)
            # Secondary micro-fissures
            sub_pts = [(px + math.cos(idx) * 8, py) for idx, (px, py) in enumerate(pts)]
            draw.line(sub_pts, fill=(*sec_rgb, 18), width=1)

        # Soft radial spotlight glow in upper center
        spot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(spot)
        for rad in range(360, 20, -20):
            alpha = int(18 * (1 - rad / 360.0))
            sdraw.ellipse((w // 2 - rad, h // 3 - rad, w // 2 + rad, h // 3 + rad), fill=(*pri_rgb, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), spot).convert("RGB")
        img = img.filter(ImageFilter.GaussianBlur(radius=1.2))

    elif arch == "warm_editorial":
        # Authentic Warm Archival Linen Canvas + Sunbeams & Dappled Botanical Leaf Shadows
        # Cross-hatch linen weave
        for x in range(0, w, 6):
            draw.line([(x, 0), (x, h)], fill=(*surf_rgb, 28), width=1)
        for y in range(0, h, 6):
            draw.line([(0, y), (w, y)], fill=(*pri_rgb, 14), width=1)
        # Warm window light beams from top-right
        beam = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(beam)
        bdraw.polygon([(w * 0.55, 0), (w, 0), (w * 0.25, h), (0, h * 0.7)], fill=(*pri_rgb, 24))
        bdraw.polygon([(w * 0.75, 0), (w, h * 0.2), (w * 0.55, h), (w * 0.35, h)], fill=(*sec_rgb, 20))
        beam = beam.filter(ImageFilter.GaussianBlur(radius=18))
        img = Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB")

    elif arch in ("apple_bento", "paper_cutout"):
        # 3D Studio Softbox Illumination Canvas with Rich Volumetric Color Meshes
        mesh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        mdraw = ImageDraw.Draw(mesh)
        mdraw.ellipse((-80, -60, 460, 380), fill=(*pri_rgb, 48))
        mdraw.ellipse((w - 440, h - 360, w + 80, h + 60), fill=(*sec_rgb, 45))
        mdraw.ellipse((w // 2 - 200, h // 2 - 160, w // 2 + 200, h // 2 + 160), fill=(*surf_rgb, 60))
        mesh = mesh.filter(ImageFilter.GaussianBlur(radius=32))
        img = Image.alpha_composite(img.convert("RGBA"), mesh).convert("RGB")

    # Save to in-memory bytes and encode as data:image/png;base64 URI for 100% self-contained SVG
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64_str}"


class ArtStyleSkinEngine:
    """
    Multi-Dimensional Visual Skin Engine (v6.0):
    Renders genuinely different dimensional worlds (2.5D Isometric, 3D Volumetric Claymorphism,
    Photorealistic Textured Materials, and 2D Technical/Constructivist) into Native DrawingML.
    """

    @staticmethod
    def get_dimensional_paradigm(arch: str) -> str:
        """Maps each archetype to one of the 4 core Dimensional Rendering Paradigms."""
        if arch in ("cyber_hud", "bauhaus_modern", "isometric_25d"):
            return "2.5d_isometric"
        if arch in ("apple_bento", "paper_cutout", "clay_3d"):
            return "3d_volumetric"
        if arch in ("royal_gold", "warm_editorial", "photorealistic_art"):
            return "photorealistic_material"
        return "2d_technical"  # swiss_academic, blueprint_schematic, neo_brutalist

    # ==========================================================================
    # 0. LIGHTING, GRADIENTS & DROP-SHADOW DEFINITIONS (`render_style_defs`)
    # ==========================================================================
    @staticmethod
    def render_style_defs(renderer) -> str:
        """
        Generates SVG <defs> containing native-compatible <linearGradient>,
        <radialGradient>, and <filter> (feDropShadow / feGaussianBlur) definitions.
        """
        th = renderer.theme
        primary = th["primary"]
        secondary = th["secondary"]
        accent = th.get("accent", primary)
        surface = th["surface"]
        badge_bg = th["badge_bg"]
        is_dark = renderer.is_dark

        # 3D & 2.5D Shaded stops
        surf_top_lit = _shade_color(surface, 0.24 if is_dark else 0.08)
        surf_mid = surface
        surf_bot_shade = _shade_color(surface, -0.25 if is_dark else -0.07)

        pri_lit = _shade_color(primary, 0.42)
        pri_mid = primary
        pri_dark = _shade_color(primary, -0.38)

        sec_lit = _shade_color(secondary, 0.42)
        sec_mid = secondary
        sec_dark = _shade_color(secondary, -0.38)

        acc_lit = _shade_color(accent, 0.42)
        acc_mid = accent
        acc_dark = _shade_color(accent, -0.38)

        gold_1 = _shade_color(primary, 0.45)
        gold_2 = primary
        gold_3 = _shade_color(primary, -0.35)

        shadow_alpha = "0.42" if is_dark else "0.18"
        deep_shadow_alpha = "0.55" if is_dark else "0.26"

        return f"""<defs>
  <!-- 3D Volumetric Clay Card Surface Gradient -->
  <linearGradient id="grad_3d_surface" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0%" stop-color="{surf_top_lit}" />
    <stop offset="55%" stop-color="{surf_mid}" />
    <stop offset="100%" stop-color="{surf_bot_shade}" />
  </linearGradient>

  <!-- 2.5D Isometric Top Face Lit Gradient -->
  <linearGradient id="grad_iso_top" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{_shade_color(surface, 0.28 if is_dark else 0.06)}" />
    <stop offset="100%" stop-color="{_shade_color(surface, -0.08 if is_dark else -0.04)}" />
  </linearGradient>

  <!-- Photorealistic Frosted Glassmorphism Gradient -->
  <linearGradient id="grad_frosted_glass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{_shade_color(surface, 0.30)}" stop-opacity="0.92" />
    <stop offset="50%" stop-color="{surface}" stop-opacity="0.82" />
    <stop offset="100%" stop-color="{_shade_color(surface, -0.20)}" stop-opacity="0.90" />
  </linearGradient>

  <!-- Metallic Gold / Specular Rim Gradient -->
  <linearGradient id="grad_metallic_rim" x1="0" y1="0" x2="1" y2="0.8">
    <stop offset="0%" stop-color="{gold_1}" />
    <stop offset="50%" stop-color="{gold_2}" />
    <stop offset="100%" stop-color="{gold_3}" />
  </linearGradient>

  <!-- 3D Primary Volumetric Pill / Cone Gradient -->
  <linearGradient id="grad_3d_primary" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{pri_lit}" />
    <stop offset="55%" stop-color="{pri_mid}" />
    <stop offset="100%" stop-color="{pri_dark}" />
  </linearGradient>

  <!-- 3D Secondary Volumetric Gradient -->
  <linearGradient id="grad_3d_secondary" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{sec_lit}" />
    <stop offset="55%" stop-color="{sec_mid}" />
    <stop offset="100%" stop-color="{sec_dark}" />
  </linearGradient>

  <!-- 3D Accent Volumetric Gradient -->
  <linearGradient id="grad_3d_accent" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{acc_lit}" />
    <stop offset="55%" stop-color="{acc_mid}" />
    <stop offset="100%" stop-color="{acc_dark}" />
  </linearGradient>

  <!-- 3D Specular Sphere Radial Gradients (Studio Softbox Focus at 0.35, 0.35) -->
  <radialGradient id="orb_3d_primary" cx="0.5" cy="0.5" r="0.5" fx="0.35" fy="0.35">
    <stop offset="0%" stop-color="#FFFFFF" />
    <stop offset="28%" stop-color="{pri_lit}" />
    <stop offset="72%" stop-color="{pri_mid}" />
    <stop offset="100%" stop-color="{pri_dark}" />
  </radialGradient>

  <radialGradient id="orb_3d_secondary" cx="0.5" cy="0.5" r="0.5" fx="0.35" fy="0.35">
    <stop offset="0%" stop-color="#FFFFFF" />
    <stop offset="28%" stop-color="{sec_lit}" />
    <stop offset="72%" stop-color="{sec_mid}" />
    <stop offset="100%" stop-color="{sec_dark}" />
  </radialGradient>

  <radialGradient id="orb_3d_accent" cx="0.5" cy="0.5" r="0.5" fx="0.35" fy="0.35">
    <stop offset="0%" stop-color="#FFFFFF" />
    <stop offset="28%" stop-color="{acc_lit}" />
    <stop offset="72%" stop-color="{acc_mid}" />
    <stop offset="100%" stop-color="{acc_dark}" />
  </radialGradient>

  <radialGradient id="orb_3d_badge" cx="0.5" cy="0.5" r="0.5" fx="0.35" fy="0.35">
    <stop offset="0%" stop-color="{_shade_color(badge_bg, 0.45)}" />
    <stop offset="65%" stop-color="{badge_bg}" />
    <stop offset="100%" stop-color="{_shade_color(badge_bg, -0.35)}" />
  </radialGradient>

  <!-- Native DrawingML Outer Drop Shadows -->
  <filter id="shadow_3d_soft" primitiveUnits="userSpaceOnUse">
    <feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000000" flood-opacity="{shadow_alpha}" />
  </filter>

  <filter id="shadow_3d_deep" primitiveUnits="userSpaceOnUse">
    <feDropShadow dx="6" dy="18" stdDeviation="15" flood-color="#000000" flood-opacity="{deep_shadow_alpha}" />
  </filter>

  <filter id="shadow_cutout_ elevation" primitiveUnits="userSpaceOnUse">
    <feDropShadow dx="8" dy="10" stdDeviation="6" flood-color="#000000" flood-opacity="0.32" />
  </filter>
</defs>"""

    # ==========================================================================
    # 1. MULTI-DIMENSIONAL CONTAINER SILHOUETTES (`render_card_container`)
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
        is_dark = renderer.is_dark
        out: List[str] = []

        if arch == "cyber_hud":
            # ==================================================================
            # PARADIGM 1A: 2.5D ISOMETRIC EXTRUDED SCI-FI SLAB (3 Shaded Planes)
            # ==================================================================
            dx = 16.0  # Isometric 3D extrusion X vector
            dy = 11.0  # Isometric 3D extrusion Y vector
            cut = min(24.0, h * 0.15, w * 0.10)

            # 1) Cast Floor Drop-Shadow Polygon on Isometric Ground Plane
            sh_pts = (
                f"{x + cut + dx + 8},{y + dy + 10} "
                f"{x + w + dx + 8},{y + dy + 10} "
                f"{x + w + dx + 8},{y + h - cut + dy + 10} "
                f"{x + w - cut + dx + 8},{y + h + dy + 10} "
                f"{x + dx + 8},{y + h + dy + 10} "
                f"{x + dx + 8},{y + cut + dy + 10}"
            )
            out.append(f'<polygon points="{sh_pts}" fill="#000000" fill-opacity="0.38" />')

            # 2) Right Extrusion 3D Thickness Wall (Medium Shaded Plane)
            right_wall_col = _shade_color(surface, -0.25 if is_dark else -0.15)
            rw_pts = (
                f"{x + w},{y} "
                f"{x + w + dx},{y + dy} "
                f"{x + w + dx},{y + h - cut + dy} "
                f"{x + w},{y + h - cut}"
            )
            out.append(f'<polygon points="{rw_pts}" fill="{right_wall_col}" stroke="{border}" stroke-width="1.5" />')

            # 3) Bottom-Right Chamfer Extrusion Wall (Intermediate Plane)
            chamf_wall_col = _shade_color(primary, -0.35)
            cw_pts = (
                f"{x + w},{y + h - cut} "
                f"{x + w + dx},{y + h - cut + dy} "
                f"{x + w - cut + dx},{y + h + dy} "
                f"{x + w - cut},{y + h}"
            )
            out.append(f'<polygon points="{cw_pts}" fill="{chamf_wall_col}" stroke="{primary}" stroke-width="1.5" />')

            # 4) Bottom Extrusion 3D Thickness Wall (Deepest Shaded Plane)
            bot_wall_col = _shade_color(surface, -0.45 if is_dark else -0.28)
            bw_pts = (
                f"{x},{y + h} "
                f"{x + w - cut},{y + h} "
                f"{x + w - cut + dx},{y + h + dy} "
                f"{x + dx},{y + h + dy}"
            )
            out.append(f'<polygon points="{bw_pts}" fill="{bot_wall_col}" stroke="{border}" stroke-width="1.5" />')

            # 5) Top Lit Isometric Platform Face
            top_pts = (
                f"{x + cut},{y} "
                f"{x + w},{y} "
                f"{x + w},{y + h - cut} "
                f"{x + w - cut},{y + h} "
                f"{x},{y + h} "
                f"{x},{y + cut}"
            )
            out.append(f'<polygon points="{top_pts}" fill="url(#grad_iso_top)" stroke="{primary}" stroke-width="{stroke_width}" />')

            # 6) 2.5D Extruded Top Energy Bar
            if top_accent:
                tab_w = min(150.0, w * 0.38)
                out.append(f'<polygon points="{x + cut},{y} {x + cut + tab_w},{y} {x + cut + tab_w - 8},{y + 8} {x + cut - 8},{y + 8}" fill="{primary}" />')
            # Isometric depth tick marks on right wall
            for t_i in range(3):
                ty = y + 24 + t_i * 18
                if ty + dy < y + h - cut:
                    out.append(f'<line x1="{x + w + 3}" y1="{ty}" x2="{x + w + dx - 3}" y2="{ty + dy - 2}" stroke="{primary}" stroke-width="2" />')

        elif arch == "bauhaus_modern":
            # ==================================================================
            # PARADIGM 1B: 2.5D ARCHITECTURAL AXONOMETRIC MONOLITH BLOCK
            # ==================================================================
            dx = 18.0
            dy = 14.0
            border_col = th["surface_border"]

            # Cast Isometric Ground Shadow
            out.append(f'<polygon points="{x + dx + 8},{y + dy + 8} {x + w + dx + 8},{y + dy + 8} {x + w + dx + 8},{y + h + dy + 8} {x + dx + 8},{y + h + dy + 8}" fill="#000000" fill-opacity="0.22" />')
            # Right 3D Extruded Side Wall (Colored in Secondary Constructivist Tone)
            out.append(f'<polygon points="{x + w},{y} {x + w + dx},{y + dy} {x + w + dx},{y + h + dy} {x + w},{y + h}" fill="{secondary}" stroke="{border_col}" stroke-width="3" />')
            # Bottom 3D Extruded Wall (Colored in Primary Darkened Tone)
            out.append(f'<polygon points="{x},{y + h} {x + w},{y + h} {x + w + dx},{y + h + dy} {x + dx},{y + h + dy}" fill="{_shade_color(primary, -0.25)}" stroke="{border_col}" stroke-width="3" />')
            # Top Face Lit Constructivist Canvas
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border_col}" stroke-width="3.5" />')
            # 2.5D Stepped Corner Color-Block Pedestal
            seg1 = min(120.0, w * 0.3)
            seg2 = min(70.0, w * 0.18)
            out.append(f'<rect x="{x}" y="{y}" width="{seg1}" height="12" fill="{primary}" stroke="{border_col}" stroke-width="2" />')
            out.append(f'<rect x="{x + seg1}" y="{y}" width="{seg2}" height="12" fill="{accent}" stroke="{border_col}" stroke-width="2" />')

        elif arch == "apple_bento":
            # ==================================================================
            # PARADIGM 2A: 3D VOLUMETRIC CLAYMORPHISM & GLOSSY SOFT-BODY STUDIO
            # ==================================================================
            # 1) Deep Soft 3D Ambient Occlusion Base Cushion (Extruded Lower Rim)
            rim_col = _shade_color(surface, -0.28 if is_dark else -0.12)
            out.append(f'<rect x="{x}" y="{y + 10}" width="{w}" height="{h}" rx="40" fill="{rim_col}" filter="url(#shadow_3d_soft)" />')
            # 2) Inflated 3D Volumetric Body with Multi-Stop Specular Gradient
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h - 4}" rx="40" fill="url(#grad_3d_surface)" stroke="{_shade_color(surface, 0.38)}" stroke-width="2.5" />')
            # 3) Top Curved Studio Softbox Specular Highlight Pill (Creates unmistakable 3D Clay/Glossy feel)
            hl_w = max(40.0, w - 64)
            out.append(f'<rect x="{x + 32}" y="{y + 6}" width="{hl_w}" height="12" rx="6" fill="#FFFFFF" fill-opacity="{0.22 if is_dark else 0.65}" />')
            # 4) 3D Floating Corner Sphere Stud
            out.append(f'<circle cx="{x + w - 28}" cy="{y + 26}" r="8" fill="url(#orb_3d_primary)" />')

        elif arch == "paper_cutout":
            # ==================================================================
            # PARADIGM 2B: 3D TACTILE MULTI-LAYERED DIORAMA WITH REAL DROP SHADOWS
            # ==================================================================
            # Layer 1: Deep tilted colored paper backing with real Gaussian shadow
            back_pts = f"{x - 6},{y + 10} {x + w + 10},{y + 4} {x + w + 5},{y + h + 12} {x + 6},{y + h + 8}"
            out.append(f'<polygon points="{back_pts}" fill="url(#grad_3d_secondary)" filter="url(#shadow_cutout_elevation)" />')
            # Layer 2: Mid-sheet accent paper
            mid_pts = f"{x + 4},{y - 4} {x + w + 4},{y + 8} {x + w - 6},{y + h + 4} {x - 4},{y + h - 4}"
            out.append(f'<polygon points="{mid_pts}" fill="{primary}" fill-opacity="0.85" />')
            # Layer 3: Main tactile top cardstock with soft 3D shadow
            front_pts = f"{x + 2},{y} {x + w},{y + 2} {x + w - 2},{y + h} {x},{y + h - 2}"
            out.append(f'<polygon points="{front_pts}" fill="url(#grad_3d_surface)" stroke="{border}" stroke-width="2.5" filter="url(#shadow_3d_soft)" />')
            # 3D Spherical Push-Pin / Tack holding the top center of the cutout card
            pin_cx = x + w / 2
            pin_cy = y + 6
            out.append(f'<ellipse cx="{pin_cx + 4}" cy="{pin_cy + 6}" rx="12" ry="8" fill="#000000" fill-opacity="0.3" />')
            out.append(f'<circle cx="{pin_cx}" cy="{pin_cy}" r="12" fill="url(#orb_3d_accent)" stroke="#FFFFFF" stroke-width="1.5" />')

        elif arch == "royal_gold":
            # ==================================================================
            # PARADIGM 3A: PHOTOREALISTIC LUXURY MARBLE & 3D BEVELED GOLD BULLION
            # ==================================================================
            cut = min(22.0, h * 0.14, w * 0.1)
            # Outer 3D Gold Bevel Frame
            pts_outer = (
                f"{x + cut},{y} {x + w - cut},{y} {x + w},{y + cut} {x + w},{y + h - cut} "
                f"{x + w - cut},{y + h} {x + cut},{y + h} {x},{y + h - cut} {x},{y + cut}"
            )
            out.append(f'<polygon points="{pts_outer}" fill="url(#grad_metallic_rim)" filter="url(#shadow_3d_deep)" />')
            # Inner Frosted Obsidian / Ivory Marble Slab (inset by 4px to expose 3D metallic bevel)
            b = 4.0
            pts_slab = (
                f"{x + cut + 2},{y + b} {x + w - cut - 2},{y + b} {x + w - b},{y + cut + 2} {x + w - b},{y + h - cut - 2} "
                f"{x + w - cut - 2},{y + h - b} {x + cut + 2},{y + h - b} {x + b},{y + h - cut - 2} {x + b},{y + cut + 2}"
            )
            out.append(f'<polygon points="{pts_slab}" fill="url(#grad_frosted_glass)" stroke="{primary}" stroke-width="1" />')
            # Subtle realistic marble vein inside card
            out.append(f'<path d="M {x + 20},{y + h - 18} Q {x + w * 0.4},{y + h * 0.6} {x + w - 24},{y + 20}" fill="none" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.16" />')
            # 3D Faceted Gold Jewel Studs
            for d_x, d_y in ((x + w / 2, y + 2), (x + w / 2, y + h - 2)):
                out.append(f'<polygon points="{d_x},{d_y - 7} {d_x + 7},{d_y} {d_x},{d_y + 7} {d_x - 7},{d_y}" fill="url(#orb_3d_primary)" />')

        elif arch == "warm_editorial":
            # ==================================================================
            # PARADIGM 3B: PHOTOREALISTIC ARCHIVAL PAPER & CHIAROSCURO ARCH
            # ==================================================================
            arch_r = min(38.0, w * 0.15, h * 0.2)
            path_d = (
                f"M {x},{y + arch_r} "
                f"A {arch_r},{arch_r} 0 0,1 {x + arch_r},{y} "
                f"L {x + w - arch_r},{y} "
                f"A {arch_r},{arch_r} 0 0,1 {x + w},{y + arch_r} "
                f"L {x + w},{y + h - 10} "
                f"Q {x + w},{y + h} {x + w - 10},{y + h} "
                f"L {x + 10},{y + h} "
                f"Q {x},{y + h} {x},{y + h - 10} Z"
            )
            # Soft realistic gallery wall cast shadow + warm gradient paper card
            out.append(f'<path d="{path_d}" fill="url(#grad_frosted_glass)" stroke="{border}" stroke-width="2" filter="url(#shadow_3d_soft)" />')
            # Inner gold/terracotta double-embossed frame line
            out.append(f'<line x1="{x + 28}" y1="{y + 12}" x2="{x + w - 28}" y2="{y + 12}" stroke="{primary}" stroke-width="2.5" />')
            out.append(f'<line x1="{x + 42}" y1="{y + 18}" x2="{x + w - 42}" y2="{y + 18}" stroke="{secondary}" stroke-width="1" />')
            # 3D Wax Seal / Medallion stud at top center
            out.append(f'<circle cx="{x + w / 2}" cy="{y + 12}" r="7" fill="url(#orb_3d_primary)" />')

        elif arch == "neo_brutalist":
            # ==================================================================
            # PARADIGM 4A: 2D RETRO OS WINDOW WITH HARDEXTRUDED BLOCK SHADOW
            # ==================================================================
            shadow_col = "#000000" if not is_dark else primary
            border_col = "#000000" if not is_dark else "#FFFFFF"
            bar_h = 22
            out.append(f'<rect x="{x + 10}" y="{y + 10}" width="{w}" height="{h}" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border_col}" stroke-width="4" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{bar_h}" rx="0" fill="{primary}" stroke="{border_col}" stroke-width="3.5" />')
            for b_idx, b_col in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
                bx = x + 16 + (b_idx * 18)
                by = y + 11
                out.append(f'<circle cx="{bx}" cy="{by}" r="5.5" fill="{b_col}" stroke="#000000" stroke-width="1.8" />')
            out.append(f'<line x1="{x + w - 28}" y1="{y + 11}" x2="{x + w - 12}" y2="{y + 11}" stroke="#000000" stroke-width="2.5" />')

        elif arch == "swiss_academic":
            # ==================================================================
            # PARADIGM 4B: 2D INTERNATIONAL SWISS TYPOGRAPHIC GRID
            # ==================================================================
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{border}" stroke-width="1.5" />')
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="0" fill="{primary}" />')
            out.append(f'<rect x="{x}" y="{y}" width="80" height="8" rx="0" fill="{secondary}" />')
            out.append(f'<line x1="{x}" y1="{y + h - 10}" x2="{x + w}" y2="{y + h - 10}" stroke="{border}" stroke-width="1" />')
            for cx_t, cy_t in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
                out.append(f'<line x1="{cx_t - 7}" y1="{cy_t}" x2="{cx_t + 7}" y2="{cy_t}" stroke="{secondary}" stroke-width="1.8" />')
                out.append(f'<line x1="{cx_t}" y1="{cy_t - 7}" x2="{cx_t}" y2="{cy_t + 7}" stroke="{secondary}" stroke-width="1.8" />')

        else:  # blueprint_schematic
            # ==================================================================
            # PARADIGM 4C: 2D ARCHITECTURAL CAD BLUEPRINT SCHEMATIC
            # ==================================================================
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{surface}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<rect x="{x + 5}" y="{y + 5}" width="{w - 10}" height="{h - 10}" rx="0" fill="none" stroke="{secondary}" stroke-width="0.8" stroke-dasharray="6 4" />')
            ext = 14
            out.append(f'<line x1="{x - ext}" y1="{y}" x2="{x + w + ext}" y2="{y}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x - ext}" y1="{y + h}" x2="{x + w + ext}" y2="{y + h}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x}" y1="{y - ext}" x2="{x}" y2="{y + h + ext}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            out.append(f'<line x1="{x + w}" y1="{y - ext}" x2="{x + w}" y2="{y + h + ext}" stroke="{primary}" stroke-width="1.2" stroke-opacity="0.65" />')
            stamp_w = min(115.0, w * 0.3)
            out.append(f'<rect x="{x}" y="{y}" width="{stamp_w}" height="16" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="1.2" />')
            out.append(f'<text x="{x + stamp_w / 2}" y="{y + 12}" font-family="monospace" font-size="10" font-weight="700" fill="{primary}" text-anchor="middle">CAD // {int(w)}x{int(h)}</text>')

        return out

    # ==========================================================================
    # 2. MULTI-DIMENSIONAL ICON BADGES (`render_icon_badge`)
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
        sz = icon_size or int(r * 1.05)
        out: List[str] = []

        if arch in ("cyber_hud", "bauhaus_modern"):
            # 2.5D Isometric 3-Face Extruded Cube Pedestal Badge!
            top_f, left_f, right_f = _iso_cube_faces(cx, cy, r * 1.18)
            # Cast floor shadow under isometric cube
            out.append(f'<ellipse cx="{cx + 4}" cy="{cy + r * 1.15}" rx="{r * 0.95}" ry="{r * 0.45}" fill="#000000" fill-opacity="0.35" />')
            out.append(f'<polygon points="{left_f}" fill="{_shade_color(color, -0.22)}" stroke="{color}" stroke-width="1.5" />')
            out.append(f'<polygon points="{right_f}" fill="{_shade_color(color, -0.45)}" stroke="{color}" stroke-width="1.5" />')
            out.append(f'<polygon points="{top_f}" fill="{_shade_color(badge_bg, 0.25)}" stroke="{color}" stroke-width="2" />')
            # Inner glowing core on cube center
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62}" fill="{badge_bg}" fill-opacity="0.88" stroke="{color}" stroke-width="1.5" />')

        elif arch in ("apple_bento", "paper_cutout"):
            # 3D Volumetric Glossy Sphere / Inflated Clay Orb with Specular Highlight
            orb_grad = "orb_3d_primary" if color == th["primary"] else ("orb_3d_secondary" if color == th["secondary"] else "orb_3d_accent")
            out.append(f'<ellipse cx="{cx + 3}" cy="{cy + r * 0.85}" rx="{r * 0.85}" ry="{r * 0.35}" fill="#000000" fill-opacity="0.28" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 3}" fill="url(#{orb_grad})" filter="url(#shadow_3d_soft)" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.78}" fill="url(#orb_3d_badge)" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.5" />')
            # Studio specular reflection dot
            out.append(f'<ellipse cx="{cx - r * 0.28}" cy="{cy - r * 0.32}" rx="{r * 0.25}" ry="{r * 0.14}" fill="#FFFFFF" fill-opacity="0.55" />')

        elif arch in ("royal_gold", "warm_editorial"):
            # Photorealistic 3D Beveled Gold / Bronze Medallion Seal
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 5}" fill="url(#grad_metallic_rim)" filter="url(#shadow_3d_soft)" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="{badge_bg}" stroke="{color}" stroke-width="1.8" />')
            out.append(f'<circle cx="{cx - r * 0.3}" cy="{cy - r * 0.3}" r="{r * 0.18}" fill="#FFFFFF" fill-opacity="0.35" />')

        elif arch == "neo_brutalist":
            shadow_col = "#000000" if not renderer.is_dark else color
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            out.append(f'<rect x="{cx - r + 5}" y="{cy - r + 5}" width="{r * 2}" height="{r * 2}" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{border_col}" stroke-width="3" />')

        elif arch == "swiss_academic":
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{color}" stroke-width="2" />')
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="6" rx="0" fill="{color}" />')

        else:  # blueprint_schematic
            out.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="0" fill="{badge_bg}" stroke="{color}" stroke-width="1.8" />')
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.85}" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="4 3" />')
            out.append(f'<line x1="{cx - r - 7}" y1="{cy}" x2="{cx + r + 7}" y2="{cy}" stroke="{color}" stroke-width="1.2" stroke-opacity="0.6" />')
            out.append(f'<line x1="{cx}" y1="{cy - r - 7}" x2="{cx}" y2="{cy + r + 7}" stroke="{color}" stroke-width="1.2" stroke-opacity="0.6" />')

        out.append(get_icon_svg_content(icon_key, cx - sz / 2, cy - sz / 2, size=sz, stroke_color=color))
        return out

    # ==========================================================================
    # 3. MULTI-DIMENSIONAL SLIDE HEADERS (`render_style_header`)
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

        if arch in ("cyber_hud", "bauhaus_modern"):
            # 2.5D Extruded Isometric Header Bar with Side Depth Wall
            kw = 310
            kx = (title_x - kw) if rtl else title_x
            ky = 58
            kh = 42
            dx, dy = 10, 7
            out.append(f'<polygon points="{kx + kw},{ky} {kx + kw + dx},{ky + dy} {kx + kw + dx},{ky + kh + dy} {kx + kw},{ky + kh}" fill="{_shade_color(primary, -0.35)}" />')
            out.append(f'<polygon points="{kx},{ky + kh} {kx + kw},{ky + kh} {kx + kw + dx},{ky + kh + dy} {kx + dx},{ky + kh + dy}" fill="{_shade_color(secondary, -0.45)}" />')
            out.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" fill="url(#grad_3d_primary)" stroke="{primary}" stroke-width="2" />')
            out.append(f'<text x="{kx + kw / 2}" y="86" font-family="{font}" font-size="16" font-weight="800" fill="#FFFFFF" text-anchor="middle">⬡ {escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="900" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            line_x1 = 1800 if rtl else 120
            line_x2 = 1050 if rtl else 870
            out.append(f'<line x1="{line_x1}" y1="180" x2="{line_x2}" y2="180" stroke="{primary}" stroke-width="3" />')

        elif arch in ("apple_bento", "paper_cutout"):
            # 3D Volumetric Inflated Capsule Pill Header with Studio Highlight & Orb
            kw = 300
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="60" width="{kw}" height="44" rx="22" fill="url(#grad_3d_primary)" filter="url(#shadow_3d_soft)" />')
            out.append(f'<rect x="{kx + 18}" y="65" width="{kw - 36}" height="8" rx="4" fill="#FFFFFF" fill-opacity="0.35" />')
            orb_x = (kx + kw - 24) if rtl else (kx + 24)
            out.append(f'<circle cx="{orb_x}" cy="82" r="10" fill="url(#orb_3d_accent)" />')
            out.append(f'<text x="{kx + kw / 2}" y="89" font-family="{font}" font-size="16" font-weight="800" fill="#FFFFFF" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="162" font-family="{font}" font-size="45" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')

        elif arch == "royal_gold":
            # Photorealistic Metallic Gold Bullion Crest Header
            cx = 960
            out.append(f'<polygon points="{cx - 180},60 {cx + 180},60 {cx + 200},82 {cx + 180},104 {cx - 180},104 {cx - 200},82" fill="url(#grad_metallic_rim)" filter="url(#shadow_3d_soft)" />')
            out.append(f'<polygon points="{cx - 176},64 {cx + 176},64 {cx + 194},82 {cx + 176},100 {cx - 176},100 {cx - 194},82" fill="{th["badge_bg"]}" />')
            out.append(f'<line x1="{cx - 380}" y1="82" x2="{cx - 210}" y2="82" stroke="{primary}" stroke-width="2.5" />')
            out.append(f'<line x1="{cx + 210}" y1="82" x2="{cx + 380}" y2="82" stroke="{primary}" stroke-width="2.5" />')
            out.append(f'<text x="{cx}" y="88" font-family="{font}" font-size="16" font-weight="800" fill="{primary}" text-anchor="middle">◆ {escape_xml(kicker)} ◆</text>')
            out.append(f'<text x="{cx}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="middle">{escape_xml(title)}</text>')
            out.append(f'<line x1="{cx - 280}" y1="178" x2="{cx + 280}" y2="178" stroke="{primary}" stroke-width="2" />')

        elif arch == "warm_editorial":
            # Editorial Chiaroscuro Masthead with 3D Wax Medallion
            out.append(f'<line x1="120" y1="62" x2="1800" y2="62" stroke="{primary}" stroke-width="3" />')
            out.append(f'<line x1="120" y1="68" x2="1800" y2="68" stroke="{secondary}" stroke-width="1" />')
            out.append(f'<text x="{title_x}" y="98" font-family="{font}" font-size="17" font-weight="700" fill="{primary}" text-anchor="{align}">✦ {escape_xml(kicker)} — PHOTOREALISTIC EDITORIAL</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="700" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="180" x2="1800" y2="180" stroke="{th["surface_border"]}" stroke-width="1.5" />')

        elif arch == "neo_brutalist":
            shadow_col = "#000000" if not renderer.is_dark else secondary
            border_col = "#000000" if not renderer.is_dark else "#FFFFFF"
            kw = 280
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx + 6}" y="66" width="{kw}" height="40" rx="0" fill="{shadow_col}" />')
            out.append(f'<rect x="{kx}" y="60" width="{kw}" height="40" rx="0" fill="{primary}" stroke="{border_col}" stroke-width="3.5" />')
            k_txt_col = "#000000" if not renderer.is_dark else "#111111"
            out.append(f'<text x="{kx + kw / 2}" y="87" font-family="{font}" font-size="17" font-weight="900" fill="{k_txt_col}" text-anchor="middle">★ {escape_xml(kicker)}</text>')
            hl_w = min(720, max(320, len(title) * 22))
            hl_x = (title_x - hl_w) if rtl else title_x
            out.append(f'<rect x="{hl_x}" y="148" width="{hl_w}" height="18" fill="{secondary}" fill-opacity="0.35" />')
            out.append(f'<text x="{title_x}" y="160" font-family="{font}" font-size="44" font-weight="900" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')

        elif arch == "swiss_academic":
            kw = 260
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="64" width="{kw}" height="36" rx="0" fill="{primary}" />')
            out.append(f'<text x="{kx + kw / 2}" y="88" font-family="{font}" font-size="16" font-weight="700" fill="{th["background"]}" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="44" font-weight="800" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="182" x2="1800" y2="182" stroke="{th["surface_border"]}" stroke-width="2" />')
            out.append(f'<rect x="{(title_x - 140) if rtl else title_x}" y="179" width="140" height="6" fill="{secondary}" />')

        else:  # blueprint_schematic
            kw = 310
            kx = (title_x - kw) if rtl else title_x
            out.append(f'<rect x="{kx}" y="60" width="{kw}" height="40" rx="0" fill="{th["badge_bg"]}" stroke="{primary}" stroke-width="2" />')
            out.append(f'<line x1="{kx + 90}" y1="60" x2="{kx + 90}" y2="100" stroke="{primary}" stroke-width="1.5" />')
            out.append(f'<text x="{kx + 45}" y="85" font-family="monospace" font-size="14" font-weight="700" fill="{secondary}" text-anchor="middle">DWG//01</text>')
            out.append(f'<text x="{kx + 200}" y="86" font-family="{font}" font-size="15" font-weight="700" fill="{primary}" text-anchor="middle">{escape_xml(kicker)}</text>')
            out.append(f'<text x="{title_x}" y="158" font-family="{font}" font-size="43" font-weight="700" fill="{th["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
            out.append(f'<line x1="120" y1="180" x2="1800" y2="180" stroke="{primary}" stroke-width="1.5" stroke-dasharray="10 5" />')

        out.append('</g>')
        return out

    # ==========================================================================
    # 4. MULTI-DIMENSIONAL AMBIENT CANVAS (`render_ambient_canvas`)
    # ==========================================================================
    @staticmethod
    def render_ambient_canvas(renderer, is_rtl: bool, slide_idx: int = 1) -> List[str]:
        """
        Renders the ambient world for each Dimensional Paradigm:
        - 2.5D Isometric: 30-degree Axonometric Floor Grid + Floating 3D Isometric Cubes
        - 3D Volumetric: Floating 3D Specular Spheres & Glossy Studio Orbs
        - Photorealistic: Embedded High-Res Material Texture (Marble / Linen) + Spotlights
        - 2D Technical: CAD Blueprint Grid / Swiss Grid / Brutalist Matrix
        """
        arch = renderer.archetype
        th = renderer.theme
        primary = th["primary"]
        secondary = th["secondary"]
        accent = th.get("accent", primary)
        border = th["surface_border"]
        extra: List[str] = []

        # 1) Optional High-Resolution Procedural Material Substrate for Photorealistic & 3D Studio themes
        if arch in ("royal_gold", "warm_editorial"):
            tex_posix = ensure_photorealistic_texture(th.get("name", arch), th, arch)
            if tex_posix:
                extra.append(f'<image href="{tex_posix}" x="0" y="0" width="1920" height="1080" preserveAspectRatio="xMidYMid slice" opacity="0.65" />')

        if arch in ("cyber_hud", "bauhaus_modern"):
            # ==================================================================
            # 2.5D ISOMETRIC WORLD: 30° Axonometric Perspective Floor + 3D Cubes
            # ==================================================================
            iso_lines = ['<g id="isometric_25d_world_grid">']
            # Isometric diagonal floor grid lines in lower & side canvas
            for i in range(-4, 16):
                x_start = i * 180
                iso_lines.append(f'<line x1="{x_start}" y1="680" x2="{x_start + 680}" y2="1080" stroke="{primary}" stroke-width="1" stroke-opacity="0.16" />')
                iso_lines.append(f'<line x1="{x_start + 680}" y1="680" x2="{x_start}" y2="1080" stroke="{secondary}" stroke-width="1" stroke-opacity="0.14" />')

            # Floating 2.5D Isometric Cubes in corners
            cube_positions = [
                (160 if is_rtl else 1760, 150, 42, primary),
                (105 if is_rtl else 1815, 225, 28, secondary),
                (1800 if is_rtl else 120, 935, 58, accent),
                (1710 if is_rtl else 210, 985, 34, primary),
            ]
            for cx, cy, cr, ccol in cube_positions:
                tf, lf, rf = _iso_cube_faces(cx, cy, cr)
                iso_lines.append(f'<polygon points="{lf}" fill="{_shade_color(ccol, -0.20)}" fill-opacity="0.75" stroke="{ccol}" stroke-width="1.2" />')
                iso_lines.append(f'<polygon points="{rf}" fill="{_shade_color(ccol, -0.45)}" fill-opacity="0.80" stroke="{ccol}" stroke-width="1.2" />')
                iso_lines.append(f'<polygon points="{tf}" fill="{_shade_color(ccol, 0.35)}" fill-opacity="0.85" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.5" />')
            iso_lines.append('</g>')
            extra.append("\n".join(iso_lines))

            # Spinning Isometric Gyroscope Ring
            gyro_x = 1800 if is_rtl else 120
            gyro_y = 935
            extra.append(f"""
            <g id="spin_isometric_gyro">
                <circle cx="{gyro_x}" cy="{gyro_y}" r="125" fill="none" stroke="{primary}" stroke-width="2" stroke-dasharray="14 8" stroke-opacity="0.45" />
                <circle cx="{gyro_x}" cy="{gyro_y}" r="92" fill="none" stroke="{secondary}" stroke-width="1.5" stroke-dasharray="6 10" stroke-opacity="0.4" />
            </g>
            """)

        elif arch in ("apple_bento", "paper_cutout"):
            # ==================================================================
            # 3D VOLUMETRIC CLAYMORPHISM WORLD: Floating 3D Specular Spheres
            # ==================================================================
            orb_x = 1790 if is_rtl else 130
            orb_y = 920
            alt_x = 150 if is_rtl else 1770
            extra.append(f"""
            <g id="volumetric_3d_spheres">
                <circle cx="{alt_x}" cy="150" r="68" fill="url(#orb_3d_primary)" filter="url(#shadow_3d_soft)" />
                <circle cx="{alt_x + (65 if is_rtl else -65)}" cy="215" r="34" fill="url(#orb_3d_accent)" filter="url(#shadow_3d_soft)" />
                <circle cx="{orb_x}" cy="{orb_y}" r="95" fill="url(#orb_3d_secondary)" filter="url(#shadow_3d_deep)" />
                <circle cx="{orb_x - (90 if is_rtl else -90)}" cy="{orb_y + 55}" r="44" fill="url(#orb_3d_primary)" filter="url(#shadow_3d_soft)" />
            </g>
            <g id="spin_3d_orbit_ring">
                <circle cx="{orb_x}" cy="{orb_y}" r="145" fill="none" stroke="{primary}" stroke-width="2.5" stroke-dasharray="10 12" stroke-opacity="0.45" />
                <circle cx="{orb_x + 145}" cy="{orb_y}" r="12" fill="url(#orb_3d_accent)" />
            </g>
            """)

        elif arch in ("royal_gold", "warm_editorial"):
            # ==================================================================
            # PHOTOREALISTIC MATERIAL WORLD: Metallic Filigree & 3D Gem Orbs
            # ==================================================================
            crest_x = 1790 if is_rtl else 130
            crest_y = 940
            extra.append(f"""
            <g id="photorealistic_luxury_frame">
                <rect x="34" y="34" width="1852" height="1012" fill="none" stroke="url(#grad_metallic_rim)" stroke-width="2" stroke-opacity="0.6" />
                <rect x="46" y="46" width="1828" height="988" fill="none" stroke="{primary}" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="14 8" />
                <circle cx="{crest_x}" cy="{crest_y}" r="72" fill="url(#orb_3d_primary)" filter="url(#shadow_3d_deep)" />
            </g>
            <g id="spin_luxury_astrolabe">
                <circle cx="{crest_x}" cy="{crest_y}" r="135" fill="none" stroke="url(#grad_metallic_rim)" stroke-width="2" stroke-dasharray="8 10" />
                <circle cx="{crest_x}" cy="{crest_y}" r="102" fill="none" stroke="{secondary}" stroke-width="1.5" stroke-dasharray="16 8" stroke-opacity="0.55" />
            </g>
            """)

        elif arch == "blueprint_schematic":
            grid_svg = []
            for gx in range(160, 1840, 160):
                grid_svg.append(f'<line x1="{gx}" y1="40" x2="{gx}" y2="1040" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.22" />')
            for gy in range(140, 1020, 140):
                grid_svg.append(f'<line x1="40" y1="{gy}" x2="1880" y2="{gy}" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.22" />')
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
    # 5. MULTI-DIMENSIONAL COVER SLIDES (`render_cover_slide`)
    # ==========================================================================
    @staticmethod
    def render_cover_slide(renderer, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        """Renders a Cover Slide showcasing the exact Dimensional Paradigm (2.5D, 3D, Photorealistic, or 2D)."""
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

        # Dimensional Centerpiece Sculpture when no external image is provided (or framing it)
        cx_hero = img_x + 375
        cy_hero = 530

        if arch in ("cyber_hud", "bauhaus_modern") and not image_rel_path:
            # Giant 2.5D Isometric Monumental Stacked Tower on Cover Slide!
            svg.append('<g id="iso_25d_cover_monument">')
            for tier_idx, (tr, ty_off, tcol) in enumerate([
                (230, 140, th["secondary"]),
                (175, 20, th["primary"]),
                (115, -95, th.get("accent", th["primary"])),
            ]):
                tf, lf, rf = _iso_cube_faces(cx_hero, cy_hero + ty_off, tr)
                svg.append(f'<polygon points="{lf}" fill="{_shade_color(tcol, -0.18)}" stroke="{tcol}" stroke-width="2" />')
                svg.append(f'<polygon points="{rf}" fill="{_shade_color(tcol, -0.42)}" stroke="{tcol}" stroke-width="2" />')
                svg.append(f'<polygon points="{tf}" fill="{_shade_color(tcol, 0.28)}" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.7" />')
            svg.append('</g>')

        elif arch in ("apple_bento", "paper_cutout") and not image_rel_path:
            # Giant 3D Volumetric Claymorphism Sculpture Cluster on Cover Slide!
            svg.append('<g id="clay_3d_cover_sculpture">')
            svg.append(f'<circle cx="{cx_hero}" cy="{cy_hero}" r="220" fill="url(#orb_3d_primary)" filter="url(#shadow_3d_deep)" />')
            svg.append(f'<circle cx="{cx_hero - 150}" cy="{cy_hero + 130}" r="110" fill="url(#orb_3d_secondary)" filter="url(#shadow_3d_soft)" />')
            svg.append(f'<circle cx="{cx_hero + 160}" cy="{cy_hero - 120}" r="85" fill="url(#orb_3d_accent)" filter="url(#shadow_3d_soft)" />')
            svg.append('</g>')

        elif arch == "neo_brutalist":
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, 940 if rtl else 100, 150, 860, 760))

        elif arch == "blueprint_schematic":
            tb_x = 1220 if rtl else 120
            svg.append('<g id="cad_cover_title_block">')
            svg.append(f'<rect x="{tb_x}" y="760" width="580" height="160" fill="{th["surface"]}" stroke="{th["primary"]}" stroke-width="2.5" />')
            svg.append(f'<line x1="{tb_x}" y1="815" x2="{tb_x + 580}" y2="815" stroke="{th["primary"]}" stroke-width="1.5" />')
            svg.append(f'<line x1="{tb_x + 290}" y1="760" x2="{tb_x + 290}" y2="920" stroke="{th["primary"]}" stroke-width="1.5" />')
            svg.append(f'<text x="{tb_x + 145}" y="795" font-family="monospace" font-size="16" font-weight="700" fill="{th["primary"]}" text-anchor="middle">SCALE: 1:1 // ISO-9001</text>')
            svg.append(f'<text x="{tb_x + 435}" y="795" font-family="monospace" font-size="16" font-weight="700" fill="{th["secondary"]}" text-anchor="middle">SHEET: 01 OF DECK</text>')
            svg.append('</g>')

        # Style-aware Kicker + Title via Polymorphic Container
        kw = max(280, len(kicker) * 18)
        kx = (x_pos - kw) if rtl else x_pos
        svg.extend(ArtStyleSkinEngine.render_card_container(renderer, kx, 195, kw, 60))
        svg.append(f'<text x="{kx + kw / 2}" y="233" font-family="{font}" font-size="20" font-weight="800" fill="{th["primary"]}" text-anchor="middle">{escape_xml(kicker)}</text>')

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
            auth_w = max(340, len(author) * 19)
            auth_x = (x_pos - auth_w) if rtl else x_pos
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, auth_x, 600, auth_w, 76))
            svg.append(f'<text x="{auth_x + auth_w / 2}" y="646" font-family="{font}" font-size="22" font-weight="700" fill="{th["text_main"]}" text-anchor="middle">{escape_xml(author)}</text>')

        # Hero Image Frame with Dimensional Container Silhouette
        if image_rel_path:
            center_hx = img_x + 375
            center_hy = 530
            svg.append('<g id="spin_hero_orbit">')
            svg.append(f'<circle cx="{center_hx}" cy="{center_hy}" r="395" fill="none" stroke="{th["primary"]}" stroke-width="2.2" stroke-opacity="0.4" stroke-dasharray="14 8" />')
            svg.append(f'<circle cx="{center_hx + 395}" cy="{center_hy}" r="10" fill="url(#orb_3d_accent)" />')
            svg.append('</g>')

            svg.append('<g id="hero_image">')
            svg.extend(ArtStyleSkinEngine.render_card_container(renderer, img_x, 195, 750, 665))
            svg.append(f'<image href="{image_rel_path}" x="{img_x + 18}" y="222" width="714" height="620" preserveAspectRatio="xMidYMid slice" />')
            badge_cx = (img_x + 85) if rtl else (img_x + 665)
            svg.extend(ArtStyleSkinEngine.render_icon_badge(renderer, badge_cx, 275, 42, th["primary"], "award", icon_size=42))
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)
