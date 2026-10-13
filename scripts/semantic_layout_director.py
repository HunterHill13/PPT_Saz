#!/usr/bin/env python3
"""
PPT Master / PPT_Saz v5.0 — Autonomous Semantic Layout Director & Rhythm Engine

Inspired by PPTAgent (EMNLP) and DOC2PPT (AAAI):
  1. Analyzes the semantic meaning of each slide's Persian/English title, kicker,
     and body items without altering a single character of user text.
  2. Selects the optimal visual diagram/layout from 17 structural archetypes.
  3. Enforces the strict Anti-Repetition Rhythm Law: no two consecutive slides
     may ever share the same layout, and repeated generic layouts (like
     content_cards or process_steps) are automatically diversified into
     creative diagrams (Pyramid, Funnel, Venn, Quadrant 2x2, Snake Roadmap,
     Mind-Map, Fishbone, Radar Chart, Smart Table).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List


ALL_SUPPORTED_LAYOUTS = (
    "title_hero",
    "content_cards",
    "process_steps",
    "stats_kpi",
    "comparison",
    "circular_orbit",
    "split_image",
    "pyramid_hierarchy",
    "funnel_pipeline",
    "venn_synergy",
    "quadrant_matrix_2x2",
    "snake_roadmap",
    "mind_map_hub",
    "fishbone_cause_effect",
    "data_chart_showcase",
    "smart_table_matrix",
    "hero_callout_quote",
    "closing_thankyou",
)

# Complementary alternatives when a layout was already used or repeats consecutively
DIVERSIFICATION_POOLS: Dict[str, List[str]] = {
    "content_cards": [
        "content_cards",
        "pyramid_hierarchy",
        "venn_synergy",
        "mind_map_hub",
        "quadrant_matrix_2x2",
        "circular_orbit",
        "smart_table_matrix",
    ],
    "process_steps": [
        "process_steps",
        "snake_roadmap",
        "funnel_pipeline",
        "fishbone_cause_effect",
    ],
    "stats_kpi": [
        "stats_kpi",
        "data_chart_showcase",
        "smart_table_matrix",
    ],
    "comparison": [
        "comparison",
        "quadrant_matrix_2x2",
        "smart_table_matrix",
    ],
}


def _slide_text_blob(slide: Dict[str, Any]) -> str:
    parts = [
        str(slide.get("title", "")),
        str(slide.get("kicker", "")),
        str(slide.get("subtitle", "")),
    ]
    for key in ("cards", "steps", "kpis", "items", "bullets"):
        for item in slide.get(key, []) or []:
            if isinstance(item, dict):
                parts.append(str(item.get("title", "")))
                parts.append(str(item.get("desc", "")))
            else:
                parts.append(str(item))
    return " ".join(parts).lower()


def infer_semantic_layout(slide: Dict[str, Any], idx: int, total_slides: int) -> str:
    """Infer the best visual layout for a single slide based on its content & position."""
    explicit = slide.get("layout", "").strip()
    if explicit and explicit != "auto" and explicit in ALL_SUPPORTED_LAYOUTS:
        return explicit

    if idx == 1:
        return "title_hero"

    header_blob = f"{slide.get('title', '')} {slide.get('kicker', '')} {slide.get('slug', '')}".lower()
    blob = _slide_text_blob(slide)

    # Check if final slide is a closing / thank you / conclusion
    if idx == total_slides and total_slides >= 4:
        if any(w in header_blob for w in ("تشکر", "سپاس", "پرسش", "پایان", "جمع‌بندی", "thank", "q&a", "conclusion", "closing")):
            return "closing_thankyou"

    if slide.get("col_a") and slide.get("col_b"):
        return "comparison"

    # High-priority matching on Title + Kicker first, then full blob
    for target_text in (header_blob, blob):
        if any(w in target_text for w in ("جدول", "ماتریس ارزیابی", "مشخصات فنی", "table", "specification")):
            return "smart_table_matrix"

        if any(w in target_text for w in ("علت و معلول", "ریشه‌یابی", "استخوان ماهی", "fishbone", "ishikawa", "root cause")):
            return "fishbone_cause_effect"

        if any(w in target_text for w in ("نقشه ذهنی", "شاخه‌های", "هسته مرکزی", "شعاعی", "mind map", "mindmap", "ecosystem")):
            return "mind_map_hub"

        if any(w in target_text for w in ("نمودار", "چارت", "راداری", "radar", "chart", "benchmark")):
            return "data_chart_showcase"

        if any(w in target_text for w in ("هرم", "سلسله‌مراتب", "سطوح", "pyramid", "hierarchy")):
            return "pyramid_hierarchy"

        if any(w in target_text for w in ("قیف", "پالایش", "غربالگری", "فیلترینگ", "funnel", "filtering", "screening")):
            return "funnel_pipeline"

        if any(w in target_text for w in ("هم‌افزایی", "هم‌پوشانی", "سه رکن", "تلاقی", "venn", "synergy", "overlap")):
            return "venn_synergy"

        if any(w in target_text for w in ("swot", "چهارگانه", "چهار ربع", "quadrant", "2x2", "ماتریس چهار")):
            return "quadrant_matrix_2x2"

        if any(w in target_text for w in ("نقل‌قول", "چشم‌انداز کلان", "بیانیه", "quote", "manifesto")):
            return "hero_callout_quote"

        if any(w in target_text for w in ("موجی", "زیگزاگ", "snake", "journey")):
            return "snake_roadmap"

    if any(w in header_blob for w in ("مقایسه", "در برابر", "تفاوت", "versus", "vs", "comparison")):
        return "comparison"

    if slide.get("kpis") or any(w in header_blob for w in ("آمار", "شاخص", "بازدهی", "kpi", "metrics")):
        return "stats_kpi"

    if slide.get("steps") or any(w in header_blob for w in ("مراحل", "فرآیند", "گام", "نقشه راه", "مسیر", "process", "roadmap", "steps", "timeline")):
        return "process_steps"

    # Count items to pick smart structural default
    items = slide.get("cards") or slide.get("items") or slide.get("bullets") or []
    if len(items) == 4:
        return "quadrant_matrix_2x2"

    return "content_cards"


def orchestrate_deck_layouts(slides: List[Dict[str, Any]], diversify_existing: bool = False) -> List[str]:
    """
    Assign layouts across the entire deck while enforcing the Anti-Repetition Rhythm Law:
      - No two consecutive slides ever share the same layout.
      - Repeated generic layouts are automatically rotated through creative infographic diagrams.
    """
    total = len(slides)
    assigned: List[str] = []
    usage_counts: Dict[str, int] = {}

    for idx, slide in enumerate(slides, start=1):
        explicit = slide.get("layout", "").strip()
        is_explicit_custom = (
            explicit
            and explicit != "auto"
            and not diversify_existing
            and explicit not in ("content_cards", "process_steps", "stats_kpi")
        )

        base_layout = infer_semantic_layout(slide, idx, total)
        prev_layout = assigned[-1] if assigned else None

        if is_explicit_custom and base_layout != prev_layout:
            chosen = base_layout
        else:
            pool = DIVERSIFICATION_POOLS.get(base_layout, [base_layout])
            count_used = usage_counts.get(base_layout, 0)

            # If this layout wasn't used yet and doesn't repeat the previous slide, keep it
            if count_used == 0 and base_layout != prev_layout:
                chosen = base_layout
            else:
                # Pick the first candidate in the pool that differs from prev_layout and has minimal usage
                candidates = [c for c in pool if c != prev_layout]
                if not candidates:
                    candidates = [c for c in ALL_SUPPORTED_LAYOUTS if c not in ("title_hero", "closing_thankyou", prev_layout)]
                candidates.sort(key=lambda c: usage_counts.get(c, 0))
                chosen = candidates[0]

        assigned.append(chosen)
        usage_counts[chosen] = usage_counts.get(chosen, 0) + 1

    return assigned
