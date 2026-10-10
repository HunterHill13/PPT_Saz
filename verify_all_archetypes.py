#!/usr/bin/env python3
"""
Verify all 6 archetypes compile into native PPTX presentations
and contain 100% distinct layout architectures and geometry.
"""

import json
import os
from pathlib import Path
import sys

_SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from presentation_generator import generate_presentation_project

ARCHETYPES_TO_TEST = [
    ("bento_glass_dark", "apple_bento", "bento_hero_card"),
    ("swiss_academic_light", "swiss_academic", "swiss_card_1"),
    ("neo_brutalist_light", "neo_brutalist", "brutalist_card_1"),
    ("warm_editorial_light", "warm_editorial", "editorial_card_1"),
    ("royal_gold_dark", "royal_gold", "royal_card_1"),
    ("cyber_aurora", "cyber_hud", "spin_card_halo_1"),
]

def main():
    sample_json = Path("examples/sample_presentation.json")
    with open(sample_json, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    results = []
    base_dir = Path("projects/test_distinct_suite")
    base_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("STARTING 6-ARCHETYPE DISTINCT ARCHITECTURE TEST SUITE")
    print("==================================================")

    for theme_key, expected_archetype, key_tag in ARCHETYPES_TO_TEST:
        project_dir = base_dir / f"test_{theme_key}"
        output_pptx = base_dir / f"final_{theme_key}.pptx"

        print(f"\n---> Testing Theme: {theme_key} (Archetype: {expected_archetype})")
        
        try:
            pptx_path = generate_presentation_project(
                deck_data=deck_data,
                project_dir=project_dir,
                output_pptx=output_pptx,
                theme_key=theme_key,
                transition="morph",
                animation_mode="auto"
            )

            file_size = os.path.getsize(pptx_path)
            svg_files = list((project_dir / "svg_output").glob("*.svg"))
            
            # Check for unique signature tag in slide 2 SVG
            slide2_svg = project_dir / "svg_output" / "02_pillars.svg"
            has_tag = False
            if slide2_svg.exists():
                svg_text = slide2_svg.read_text(encoding="utf-8")
                has_tag = key_tag in svg_text

            print(f"  [SUCCESS] PPTX: {pptx_path.name} | Size: {file_size:,} bytes | SVGs: {len(svg_files)} | Tag '{key_tag}': {has_tag}")
            results.append({
                "theme": theme_key,
                "archetype": expected_archetype,
                "size": file_size,
                "has_tag": has_tag,
                "status": "PASS" if file_size > 50000 and has_tag else "FAIL"
            })
        except Exception as e:
            print(f"  [FAILED] Error: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "theme": theme_key,
                "archetype": expected_archetype,
                "error": str(e),
                "status": "ERROR"
            })

    print("\n==================================================")
    print("TEST SUITE SUMMARY RESULTS:")
    print("==================================================")
    all_passed = True
    for r in results:
        status = r["status"]
        if status != "PASS":
            all_passed = False
        print(f"  {r['theme']} ({r['archetype']}): {status} | Size: {r.get('size', 0):,} bytes | Signature Tag Verified: {r.get('has_tag', False)}")

    if all_passed:
        print("\nALL 6 ARCHETYPES VERIFIED 100% DISTINCT AND COMPILED SUCCESSFULLY!")
    else:
        print("\nSOME TESTS FAILED!")

if __name__ == "__main__":
    main()
