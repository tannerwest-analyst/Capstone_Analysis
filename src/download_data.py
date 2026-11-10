import hashlib
import json
from datetime import date
from pathlib import Path

import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "oews_metro_may2025.zip": "https://www.bls.gov/oes/special-requests/oesm25ma.zip",
    "hud_fmr_fy2026.xlsx": "https://hudgis-hud.opendata.arcgis.com/api/download/v1/items/12d2516901f947b5bb4da4e780e35f07/csv?layers=0"
}

HEADERS = {
    # BLS often rejects requests with no browser-like User-Agent
    "User-Agent": "Mozilla/5.0 (capstone project; contact: tannerlc07@gmail.com)"
}

def download(name, url):
    dest = RAW / name
    if dest.exists():
        print(f"skip {name} (already downloaded)")
        return
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return {
        "file": name,
        "url": url,
        "downloaded": date.today().isoformat(),
        "sha256": hashlib.sha256(r.content).hexdigest(),
    }

if __name__ == "__main__":
    log = [m for n, u in SOURCES.items() if (m := download(n, u))]
    if log:
        with open(RAW / "download_log.json", "a") as f:
            f.write(json.dumps(log, indent=2) + "\n")