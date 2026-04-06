#!/usr/bin/env python3
"""Build dashboards/radar_combined.yaml from ONE UI-editable Lovelace dashboard.

The template dashboard uses Frontdoor radar entities. The script duplicates each section
Office, Toilet, Backdoor, and Storage (entity id substitution) and adds input_select
visibility so the UI dropdown still works.

Template storage file (after you create dashboard id `radar_template` in HA):
  .storage/lovelace.radar_template

If you add locations, update RADAR_LOCATIONS below and configuration.yaml options.

Output is JSON (valid YAML 1.2) for Home Assistant.
"""

import json
import sys
from pathlib import Path

# Must match options in configuration.yaml (input_select.radar_dashboard_location)
SELECT_ENTITY = "input_select.radar_dashboard_location"

# Template must reference FRONTDOOR_ENTITY_INFIX everywhere; other rows are generated
# by substituting that substring for each location's infix.
RADAR_LOCATIONS = [
    ("Frontdoor", "radar_frontdoor"),
    ("Office", "radar_office"),
    ("Toilet", "radar_toilet"),
    ("Backdoor", "radar_backdoor"),
    ("Storage", "radar_storage"),
]
FRONTDOOR_ENTITY_INFIX = RADAR_LOCATIONS[0][1]

TEMPLATE_STORAGE = "lovelace.radar_template"


def wrap_card(card, select_state, section_visibility=None):
    card = dict(card)
    vis = list(card.get("visibility") or [])
    if section_visibility:
        vis.extend(section_visibility)
    vis.append({"condition": "state", "entity": SELECT_ENTITY, "state": select_state})
    card["visibility"] = vis
    return card


def clone_section_for_infix(sec, entity_infix):
    blob = json.dumps(sec)
    if entity_infix != FRONTDOOR_ENTITY_INFIX:
        blob = blob.replace(FRONTDOOR_ENTITY_INFIX, entity_infix)
    return json.loads(blob)


def merge_section_grids(template_sec, selector_card):
    out_cards = []
    if selector_card is not None:
        out_cards.append(selector_card)
    for state, infix in RADAR_LOCATIONS:
        sec = clone_section_for_infix(template_sec, infix)
        s_vis = sec.get("visibility")
        for c in sec.get("cards", []):
            out_cards.append(wrap_card(c, state, s_vis))
    merged = {"type": "grid", "cards": out_cards}
    for k in ("column_span", "columns"):
        if k in template_sec:
            merged[k] = template_sec[k]
    return merged


def main():
    root = Path(__file__).resolve().parents[1]
    store = root / ".storage"
    path = store / TEMPLATE_STORAGE
    if not path.is_file():
        print(
            f"Missing {path}\n"
            "In Home Assistant: Settings → Dashboards → Add dashboard → "
            "pick an ID/key `radar_template` (storage mode). "
            "Design the layout with Frontdoor radar entities, then re-run.",
            file=sys.stderr,
        )
        sys.exit(1)

    raw = json.loads(path.read_text(encoding="utf-8"))
    try:
        view = raw["data"]["config"]["views"][0]
    except (KeyError, IndexError) as e:
        print(f"Unexpected template JSON shape: {e}", file=sys.stderr)
        sys.exit(1)

    sections = view.get("sections") or []
    if not sections:
        print("Template has no sections", file=sys.stderr)
        sys.exit(1)

    selector_card = {
        "type": "entities",
        "title": "Radar",
        "entities": [SELECT_ENTITY],
    }

    new_sections = []
    for i, sec in enumerate(sections):
        sel = selector_card if i == 0 else None
        new_sections.append(merge_section_grids(sec, sel))

    out_view = {
        "type": "sections",
        "max_columns": view.get("max_columns", 4),
        "path": "radar-combined",
        "title": view.get("title", "Radars"),
        "sections": new_sections,
    }

    doc = {"views": [out_view]}
    out = root / "dashboards" / "radar_combined.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} from {path.name}")


if __name__ == "__main__":
    main()
