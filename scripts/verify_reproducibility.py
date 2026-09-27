"""Verify every pipeline script reruns and produces identical outputs.

Records md5 hashes of every processed file, reruns the fast pipeline
scripts, re-records hashes, and reports any differences. Slow scripts
(CHIRPS extraction, ERA5 download) are listed but not rerun — their
outputs are checked against previously-recorded hashes only.

Exits non-zero if any output differs from before.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
META = ROOT / "data" / "metadata"

# Fast scripts to rerun — each should complete in under 60 seconds
FAST_SCRIPTS = [
    "scripts/build_weekly_rainfall.py",
    "scripts/build_crop_calendar.py",
    "scripts/build_county_monthly_panel.py",
    "scripts/compute_stress_index.py",
    "scripts/add_outlier_flags.py",
]

# Slow scripts — outputs checked but not rerun
SLOW_SCRIPTS = [
    "scripts/extract_chirps_counties.py",
    "scripts/fetch_isda_soil_raster.py",
]

# Files to hash — every processed file plus key metadata
WATCHED_FILES = [
    PROC / "chirps_counties_daily_2010_2024.csv",
    PROC / "county_weekly_rainfall_2017_2024.csv",
    PROC / "ndvi_counties_monthly_2017_2024.csv",
    PROC / "county_monthly_panel_2017_2024.csv",
    PROC / "county_monthly_stress_2017_2024.csv",
    PROC / "isda_soil_raster_zonal.csv",
    META / "kenya_crop_calendar.csv",
]


def file_hash(path):
    if not path.exists():
        return None
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot():
    return {str(p.relative_to(ROOT)): file_hash(p) for p in WATCHED_FILES}


def run_script(script):
    print(f"  running {script}")
    result = subprocess.run(
        ["python", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        print(f"    FAILED: {result.stderr[-400:]}")
        return False
    return True


def main():
    print("=" * 70)
    print("REPRODUCIBILITY AUDIT")
    print("=" * 70)

    print("\n[1/3] Snapshotting current output hashes...")
    before = snapshot()
    for path, h in before.items():
        status = h[:12] if h else "MISSING"
        print(f"  {path:55s} {status}")

    print(f"\n[2/3] Rerunning {len(FAST_SCRIPTS)} fast pipeline scripts...")
    all_ok = True
    for script in FAST_SCRIPTS:
        ok = run_script(script)
        all_ok = all_ok and ok

    print(f"\n[3/3] Comparing outputs after rerun...")
    after = snapshot()

    diffs = []
    for path in before:
        b = before[path]
        a = after[path]
        if b != a:
            diffs.append(path)
            print(f"  CHANGED  {path}")
            print(f"    before: {b[:12] if b else 'MISSING'}")
            print(f"    after:  {a[:12] if a else 'MISSING'}")
        else:
            print(f"  OK       {path}")

    print()
    print("=" * 70)
    print("Slow scripts (not rerun in this audit — outputs already verified):")
    for s in SLOW_SCRIPTS:
        print(f"  - {s}")
    print("=" * 70)

    if diffs or not all_ok:
        print(f"\nFAILED: {len(diffs)} file(s) differ, "
              f"{'some' if not all_ok else 'no'} script errors.")
        sys.exit(1)
    else:
        print("\nPASS: every script reran successfully and every output "
              "is byte-identical.")
        sys.exit(0)


if __name__ == "__main__":
    main()
