# freqtrade-bot11feb2026

This repository contains the multi-strategy trading engine and related Freqtrade user_data.

## Contents
- `multi-strat-engine/` — 1m + 2–3h strategies, trade loop, reports
- `user_data/` — Freqtrade configs and strategies

## Notes
- Secrets are stored in `.env` or local config files; do not commit secrets.
- Systemd service runs the live bot: `multistrat.service`.

## Run
```bash
cd /opt/multi-strat-engine
/opt/freqtrade/.venv/bin/python trade_loop.py
```
