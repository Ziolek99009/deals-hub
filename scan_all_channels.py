import json
import os
import re
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import zip_longest

# =====================================================================
# HIGH-VOLUME DUAL-QUEUE YOUTUBE SCANNER (Amazon + eBay + AliExpress)
# Automatically extracts:
#   1. The exact Amazon affiliate link (amzn.to / amazon.com) from your
#      YouTube video description so each webpage can link straight to
#      that exact Amazon product!
#   2. The full YouTube video description & product specs!
#   3. The exact product name for your 14-country eBay button!
# =====================================================================

SETTINGS_FILE = "MY_SETTINGS.json"

DEFAULT_CHANNELS = [
    {"id": "ch1", "name": "Channel 1 • Smart Home & Kitchen", "url": "https://www.youtube.com/@GoogleDevelopers"},
    {"id": "ch2", "name": "Channel 2 • Auto & Car Gadgets", "url": "https://www.youtube.com/@YouTubeCreators"},
    {"id": "ch3", "name": "Channel 3 • Daily Tech & EDC", "url": "https://www.youtube.com/@AndroidDevelopers"},
]


def load_channels():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            chans = data.get("YOUTUBE_CHANNELS", [])
            valid = [c for c in chans if "@YourChannel" not in c.get("url", "")]
            if valid:
                return valid
        except Exception:
            pass
    return DEFAULT_CHANNELS


def extract_amazon_link_from_description(description):
    """Finds the exact amzn.to or amazon.* affiliate URL inside your YouTube description
    so your webpage's Gold Amazon Button links straight to that exact product!"""
    if not description:
        return ""
    match = re.search(
        r"(https?://(?:www\.)?(?:amzn\.to|a\.co|amazon\.[a-z\.]+)/[^\s\)\]]+)",
        description,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else ""


def extract_product_from_youtube_description_amazon_link(description, fallback_title):
    """Extracts the exact product name from the Amazon link inside your YouTube description."""
    if not description:
        return fallback_title

    slug_match = re.search(
        r"amazon\.[a-z\.]+/([A-Za-z0-9\-]{5,120})/dp/[A-Z0-9]{10}",
        description,
        flags=re.IGNORECASE,
    )
    if slug_match:
        product_from_slug = slug_match.group(1).replace("-", " ").strip()
        if len(product_from_slug) > 5:
            return product_from_slug

    for line in description.splitlines():
        if re.search(r"(?:amzn\.to|a\.co|amazon\.[a-z\.]+)", line, flags=re.IGNORECASE):
            clean_label = re.sub(r"https?://\S+", "", line)
            clean_label = re.sub(r"[^A-Za-z0-9\s\-\+]", " ", clean_label)
            clean_label = re.sub(r"\s{2,}", " ", clean_label).strip()
            if len(clean_label) >= 6:
                return clean_label

    return fallback_title


def clean_youtube_description_for_webpage(description):
    """Keeps your full YouTube product description & specs to show on the webpage."""
    if not description:
        return ""
    cleaned = re.sub(
        r"https?://(?:www\.)?(?:amzn\.to|a\.co|amazon\.[a-z\.]+)/[^\s\)\]]*",
        "",
        description,
        flags=re.IGNORECASE,
    )
    return cleaned.strip()


def fetch_videos_from_one_channel(ch_id, channel_name, channel_url, max_per_tab=10000):
    collected = []
    seen = set()
    for tab in ["/videos", "/shorts"]:
        target = channel_url.rstrip("/") + tab
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            "--playlist-end", str(max_per_tab),
            target
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                for entry in data.get("entries", []):
                    vid_id = entry.get("id")
                    raw_title = entry.get("title", "")
                    description = entry.get("description", "")
                    amazon_url = extract_amazon_link_from_description(description)
                    exact_product = extract_product_from_youtube_description_amazon_link(
                        description, clean_youtube_description_for_webpage(raw_title)
                    )
                    cleaned_desc = clean_youtube_description_for_webpage(description)
                    dur = entry.get("duration")
                    dur_str = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "2:30"
                    if vid_id and exact_product and vid_id not in seen:
                        seen.add(vid_id)
                        collected.append({
                            "video_id": vid_id,
                            "title": exact_product,
                            "amazon_url": amazon_url,
                            "yt_description": cleaned_desc,
                            "duration": dur_str,
                            "channel_id": ch_id,
                            "channel_name": channel_name,
                            "yt_url": f"https://www.youtube.com/watch?v={vid_id}"
                        })
        except Exception as e:
            print(f"Note scanning {target}: {e}")
    return collected


def build_round_robin_library(daily_fast_mode=False):
    channels = load_channels()
    limit = 40 if daily_fast_mode else 10000
    per_channel_lists = []

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {
            pool.submit(fetch_videos_from_one_channel, ch["id"], ch["name"], ch["url"], limit): ch
            for ch in channels
        }
        for fut in as_completed(futures):
            vids = fut.result()
            if vids:
                per_channel_lists.append(vids)

    newly_scanned = []
    for group in zip_longest(*per_channel_lists):
        for item in group:
            if item is not None:
                newly_scanned.append(item)

    existing = []
    if os.path.exists("videos_library.json"):
        try:
            with open("videos_library.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    seen_ids = set()
    merged = []
    for v in newly_scanned + existing:
        vid = v.get("video_id")
        if vid and vid not in seen_ids:
            seen_ids.add(vid)
            merged.append(v)

    with open("videos_library.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(f"Library now holds {len(merged)} total videos (with Amazon description links + eBay/AliExpress)!")


if __name__ == "__main__":
    fast = "--daily-new" in sys.argv
    build_round_robin_library(daily_fast_mode=fast)
