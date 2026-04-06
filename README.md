# Home Assistant configuration

Personal [Home Assistant](https://www.home-assistant.io/) config kept in Git for backup and change history.

## What’s tracked

Core config as YAML (`configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`), `blueprints/`, `esphome/`, and other `custom_components/` integrations. **`custom_components/hacs/` is ignored** (huge file count; reinstall [HACS](https://hacs.xyz/) after a restore).

## What’s not in Git

See `.gitignore`: databases (`*.db`), logs, runtime/cache, `.storage/`, `secrets.yaml`, and Python `__pycache__` / bytecode. Recreate or copy `secrets.yaml` and let HA rebuild internal DB/storage on a fresh install.

## Combined radar dashboard

- **Helper:** `input_select.radar_dashboard_location` (Hal / Werkkamer) in `configuration.yaml`.
- **What you edit in the HA UI:** a **storage** dashboard whose id is **`radar_template`** (creates `.storage/lovelace.radar_template`). Use the visual editor there. Optionally hide it in the sidebar under **Settings → Dashboards** if you only browse the generated **Radars (combi)** entry.

- **Generated output:** `dashboards/radar_combined.yaml` (YAML mode, Git-friendly). Build it with:

  `python3 scripts/build_radar_combined_dashboard.py`

The template must use **Hal** entity ids (`ld2412_c3_5_hal_voordeur`). The script clones the layout for **Werkkamer** (`ld2412_c3_2_werkkamer`) and wires the location dropdown. If entity names change, edit the `HAL_ENTITY_INFIX` / `WK_ENTITY_INFIX` constants in `scripts/build_radar_combined_dashboard.py`.

After editing the template in the UI, re-run the script, then reload Lovelace (or restart HA). You can remove the old separate Hal/Werkkamer dashboards once the template is in place.

## Restore (sketch)

1. Restore this folder as the HA `config` directory (or merge into it).
2. Ensure `secrets.yaml` exists with real values (not from this repo).
3. Start Home Assistant and confirm the UI loads.
4. If `custom_components/hacs/` was not restored from Git, install [HACS](https://hacs.xyz/docs/setup/download), then reinstall any HACS integrations you use from the UI.
