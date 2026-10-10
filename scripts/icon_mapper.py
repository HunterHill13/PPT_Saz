#!/usr/bin/env python3
"""
PPT_Saz - Vector Icon Mapper & Embedder
Finds, parses, and embeds vector SVG icons from templates/icons/tabler-outline/
with automatic semantic keyword matching (Persian & English) and theme-colored styling.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
_ICONS_DIR = _SCRIPTS_DIR.parent / "templates" / "icons" / "tabler-outline"

# Semantic keyword to icon filename mapping (Persian and English)
KEYWORD_ICON_MAP = {
    # AI & Computing
    "ai": "brain",
    "هوش": "brain",
    "مغز": "brain",
    "یادگیری": "brain",
    "داده": "database",
    "data": "database",
    "پردازش": "cpu",
    "cpu": "cpu",
    "پردازنده": "cpu",
    "سخت‌افزار": "cpu",
    "نرم‌افزار": "code",
    "برنامه‌نویسی": "code",
    "کد": "code",
    "سرور": "server",
    "ابر": "cloud",
    "cloud": "cloud",
    "ربات": "robot",
    "robot": "robot",
    "اتوماسیون": "robot",

    # Business & Analytics
    "آمار": "chart-bar",
    "تحلیل": "chart-arrows",
    "نمودار": "chart-line",
    "رشد": "trending-up",
    "افزایش": "trending-up",
    "مالی": "coin",
    "سرمایه‌گذاری": "currency-dollar",
    "استراتژی": "target",
    "هدف": "target",
    "مدیریت": "briefcase",
    "کسب‌وکار": "building",

    # Security & Quality
    "امنیت": "shield-check",
    "حفاظت": "shield-lock",
    "تایید": "circle-check",
    "موفقیت": "trophy",
    "کیفیت": "rosette-check",
    "قانون": "scale",

    # Innovation & Speed
    "ایده": "bulb",
    "خلاقیت": "sparkles",
    "نوآوری": "bulb",
    "سرعت": "rocket",
    "پرتاب": "rocket",
    "پیشرفت": "rocket",
    "انرژی": "bolt",
    "بهره‌وری": "gauge",

    # Communication & People
    "کاربر": "user",
    "تیم": "users",
    "همکاری": "users-group",
    "ارتباط": "share",
    "شبکه": "network",
    "آموزش": "school",
    "پژوهش": "microscope",
    "تحقیق": "search",
    "پزشکی": "heartbeat",
    "سلامت": "heart",
    "تنظیمات": "settings",
    "ابزار": "tools",
}


def find_icon_path(keyword_or_name: str) -> Optional[Path]:
    """Find the path to an SVG icon matching a name or keyword."""
    if not _ICONS_DIR.exists():
        return None

    clean = keyword_or_name.strip().lower()

    # Direct match if already a known icon name
    direct = _ICONS_DIR / f"{clean}.svg"
    if direct.exists():
        return direct

    # Check semantic dictionary
    for k, icon_name in KEYWORD_ICON_MAP.items():
        if k in clean:
            match_path = _ICONS_DIR / f"{icon_name}.svg"
            if match_path.exists():
                return match_path

    # Check substring match in directory
    for f in _ICONS_DIR.glob(f"*{clean}*.svg"):
        return f

    return None


def get_icon_svg_content(
    keyword_or_name: str,
    x: float,
    y: float,
    size: float = 48,
    stroke_color: str = "#48CAE4",
    stroke_width: float = 2.0
) -> str:
    """
    Load the icon SVG file and return it as a scaled, positioned SVG <g>
    compatible with DrawingML conversion (no nested root svg, pure paths).
    """
    icon_path = find_icon_path(keyword_or_name)
    if not icon_path:
        # Fallback to a clean check or star
        icon_path = find_icon_path("sparkles") or find_icon_path("circle-check")

    if not icon_path or not icon_path.exists():
        # Minimal geometric star/diamond fallback
        return f"""<g transform="translate({x}, {y})">
            <polygon points="{size/2},0 {size},{size/2} {size/2},{size} 0,{size/2}" fill="none" stroke="{stroke_color}" stroke-width="{stroke_width}" />
        </g>"""

    try:
        content = icon_path.read_text(encoding="utf-8")
        # Extract inner path / polygon / line elements from the SVG
        # Tabler icons have viewBox 0 0 24 24
        inner_elements = []
        for line in content.splitlines():
            line_str = line.strip()
            if line_str.startswith("<path") or line_str.startswith("<circle") or line_str.startswith("<line") or line_str.startswith("<polygon"):
                # Clean up existing stroke and fill attributes to inject our custom theme colors
                clean_line = re.sub(r'stroke="[^"]*"', '', line_str)
                clean_line = re.sub(r'fill="[^"]*"', '', clean_line)
                clean_line = re.sub(r'stroke-width="[^"]*"', '', clean_line)
                clean_line = clean_line.replace("  ", " ").strip()
                inner_elements.append(clean_line)

        scale = size / 24.0
        inner_body = "\n        ".join(inner_elements)
        return f"""<g transform="translate({x}, {y}) scale({scale})" stroke="{stroke_color}" fill="none" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
        {inner_body}
</g>"""
    except Exception as e:
        print(f"Warning: Failed to load icon {icon_path}: {e}", file=sys.stderr)
        return ""


if __name__ == "__main__":
    svg = get_icon_svg_content("هوش مصنوعی", 100, 100, 64, "#00B4D8")
    print(svg)
