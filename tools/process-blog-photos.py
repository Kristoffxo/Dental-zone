#!/usr/bin/env python3
"""Prepare Independence Day photos for the blog post.

Usage:
    1. Drop the original photos into images/blog/  (any filenames)
    2. python3 tools/process-blog-photos.py --list      # show what's there
    3. python3 tools/process-blog-photos.py --apply     # rename + optimise

The mapping in ASSIGN is filled in by hand after looking at the photos, because
only a human (or a model that can see them) can tell which shot is which.
"""
import argparse, os, sys, glob, shutil

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow required:  python3 -m pip install --user Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "images", "blog")
RAW  = os.path.join(BLOG, "_originals")

# canonical name -> (max width, note). Portraits keep more height, banners less.
TARGETS = {
    "id2026-team-flag":     1800,   # hero + homepage card + OG image
    "id2026-group-flags":   1800,   # wide banner in the gallery
    "id2026-doctor-desk-1": 1600,
    "id2026-team-seated":   1600,
    "id2026-selfie-staff":  1200,
    "id2026-selfie-four":   1200,
    "id2026-doctor-desk-2": 1200,
}

# original filename -> canonical name. Filled in after inspection.
ASSIGN = {}


def listing():
    files = sorted(
        f for f in glob.glob(os.path.join(BLOG, "*"))
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic", ".webp"))
        and "_originals" not in f
    )
    if not files:
        print("nothing in images/blog/ yet")
        return
    print(f"{len(files)} file(s) in images/blog/\n")
    for f in files:
        try:
            with Image.open(f) as im:
                w, h = im.size
                kind = "landscape" if w > h * 1.15 else "portrait" if h > w * 1.15 else "square"
                print(f"  {os.path.basename(f):<44} {w:>5}x{h:<5} {kind:<10} "
                      f"{os.path.getsize(f)//1024:>5} KB")
        except Exception as e:
            print(f"  {os.path.basename(f):<44} !! unreadable: {e}")


def apply():
    if not ASSIGN:
        sys.exit("ASSIGN is empty — fill it in after running --list")

    os.makedirs(RAW, exist_ok=True)
    for src_name, canon in ASSIGN.items():
        src = os.path.join(BLOG, src_name)
        if not os.path.exists(src):
            print(f"  skip (missing): {src_name}")
            continue

        # keep an untouched copy before we downscale anything
        backup = os.path.join(RAW, src_name)
        if not os.path.exists(backup):
            shutil.copy2(src, backup)

        with Image.open(src) as im:
            im = im.convert("RGB")
            before = os.path.getsize(src) // 1024
            cap = TARGETS.get(canon, 1600)
            if im.size[0] > cap:
                im = im.resize((cap, round(im.size[1] * cap / im.size[0])), Image.LANCZOS)
            out = os.path.join(BLOG, canon + ".jpg")
            im.save(out, "JPEG", quality=84, optimize=True, progressive=True)
            after = os.path.getsize(out) // 1024
            print(f"  {src_name}  ->  {canon}.jpg   {im.size}  {before}KB -> {after}KB")

        if os.path.abspath(src) != os.path.abspath(out):
            os.remove(src)

    print("\ndone — originals preserved in images/blog/_originals/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list",  action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.apply:
        apply()
    else:
        listing()
