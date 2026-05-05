#!/usr/bin/env python3
"""
scripts/fetch_external.py

Downloads external large files referenced in EXTERNAL_FILES.md into
../removed_large_files (by default). Expects EXTERNAL_FILES.md to contain
the shareable Google Drive folder URL or file URLs.

Usage:
  python scripts/fetch_external.py

The script will attempt to install `gdown` if it's not available.
"""
from pathlib import Path
import re
import subprocess
import sys
import os


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_MD = ROOT / "EXTERNAL_FILES.md"
DEST_DIR = Path(os.getenv("EXTERNAL_FILES_DIR", str(ROOT.parent / "removed_large_files")))
DEST_DIR.mkdir(parents=True, exist_ok=True)


def ensure_gdown():
    try:
        import gdown  # type: ignore
        return True
    except Exception:
        print("gdown not found, attempting to install it...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"], stdout=subprocess.DEVNULL)
            import gdown  # type: ignore
            return True
        except Exception as e:
            print("Failed to install gdown:", e)
            return False


def find_urls_in_md(path: Path):
    if not path.exists():
        return []
    txt = path.read_text(encoding="utf-8")
    # crude URL extractor
    urls = re.findall(r"https?://[^\s)]+", txt)
    return urls


def run_gdown(args):
    cmd = [sys.executable, "-m", "gdown"] + args
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def download_from_folder(url: str):
    # gdown supports --folder for Google Drive folders
    run_gdown(["--folder", url, "-O", str(DEST_DIR)])


def download_files(urls):
    for u in urls:
        # If the url looks like a Drive folder, download folder
        if "/drive/folders/" in u or "folders/" in u:
            print("Detected folder URL; downloading folder:", u)
            download_from_folder(u)
        else:
            print("Downloading file URL:", u)
            run_gdown([u, "-O", str(DEST_DIR)])


def main():
    urls = find_urls_in_md(EXTERNAL_MD)
    if not urls:
        print(f"No URLs found in {EXTERNAL_MD}. Please paste your Drive folder or file link into EXTERNAL_FILES.md and re-run.")
        sys.exit(2)

    if not ensure_gdown():
        print("gdown is required to download from Google Drive. Install it manually: pip install gdown")
        sys.exit(3)

    try:
        download_files(urls)
    except subprocess.CalledProcessError as e:
        print("Download failed:", e)
        sys.exit(4)

    # List downloaded files
    print("Downloaded files to:", DEST_DIR)
    for p in sorted(DEST_DIR.iterdir()):
        print(" -", p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
