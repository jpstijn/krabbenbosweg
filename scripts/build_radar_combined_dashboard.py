#!/usr/bin/env python3
"""Merge .storage/lovelace.radar_hal + lovelace.radar_werkkamer into dashboards/radar_combined.yaml.

Run after editing either radar dashboard in the UI (copy from .storage) or adjust this script.
Output is JSON (valid YAML 1.2) for Home Assistant.
"""

import json
import sys
from pathlib import Path

HAL_STATE = "Hal"
WERK_STATE = "Werkkamer"
SELECT_ENTITY = "input_select.radar_dashboard_location"


def wrap_card(card, select_state, section_visibility=None):
    card = dict(card)
    vis = list(card.get("visibility") or [])
    if section_visibility:
        vis.extend(section_visibility)
    vis.append({"condition": "state", "entity": SELECT_ENTITY, "state": select_state})
    card["visibility"] = vis
    return card


def merge_section_grids(h_sec, w_sec, selector_card):
    h_vis = h_sec.get("visibility")
    w_vis = w_sec.get("visibility")
    out_cards = []
    if selector_card is not None:
        out_cards.append(selector_card)
    for c in h_sec.get("cards", []):
        out_cards.append(wrap_card(c, HAL_STATE, h_vis))
    for c in w_sec.get("cards", []):
        out_cards.append(wrap_card(c, WERK_STATE, w_vis))
    sec = {"type": "grid", "cards": out_cards}
    for k in ("column_span", "columns"):
        if k in h_sec:
            sec[k] = h_sec[k]
    return sec


def main():
    root = Path(__file__).resolve().parents[1]
    store = root / ".storage"
    hal = json.loads((store / "lovelace.radar_hal").read_text(encoding="utf-8"))
    wk = json.loads((store / "lovelace.radar_werkkamer").read_text(encoding="utf-8"))

    vh = hal["data"]["config"]["views"][0]
    vw = wk["data"]["config"]["views"][0]
    sh, sw = vh["sections"], vw["sections"]

    if len(sh) != len(sw):
        print("Section count mismatch", file=sys.stderr)
        sys.exit(1)

    selector_card = {
        "type": "entities",
        "title": "Radar",
        "entities": [SELECT_ENTITY],
    }

    new_sections = []
    for i, (h_sec, w_sec) in enumerate(zip(sh, sw)):
        sel = selector_card if i == 0 else None
        new_sections.append(merge_section_grids(h_sec, w_sec, sel))

    view = {
        "type": "sections",
        "max_columns": vh.get("max_columns", 4),
        "path": "radar-combined",
        "title": "Radars",
        "sections": new_sections,
    }

    doc = {"views": [view]}
    out = root / "dashboards" / "radar_combined.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
