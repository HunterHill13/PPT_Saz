#!/usr/bin/env python3
"""
PPT_Saz - Native PowerPoint Presentation Generator Orchestrator
Takes structured slide content (text, layout, images, animations) and produces
a native, editable PowerPoint (.pptx) presentation with full animations, transitions, and RTL/Persian support.
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
from image_pipeline import fetch_or_create_placeholder

configure_utf8_stdio()


def is_persian(text: str) -> bool:
    """Check if the text contains Persian/Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def load_themes() -> Dict[str, Any]:
    """Load theme definitions from presets/themes.json."""
    theme_file = _SCRIPTS_DIR.parent / "presets" / "themes.json"
    if not theme_file.exists():
        theme_file = _SCRIPTS_DIR / "themes.json"
    if theme_file.exists():
        with open(theme_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # Default fallback theme
    return {
        "corporate_blue": {
            "name": "Corporate Blue",
            "background": "#0B132B",
            "surface": "#1C2541",
            "surface_border": "#3A506B",
            "primary": "#48CAE4",
            "secondary": "#00B4D8",
            "text_main": "#F8FAFC",
            "text_muted": "#94A3B8",
            "accent": "#F59E0B",
            "font_fa": "Vazirmatn, Tahoma, Arial",
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
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" lang="{lang}">
<!-- Background -->
<rect width="{self.width}" height="{self.height}" fill="{self.theme['background']}" />
"""

    def render_title_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        title = slide.get("title", "عنوان ارائه")
        subtitle = slide.get("subtitle", "")
        author = slide.get("author", "")
        rtl = is_persian(title) or is_persian(subtitle)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        x_pos = 1720 if rtl else 200

        svg = [self._header_svg(rtl)]

        # Title group
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{x_pos}" y="420" font-family="{font}" font-size="68" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        if subtitle:
            svg.append(f'<text x="{x_pos}" y="520" font-family="{font}" font-size="34" font-weight="600" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(subtitle)}</text>')
        if author:
            svg.append(f'<text x="{x_pos}" y="620" font-family="{font}" font-size="24" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(author)}</text>')
        svg.append('</g>')

        # Accent Bar
        svg.append('<g id="accent_bar">')
        if rtl:
            svg.append(f'<rect x="1740" y="360" width="12" height="180" fill="{self.theme["primary"]}" rx="6" />')
        else:
            svg.append(f'<rect x="160" y="360" width="12" height="180" fill="{self.theme["primary"]}" rx="6" />')
        svg.append('</g>')

        if image_rel_path:
            svg.append('<g id="hero_image">')
            svg.append(f'<rect x="{100 if rtl else 1100}" y="240" width="700" height="600" rx="24" fill="{self.theme["surface"]}" stroke="{self.theme["primary"]}" stroke-width="3" />')
            svg.append(f'<image href="{image_rel_path}" x="{110 if rtl else 1110}" y="250" width="680" height="580" preserveAspectRatio="xMidYMid slice" />')
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_content_cards_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "بخش اصلی")
        cards = slide.get("cards", [])
        rtl = is_persian(title) or any(is_persian(str(c)) for c in cards)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        title_x = 1800 if rtl else 120
        align = "end" if rtl else "start"

        svg = [self._header_svg(rtl)]

        # Top Header
        svg.append('<g id="header_group">')
        svg.append(f'<text x="{title_x}" y="120" font-family="{font}" font-size="22" font-weight="600" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{title_x}" y="180" font-family="{font}" font-size="52" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        # Cards Layout (2 or 3 or 4 cards)
        count = max(1, len(cards))
        margin = 120
        gap = 40
        card_y = 260
        card_h = 680
        total_w = self.width - (2 * margin) - ((count - 1) * gap)
        card_w = total_w / count

        for i, card in enumerate(cards):
            c_title = card.get("title", f"مورد {i+1}")
            c_desc = card.get("desc", "")
            
            if rtl:
                c_x = (self.width - margin) - ((i + 1) * card_w) - (i * gap)
            else:
                c_x = margin + (i * (card_w + gap))

            svg.append(f'<g id="card_{i+1}">')
            svg.append(f'<rect x="{c_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="16" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
            
            # Badge or Accent header
            badge_y = card_y + 40
            bx = (c_x + card_w - 60) if rtl else (c_x + 60)
            svg.append(f'<circle cx="{bx}" cy="{badge_y+20}" r="24" fill="{self.theme["primary"]}" fill-opacity="0.2" />')
            svg.append(f'<text x="{bx}" y="{badge_y+28}" font-family="{font}" font-size="20" fill="{self.theme["primary"]}" font-weight="700" text-anchor="middle">{i+1}</text>')

            # Card title
            tx = (c_x + card_w - 60) if rtl else (c_x + 60)
            svg.append(f'<text x="{tx}" y="{card_y + 130}" font-family="{font}" font-size="32" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(c_title)}</text>')

            # Card description
            desc_lines = c_desc.split("\n")
            curr_y = card_y + 200
            for line in desc_lines[:8]:
                if line.strip():
                    svg.append(f'<text x="{tx}" y="{curr_y}" font-family="{font}" font-size="22" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(line.strip())}</text>')
                    curr_y += 42
            svg.append('</g>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_split_image_slide(self, slide: Dict[str, Any], image_rel_path: Optional[str] = None) -> str:
        title = slide.get("title", "عنوان اسلاید")
        kicker = slide.get("kicker", "بررسی تخصصی")
        bullets = slide.get("bullets", [])
        rtl = is_persian(title) or any(is_persian(str(b)) for b in bullets)

        font = self.theme.get('font_fa' if rtl else 'font_en')
        align = "end" if rtl else "start"
        text_x = 1800 if rtl else 120
        image_x = 120 if rtl else 1020
        image_y = 180
        image_w = 780
        image_h = 760

        svg = [self._header_svg(rtl)]

        # Header & Text
        svg.append('<g id="title_group">')
        svg.append(f'<text x="{text_x}" y="140" font-family="{font}" font-size="24" font-weight="600" fill="{self.theme["primary"]}" text-anchor="{align}">{escape_xml(kicker)}</text>')
        svg.append(f'<text x="{text_x}" y="210" font-family="{font}" font-size="52" font-weight="700" fill="{self.theme["text_main"]}" text-anchor="{align}">{escape_xml(title)}</text>')
        svg.append('</g>')

        svg.append('<g id="bullets_group">')
        tx = text_x
        curr_y = 320
        for i, bullet in enumerate(bullets):
            svg.append(f'<g id="bullet_{i+1}">')
            dot_x = (tx - 10) if rtl else (tx + 10)
            text_pos_x = (tx - 40) if rtl else (tx + 40)
            svg.append(f'<circle cx="{dot_x}" cy="{curr_y-8}" r="8" fill="{self.theme["primary"]}" />')
            svg.append(f'<text x="{text_pos_x}" y="{curr_y}" font-family="{font}" font-size="26" font-weight="400" fill="{self.theme["text_muted"]}" text-anchor="{align}">{escape_xml(bullet)}</text>')
            svg.append('</g>')
            curr_y += 85
        svg.append('</g>')

        # Image Container
        svg.append('<g id="hero_image">')
        svg.append(f'<rect x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" rx="20" fill="{self.theme["surface"]}" stroke="{self.theme["surface_border"]}" stroke-width="2" />')
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

    print(f"Creating presentation with {len(slides)} slides...")

    for idx, slide in enumerate(slides, start=1):
        slide_stem = f"{idx:02d}_{slide.get('slug', f'slide_{idx}')}"
        layout = slide.get("layout", "content_cards")
        
        # Sourcing / Fetching Image if requested
        img_filename = f"img_{idx:02d}.jpg"
        img_rel_for_svg = f"../images/{img_filename}"
        img_query = slide.get("image_query", slide.get("image_prompt", slide.get("title", "presentation")))
        
        # Acquire image
        img_path = fetch_or_create_placeholder(img_query, images_dir, img_filename, theme=deck_data.get("theme_category", "technology"))

        # Render SVG
        if layout == "title_hero" or idx == 1:
            svg_content = renderer.render_title_slide(slide, image_rel_path=img_rel_for_svg)
        elif layout == "split_image":
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

    # Set destination PPTX path
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
