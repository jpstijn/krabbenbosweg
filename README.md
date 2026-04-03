# Home Assistant configuration

Personal [Home Assistant](https://www.home-assistant.io/) config kept in Git for backup and change history.

## What’s tracked

Core config as YAML (`configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`), `blueprints/`, `esphome/`, and other `custom_components/` integrations. **`custom_components/hacs/` is ignored** (huge file count; reinstall [HACS](https://hacs.xyz/) after a restore).

## What’s not in Git

See `.gitignore`: databases (`*.db`), logs, runtime/cache, `.storage/`, `secrets.yaml`, and Python `__pycache__` / bytecode. Recreate or copy `secrets.yaml` and let HA rebuild internal DB/storage on a fresh install.

## Combined radar dashboard

- **Helper:** `input_select.radar_dashboard_location` (Hal / Werkkamer) lives in `configuration.yaml`.
- **Dashboard:** `dashboards/radar_combined.yaml` — generated from `.storage/lovelace.radar_hal` and `.storage/lovelace.radar_werkkamer` so both UIs stay in sync:

  `python3 scripts/build_radar_combined_dashboard.py`

After changing either radar dashboard in the UI, re-run the script and reload resources / restart HA as needed.

## Restore (sketch)

1. Restore this folder as the HA `config` directory (or merge into it).
2. Ensure `secrets.yaml` exists with real values (not from this repo).
3. Start Home Assistant and confirm the UI loads.
4. If `custom_components/hacs/` was not restored from Git, install [HACS](https://hacs.xyz/docs/setup/download), then reinstall any HACS integrations you use from the UI.
