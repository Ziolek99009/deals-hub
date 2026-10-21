import json
import os
import re
import sys
import subprocess
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import zip_longest
import requests

# =====================================================================
# HIGH-VOLUME 4-CHANNEL YOUTUBE SCANNER (270 New/Day + 20k Back-Catalog)
# Every 4-hour GitHub Actions run (6x/day):
#   1. Scans up to 3,000 videos per channel in parallel (~45s) so it
#      sees BOTH all 270 daily new uploads AND your existing back-catalog.
#   2. Adds up to 120 new/back-catalog videos per 4-hour run (720/day =
#      all 270 new daily uploads + 450 back-catalog videos/day!).
#   3. Extracts the exact Amazon product link (/dp/ASIN?tag=ziolek-20 or
#      amzn.to/...) and full YouTube description for every added video!
# =====================================================================

SETTINGS_FILE = "MY_SETTINGS.json"
DEMO_VIDEO_IDS = {"IBVmenOroPs", "dQw4w9WgXcQ", "ysz5S6PUM-U", "aqz-KE-bpKQ"}

CHANNEL_NAME_MAP = {
    "ch1": "KitchenGear",
    "ch2": "Simple Home Reviews",
    "ch3": "Bedroom Comfort",
    "ch4": "WorldShoping",
}

DEFAULT_CHANNELS = [
    {"id": "ch1", "name": "KitchenGear", "url": "https://www.youtube.com/channel/UCdcte1tNyB_F6a4P9S1V7dw"},
    {"id": "ch2", "name": "Simple Home Reviews", "url": "https://www.youtube.com/channel/UCJuQdlTl_DE_7E4TbgcXUtQ/"},
    {"id": "ch3", "name": "Bedroom Comfort", "url": "https://www.youtube.com/channel/UCizMutB0xtYKPsXGUQDfy-Q/"},
    {"id": "ch4", "name": "WorldShoping", "url": "https://www.youtube.com/channel/UC8dMCVIMDD--MPY1Bwe_OKQ/"},
]

import urllib.parse

# Max newly added videos to enrich per 4-hour run:
# 150 per 4-hour run x 6 runs/day = 900 videos/day (all 270 new daily uploads + 630 back-catalog/day!)
MAX_NEW_VIDEOS_PER_RUN = 150


def load_channels():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            chans = data.get("YOUTUBE_CHANNELS", [])
            valid = [c for c in chans if "@YourChannel" not in c.get("url", "")]
            if valid:
                for idx, c in enumerate(valid, 1):
                    cid = c.get("id") or f"ch{idx}"
                    c["id"] = cid
                    if "•" in c.get("name", "") or not c.get("name") or c.get("name", "").startswith("Channel "):
                        c["name"] = CHANNEL_NAME_MAP.get(cid, f"Channel {idx}")
                return valid
        except Exception:
            pass
    return DEFAULT_CHANNELS


def extract_amazon_link_from_description(description):
    if not description:
        return ""
    match = re.search(
        r"(https?://(?:www\.)?(?:amzn\.to|a\.co|amazon\.[a-z\.]+)/[^\s\)\"\]]+)",
        description,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else ""


def clean_summary_for_transcript(raw_desc, fallback_title):
    if not raw_desc:
        return f"Hands-on video overview of {fallback_title} covering key specifications, sizing, and daily usability."
    notes = re.sub(r"https?://\S+", "", raw_desc)
    notes = re.sub(r"Product link:\s*🔗?\s*Check it out:\s*", "", notes, flags=re.I)
    notes = re.sub(r"Link to Buy\s*-\s*", "", notes, flags=re.I)
    notes = re.sub(r"🔗\s*Check it out:\s*", "", notes, flags=re.I)
    notes = re.sub(r"Disclosure:.*?(?:cost to you\.|purchases\.|link\.)", "", notes, flags=re.I)
    notes = re.sub(r"As an Amazon Associate[^\.]*\.", "", notes, flags=re.I)
    notes = re.sub(r"This helps support the channel at no extra cost to you\.", "", notes, flags=re.I)
    notes = re.sub(r"#\w+", "", notes)
    notes = re.sub(r"\s{2,}", " ", notes).strip(" -—•:")
    return notes[:550] if len(notes) > 30 else f"Hands-on video overview of {fallback_title} covering key specifications, sizing, and daily usability."


def fetch_xml_feed_lookup(channel_url):
    lookup = {}
    m = re.search(r"channel/(UC[A-Za-z0-9_\-]+)", channel_url)
    if not m:
        return lookup
    yt_cid = m.group(1)
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={yt_cid}"
    try:
        r = requests.get(feed_url, timeout=12)
        if r.status_code == 200 and "<feed" in r.text:
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "media": "http://search.yahoo.com/mrss/",
            }
            root = ET.fromstring(r.text)
            for entry in root.findall("atom:entry", ns):
                vid_el = entry.find("yt:videoId", ns)
                title_el = entry.find("atom:title", ns)
                desc_el = entry.find("media:group/media:description", ns)
                if vid_el is not None and vid_el.text:
                    vid = vid_el.text.strip()
                    raw_desc = desc_el.text if (desc_el is not None and desc_el.text) else ""
                    title = title_el.text.strip() if (title_el is not None and title_el.text) else "Product Review"
                    lookup[vid] = {
                        "title": title,
                        "raw_desc": raw_desc,
                    }
    except Exception:
        pass
    return lookup


def enrich_video_from_watch_page(v):
    if v.get("amazon_url") and ("/dp/" in v["amazon_url"] or "amzn.to" in v["amazon_url"]) and v.get("yt_description") and "..." not in v["amazon_url"]:
        return v
    vid = v.get("video_id", "")
    if not vid:
        return v
    try:
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20261015.01.00",
                    "hl": "en",
                    "gl": "US",
                }
            },
            "videoId": vid,
        }
        r = requests.post("https://www.youtube.com/youtubei/v1/next?prettyPrint=false", json=payload, timeout=10)
        raw_desc = ""
        m = re.search(r'"attributedDescriptionBodyText":\{"content":"((?:\\.|[^"\\])*)"', r.text)
        if m:
            raw_desc = json.loads('"' + m.group(1) + '"')
        amz_url = ""
        for qm in re.finditer(r'q=(https?%3A%2F%2F[^&"\\]+)', r.text):
            u = urllib.parse.unquote(qm.group(1))
            if "amazon." in u or "amzn.to" in u or "a.co" in u:
                amz_url = u
                break
        if not amz_url and raw_desc:
            amz_url = extract_amazon_link_from_description(raw_desc)
        if amz_url and amz_url.endswith("?..."):
            amz_url = amz_url.replace("?...", "?tag=ziolek-20")
        if amz_url:
            v["amazon_url"] = amz_url
            if raw_desc:
                raw_desc = re.sub(r"https?://(?:www\.)?amazon\.[a-z\.]+/dp/[A-Z0-9]{10}\?\.\.\.", amz_url, raw_desc)
        if raw_desc:
            v["yt_description"] = re.sub(r"\s{2,}", " ", raw_desc).strip()[:1400]
            v["transcript_summary"] = clean_summary_for_transcript(raw_desc, v.get("title", "Product Review"))
    except Exception:
        pass
    return v


def fetch_videos_from_one_channel(ch_id, channel_name, channel_url, max_per_tab=3000):
    collected = []
    seen = set()
    real_name = CHANNEL_NAME_MAP.get(ch_id, channel_name)
    xml_lookup = fetch_xml_feed_lookup(channel_url)

    for vid_id, info in xml_lookup.items():
        raw_desc = info["raw_desc"]
        amz = extract_amazon_link_from_description(raw_desc)
        full_desc = re.sub(r"\s{2,}", " ", raw_desc).strip()[:1400]
        seen.add(vid_id)
        collected.append({
            "video_id": vid_id,
            "title": info["title"],
            "amazon_url": amz,
            "yt_description": full_desc,
            "transcript_summary": clean_summary_for_transcript(raw_desc, info["title"]),
            "duration": "1:45",
            "channel_id": ch_id,
            "channel_name": real_name,
            "yt_url": f"https://www.youtube.com/watch?v={vid_id}"
        })

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
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                for entry in data.get("entries", []):
                    vid_id = entry.get("id")
                    if not vid_id or vid_id in DEMO_VIDEO_IDS:
                        continue
                    dur = entry.get("duration")
                    dur_str = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "1:45"
                    if vid_id in seen:
                        for c_item in collected:
                            if c_item["video_id"] == vid_id and dur:
                                c_item["duration"] = dur_str
                        continue
                    raw_title = entry.get("title", "Product Review")
                    seen.add(vid_id)
                    collected.append({
                        "video_id": vid_id,
                        "title": raw_title,
                        "amazon_url": "",
                        "yt_description": "",
                        "transcript_summary": "",
                        "duration": dur_str,
                        "channel_id": ch_id,
                        "channel_name": real_name,
                        "yt_url": f"https://www.youtube.com/watch?v={vid_id}"
                    })
        except Exception as e:
            print(f"Note scanning {target}: {e}")
    return collected


def build_round_robin_library(daily_fast_mode=False):
    channels = load_channels()
    # Scan up to 3,000 videos per channel in parallel (~45 seconds total)
    # so both the 270 daily new uploads AND the back-catalog are discovered!
    limit = 3000 if daily_fast_mode else 10000
    per_channel_lists = []

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(fetch_videos_from_one_channel, ch["id"], ch["name"], ch["url"], limit): ch
            for ch in channels
        }
        for fut in as_completed(futures):
            vids = fut.result()
            if vids:
                per_channel_lists.append(vids)

    all_discovered = []
    for group in zip_longest(*per_channel_lists):
        for item in group:
            if item is not None:
                all_discovered.append(item)

    existing = []
    if os.path.exists("videos_library.json"):
        try:
            with open("videos_library.json", "r", encoding="utf-8") as f:
                raw_existing = json.load(f)
            existing = [
                v for v in raw_existing
                if "•" not in v.get("channel_name", "")
                and v.get("video_id") not in DEMO_VIDEO_IDS
            ]
        except Exception:
            existing = []

    existing_by_id = {v.get("video_id"): v for v in existing if v.get("video_id")}

    # Separate truly new/unadded videos from already-saved videos
    brand_new_batch = []
    seen_new = set()
    for v in all_discovered:
        vid = v.get("video_id")
        if vid and vid not in existing_by_id and vid not in seen_new and vid not in DEMO_VIDEO_IDS:
            seen_new.add(vid)
            brand_new_batch.append(v)
            if len(brand_new_batch) >= MAX_NEW_VIDEOS_PER_RUN:
                break

    # Enrich the newly added batch (up to 120 per 4-hour run = 720/day) in parallel!
    to_enrich_new = [v for v in brand_new_batch if not v.get("amazon_url") or not v.get("yt_description")]
    if to_enrich_new:
        with ThreadPoolExecutor(max_workers=24) as ex:
            list(ex.map(enrich_video_from_watch_page, to_enrich_new))

    # Merge newly added batch at the top + all existing library videos
    seen_ids = set()
    merged = []
    for v in brand_new_batch + existing:
        vid = v.get("video_id")
        if vid and vid not in seen_ids and vid not in DEMO_VIDEO_IDS:
            seen_ids.add(vid)
            cid = v.get("channel_id", "ch1")
            v["channel_name"] = CHANNEL_NAME_MAP.get(cid, v.get("channel_name", "KitchenGear"))
            prev = existing_by_id.get(vid, {})
            if prev.get("amazon_url") and not v.get("amazon_url"):
                v["amazon_url"] = prev["amazon_url"]
            if prev.get("yt_description") and not v.get("yt_description"):
                v["yt_description"] = prev["yt_description"]
            if prev.get("transcript_summary") and not v.get("transcript_summary"):
                v["transcript_summary"] = prev["transcript_summary"]
            merged.append(v)

    with open("videos_library.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    real_amz_count = sum(1 for v in merged if v.get("amazon_url"))
    print(f"Added {len(brand_new_batch)} new/vault videos this run -> Library now holds {len(merged)} real videos ({real_amz_count} with direct Amazon product links)!")


if __name__ == "__main__":
    fast = "--daily-new" in sys.argv
    build_round_robin_library(daily_fast_mode=fast)
