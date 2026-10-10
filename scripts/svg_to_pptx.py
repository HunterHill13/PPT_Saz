#!/usr/bin/env python3
"""PPT_Saz - SVG to PPTX Compilation Tool.

Batch-converts SVG slide decks to editable PowerPoint presentations (.pptx)
with DrawingML shapes, native animations, and native slide transitions.
"""

import sys
from pathlib import Path

# Ensure the scripts directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from console_encoding import configure_utf8_stdio
from svg_to_pptx import main

configure_utf8_stdio()

if __name__ == '__main__':
    raise SystemExit(main())
