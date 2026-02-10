import csv, time, json
from pathlib import Path
import ccxt

CONFIG_PATH = "/opt/freqtrade/user_data/config.binance_futures_live.json"
IN_FILE = Path('/opt/multi-strat-engine/reports/filtered_signals.csv')
OUT_FILE = Path('/opt/multi-strat-engine/reports/filtered_signals.csv')
HORIZON_MIN = 15


def main():
    if not IN_FILE.exists():
        print('no file')
        return
    rows = []
    with IN_FILE.open() as f:
        r = csv.DictReader(f)
        rows = list(r)

    cfg = json.loads(Path(CONFIG_PATH).read_text())
    ex = ccxt.binance({
        "apiKey": cfg['exchange']['key'],
        "secret": cfg['exchange']['secret'],
        "enableRateLimit": True,
        "options": {"defaultType":"future"},
    })

    now = time.time()
    updated = []
    for row in rows:
        if row.get('outcome'):
            updated.append(row); continue
        ts = float(row.get('ts'))
        if now - ts < HORIZON_MIN*60:
            updated.append(row); continue
        symbol = row.get('pair')
        side = row.get('side')
        entry = float(row.get('price'))
        try:
            ticker = ex.fetch_ticker(symbol.replace('USDT', '/USDT') if '/' not in symbol else symbol)
            price = float(ticker.get('last') or ticker.get('close') or entry)
        except Exception:
            price = entry
        if side == 'LONG':
            pnl = (price - entry) / entry
        else:
            pnl = (entry - price) / entry
        row['outcome'] = 'win' if pnl > 0 else ('loss' if pnl < 0 else 'flat')
        row['pnl_pct'] = f"{pnl*100:.4f}"
        row['exit_price'] = f"{price}"
        row['horizon_min'] = str(HORIZON_MIN)
        updated.append(row)

    with OUT_FILE.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=updated[0].keys())
        w.writeheader()
        w.writerows(updated)
    print('updated')

if __name__ == '__main__':
    main()
