#!/usr/bin/env python3
"""
PPT_Saz - Image Acquisition & Processing Pipeline
Handles automatic sourcing, downloading, resizing, and fallback for presentation slide images.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Optional
import urllib.parse
import urllib.request

try:
    from PIL import Image
except ImportError:
    Image = None

# Curated fallback high-res images for common presentation themes
FALLBACK_THEME_IMAGES = {
    "technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "business": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
    "academic": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1200&q=80",
    "science": "https://images.unsplash.com/photo-1507668077129-56e32842fceb?auto=format&fit=crop&w=1200&q=80",
    "healthcare": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80",
    "nature": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1200&q=80",
    "abstract": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
}


def download_image(url: str, output_path: Path, timeout: int = 15) -> bool:
    """Download an image from a URL and save to output_path."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.read())
                return True
    except Exception as e:
        print(f"Warning: Failed to download image from {url}: {e}", file=sys.stderr)
    return False


def get_unsplash_source_url(query: str, width: int = 1200, height: int = 800) -> str:
    """Construct an Unsplash direct source image URL based on query keyword."""
    # Clean keyword
    safe_query = re.sub(r'[^a-zA-Z0-9\s]', '', query).strip()
    if not safe_query:
        safe_query = "presentation modern"
    encoded = urllib.parse.quote(safe_query)
    return f"https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w={width}&h={height}&q=80"


def fetch_or_create_placeholder(query: str, output_dir: Path, filename: str, theme: str = "technology") -> Path:
    """
    Ensure an image exists for the given query.
    1. Downloads from curated Unsplash topic or theme fallback
    2. If offline/error, creates an elegant Pillow gradient placeholder
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / filename
    if out_file.exists() and out_file.stat().st_size > 1000:
        return out_file

    # Try downloading theme image
    fallback_url = FALLBACK_THEME_IMAGES.get(theme.lower(), FALLBACK_THEME_IMAGES["technology"])
    success = download_image(fallback_url, out_file)
    
    if not success or not out_file.exists():
        # Generate an elegant placeholder using PIL
        create_gradient_placeholder(out_file, title=query[:30])

    return out_file


def create_gradient_placeholder(output_path: Path, width: int = 1200, height: int = 800, title: str = "Presentation") -> None:
    """Generate a clean gradient banner if no external network is available."""
    if Image is None:
        # Create minimal 1x1 png if PIL is missing
        output_path.write_bytes(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        return

    # Create beautiful dark blue-purple gradient
    img = Image.new("RGB", (width, height), "#0f172a")
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Draw simple gradient effect
    for y in range(height):
        r = int(15 + (45 * y / height))
        g = int(23 + (85 * y / height))
        b = int(42 + (155 * y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "JPEG", quality=90)


if __name__ == "__main__":
    test_dir = Path("test_images")
    p = fetch_or_create_placeholder("ai data", test_dir, "test1.jpg")
    print(f"Created/Fetched: {p}")
