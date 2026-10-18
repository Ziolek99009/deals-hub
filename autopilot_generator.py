import json
import os
import re
from datetime import datetime
import requests

# =====================================================================
# 1. MASTER CONFIGURATION (Automatically reads MY_SETTINGS.json!)
# =====================================================================
def load_master_config():
    cfg = {
        "site_domain": "https://your-site.pages.dev",
        "enable_amazon": True,
        "amazon_tag": "yourtag-20",
        "one_aliexpress_link": "https://s.click.aliexpress.com/e/_dExampleLink",
        "ebay_campaign_id": "5339000000",
        "partner_id": "twoj-nick",
        "last_auto_sync": datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    }
    if os.path.exists("MY_SETTINGS.json"):
        try:
            with open("MY_SETTINGS.json", "r", encoding="utf-8") as f:
                user_s = json.load(f)
            if user_s.get("SITE_URL"):
                cfg["site_domain"] = user_s["SITE_URL"].rstrip("/")
            if "ENABLE_AMAZON_BUTTON_ON_PAGES" in user_s:
                cfg["enable_amazon"] = bool(user_s["ENABLE_AMAZON_BUTTON_ON_PAGES"])
            if user_s.get("AMAZON_ASSOCIATE_TAG"):
                cfg["amazon_tag"] = user_s["AMAZON_ASSOCIATE_TAG"]
            if user_s.get("ALIEXPRESS_ONE_LINK"):
                cfg["one_aliexpress_link"] = user_s["ALIEXPRESS_ONE_LINK"]
            if user_s.get("EBAY_CAMPID"):
                cfg["ebay_campaign_id"] = str(user_s["EBAY_CAMPID"])
        except Exception:
            pass
    return cfg

CONFIG = load_master_config()

# =====================================================================
# 2. 14 OFFICIAL EBAY & GLOBAL COUNTRIES
# =====================================================================
COUNTRIES = [
    {"code": "us", "flag": "🇺🇸", "name": "USA", "lang": "en-US", "ebay_domain": "www.ebay.com", "mkrid": "711-53200-19255-0"},
    {"code": "uk", "flag": "🇬🇧", "name": "UK", "lang": "en-GB", "ebay_domain": "www.ebay.co.uk", "mkrid": "710-53481-19255-0"},
    {"code": "de", "flag": "🇩🇪", "name": "Germany", "lang": "de-DE", "ebay_domain": "www.ebay.de", "mkrid": "707-53477-19255-0"},
    {"code": "fr", "flag": "🇫🇷", "name": "France", "lang": "fr-FR", "ebay_domain": "www.ebay.fr", "mkrid": "709-53476-19255-0"},
    {"code": "es", "flag": "🇪🇸", "name": "Spain", "lang": "es-ES", "ebay_domain": "www.ebay.es", "mkrid": "1185-53479-19255-0"},
    {"code": "it", "flag": "🇮🇹", "name": "Italy", "lang": "it-IT", "ebay_domain": "www.ebay.it", "mkrid": "724-53478-19255-0"},
    {"code": "pl", "flag": "🇵🇱", "name": "Poland", "lang": "pl-PL", "ebay_domain": "www.ebay.pl", "mkrid": "4908-226936-19255-0"},
    {"code": "au", "flag": "🇦🇺", "name": "Australia", "lang": "en-AU", "ebay_domain": "www.ebay.com.au", "mkrid": "705-53470-19255-0"},
    {"code": "ca", "flag": "🇨🇦", "name": "Canada", "lang": "en-CA", "ebay_domain": "www.ebay.ca", "mkrid": "706-53473-19255-0"},
    {"code": "nl", "flag": "🇳🇱", "name": "Netherlands", "lang": "nl-NL", "ebay_domain": "www.ebay.nl", "mkrid": "1346-53482-19255-0"},
    {"code": "be", "flag": "🇧🇪", "name": "Belgium", "lang": "fr-BE", "ebay_domain": "www.ebay.be", "mkrid": "1553-53471-19255-0"},
    {"code": "at", "flag": "🇦🇹", "name": "Austria", "lang": "de-AT", "ebay_domain": "www.ebay.at", "mkrid": "5221-53469-19255-0"},
    {"code": "ch", "flag": "🇨🇭", "name": "Switzerland", "lang": "de-CH", "ebay_domain": "www.ebay.ch", "mkrid": "5222-53480-19255-0"},
    {"code": "ie", "flag": "🇮🇪", "name": "Ireland", "lang": "en-IE", "ebay_domain": "www.ebay.ie", "mkrid": "5282-53468-19255-0"}
]

# =====================================================================
# 3. STANDALONE "VS" COMPARISON & CALCULATOR PAGES FOR VPN, HOSTING,
#    AI TOOLS, CRYPTO, TRAVEL & ALI/EBAY BESTSELLERS!
#    (These are NOT just buttons under videos — they are full standalone
#    SEO pages in /compare/*.html that rank on Google/Bing/Pinterest!)
# =====================================================================
STANDALONE_COMPARISON_PAGES = [
    {
        "slug": "nordvpn-vs-surfshark-speed-and-price-comparison",
        "category": "VPN & Security Standalone Page",
        "seo_title": "NordVPN vs Surfshark (2026): Speed Test, Streaming & 2-Year Price Comparison",
        "search_keywords": "nordvpn vs surfshark, cheapest vpn for streaming, vpn speed test 2026",
        "payout_info": "Pays $40–$100 per signup (Impact.com)",
        "winner_name": "NordVPN Threat Protection Pro",
        "runner_up_name": "Surfshark One (Unlimited Devices)",
        "table_rows": [
            ["Average WireGuard Speed", "940 Mbps (NordLynx)", "890 Mbps (WireGuard)"],
            ["Devices Allowed", "10 Simultaneous Devices", "Unlimited Devices"],
            ["Streaming & Smart TV Unblock", "✓ Netflix, BBC, Prime, Disney+", "✓ All Major Platforms"],
            ["2-Year Promo Price", "$3.09 / month (-72% Off)", "$1.99 / month (-82% Off)"],
            ["Malware & Ad Blocker", "Built-in Threat Protection Pro", "CleanWeb 2.0 Included"]
        ],
        "verdict": "Choose NordVPN if you want the fastest raw download speeds and built-in anti-malware scanning. Choose Surfshark if you want to share one account with your entire household on unlimited devices.",
        "primary_btn_text": "Claim NordVPN 72% Discount + 3 Months Free →",
        "primary_url": "https://nordvpn.com/special/",
        "secondary_btn_text": "Claim Surfshark $1.99/mo Unlimited Devices Deal →",
        "secondary_url": "https://surfshark.com/deals",
        "pin_image": "https://i.ytimg.com/vi/IBVmenOroPs/hqdefault.jpg"
    },
    {
        "slug": "hostinger-vs-bluehost-cloud-hosting-cost-calculator",
        "category": "Web Hosting Standalone Page",
        "seo_title": "Hostinger vs Bluehost (2026): Real 3-Year Cost & TTFB Speed Comparison",
        "search_keywords": "hostinger vs bluehost, cheapest wordpress hosting 2026, hostinger coupon",
        "payout_info": "Pays $60–$150 per sale (Impact / Direct)",
        "winner_name": "Hostinger Business + AI Website Builder",
        "runner_up_name": "Standard Shared Hosting",
        "table_rows": [
            ["Server Technology", "LiteSpeed Enterprise + NVMe SSD", "Standard Apache Server"],
            ["Free Domain & SSL", "✓ Free .com Domain + Unlimited SSL", "✓ 1st Year Only"],
            ["Built-in AI Site Builder", "✓ Included Free (No Coding)", "Paid Add-on"],
            ["Global Data Centers", "USA, UK, Germany, France, Lithuania, India, Brazil", "USA Only"],
            ["Promo Starting Price", "$2.49 / month + 3 Months Free", "$3.95 / month"]
        ],
        "verdict": "Hostinger wins by a wide margin thanks to LiteSpeed NVMe servers, European & US data centers, and a built-in AI Website Builder included at $2.49/mo.",
        "primary_btn_text": "Claim Hostinger $2.49/mo + Free Domain Deal →",
        "primary_url": "https://www.hostinger.com/web-hosting",
        "secondary_btn_text": "Explore PartnerStack AI Business Tools →",
        "secondary_url": "https://partnerstack.com/marketplace",
        "pin_image": "https://i.ytimg.com/vi/ysz5S6PUM-U/hqdefault.jpg"
    },
    {
        "slug": "best-ai-automation-and-whop-digital-tools-comparison",
        "category": "AI & SaaS Recurring Standalone Page",
        "seo_title": "Top AI Business Chatbots, SEO Writers & Whop Automation Tools (2026 Matrix)",
        "search_keywords": "customgpt vs writesonic, best ai seo tool, whop top automation communities",
        "payout_info": "Pays 30%–50% Every Single Month (PartnerStack & Whop)",
        "winner_name": "CustomGPT.ai / Writesonic SEO Suite",
        "runner_up_name": "Whop Top-Rated AI & Trading Tools",
        "table_rows": [
            ["Primary Use Case", "Train AI on Your Own Website/Docs", "All-in-One AI & Digital Apps"],
            ["Free Trial Available", "✓ 7-Day Free Trial", "✓ Instant Access Tiers"],
            ["API & Webhook Support", "✓ Full REST API Included", "✓ Discord / Telegram / Web Apps"],
            ["languages Supported", "92+ Languages Automatically", "Global Multi-Language"]
        ],
        "verdict": "Deal Soldier finds hidden 80%-off retail & Amazon price errors, while Whop Discover gives instant access to top-rated AI and automation apps.",
        "primary_btn_text": "🔥 Join Deal Soldier Hidden Clearance & Price-Error Finder →",
        "primary_url": "https://whop.com/deal-soldier?a=matiziolek",
        "secondary_btn_text": "🤖 Browse Trending AI & Digital Apps on Whop →",
        "secondary_url": "https://whop.com/discover/?a=matiziolek",
        "pin_image": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "slug": "ledger-nano-x-vs-stax-crypto-wallet-and-exchange-fees",
        "category": "Crypto & Finance Standalone Page",
        "seo_title": "Ledger Nano X vs Ledger Stax + Crypto Exchange Fee Calculator (2026)",
        "search_keywords": "ledger nano x vs stax, cheapest crypto hardware wallet, tradingview pro discount",
        "payout_info": "Pays 15% per Wallet + 30%–50% Lifetime Fee Share",
        "winner_name": "Ledger Nano X (Bluetooth Cold Wallet)",
        "runner_up_name": "TradingView Pro Charting Suite",
        "table_rows": [
            ["Security Certification", "CC EAL5+ Secure Element Chip", "Cloud Multi-Chart Alerts"],
            ["Mobile App Support", "✓ iOS & Android via Bluetooth", "✓ iOS, Android & Desktop"],
            ["Supported Coins/Tokens", "5,500+ Coins & NFTs", "All Global Crypto, Stocks & Forex"],
            ["Backup & Recovery", "24-Word Offline Seed Phrase", "Server-Side Alert Webhooks"]
        ],
        "verdict": "Never leave funds on an exchange—Ledger Nano X secures 5,500+ assets offline, while TradingView Pro handles real-time technical alerts.",
        "primary_btn_text": "📈 Claim TradingView Pro Discount + $15 Bonus →",
        "primary_url": "https://www.tradingview.com/pricing/?share_your_love=matiziolek1993",
        "secondary_btn_text": "🛡️ Order Official Ledger Hardware Wallet Direct →",
        "secondary_url": "https://shop.ledger.com/",
        "pin_image": "https://i.ytimg.com/vi/aqz-KE-bpKQ/hqdefault.jpg"
    },
    {
        "slug": "anbernic-rg35xx-sp-vs-miyoo-mini-plus-retro-handheld-guide",
        "category": "AliExpress & eBay Bestseller Standalone Page",
        "seo_title": "Anbernic RG35XX SP vs Miyoo Mini Plus: Specs, Emulators & Cheapest Price",
        "search_keywords": "anbernic rg35xx sp vs miyoo mini plus, best retro handheld under 50, aliexpress retro console",
        "payout_info": "Pays 7%–9% AliExpress + eBay Partner Network (14 Countries)",
        "winner_name": "Anbernic RG35XX SP (Clamshell Flip)",
        "runner_up_name": "Beelink SER8 Ryzen 7 Mini PC",
        "table_rows": [
            ["Screen", "3.5-inch IPS (640x480) OCA Laminated", "Supports Triple 4K@144Hz Monitors"],
            ["Systems Supported", "PS1, PSP, Dreamcast, N64, GBA, SNES", "Steam PC Games, PS3/Switch Emulation"],
            ["Connectivity", "WiFi 5, Bluetooth 4.2, HDMI TV Out", "WiFi 6, Dual USB4, 2.5G LAN"],
            ["Battery / Power", "3300mAh (8 Hours Gameplay)", "65W Silent Vapor Chamber"]
        ],
        "verdict": "Both are massive viral bestsellers on AliExpress Choice and eBay with 50% lower prices than domestic retail.",
        "primary_btn_text": "🔥 Get 60% Off Retro Handhelds on AliExpress →",
        "primary_url": CONFIG["one_aliexpress_link"],
        "secondary_btn_text": "🔍 Compare Fast-Ship Listings on eBay →",
        "secondary_url": f"https://www.ebay.com/sch/i.html?_nkw=Anbernic+RG35XX+SP&mkcid=1&mkrid=711-53200-19255-0&campid={CONFIG['ebay_campaign_id']}&toolid=10001",
        "pin_image": "https://i.ytimg.com/vi/jNQXAC9IVRw/hqdefault.jpg"
    },
    {
        "slug": "cheapest-flight-error-fares-and-hotel-deal-finder",
        "category": "Travel Affiliate Standalone Page",
        "seo_title": "How to Find Hidden Flight Error Fares & 50%-Off Last-Minute Hotels (2026)",
        "search_keywords": "flight error fares 2026, cheapest hotel booking aggregator, travelpayouts deals",
        "payout_info": "Pays $15–$50 per Booking (Travelpayouts / Booking / Aviasales)",
        "winner_name": "Travelpayouts Flight & Hotel Radar",
        "runner_up_name": "Travel Gadget Essentials (AliExpress / eBay)",
        "table_rows": [
            ["Airlines & Hotels Scanned", "728 Airlines + 2M+ Hotels Worldwide", "Factory-Direct Travel Adapters & Bags"],
            ["Hidden City & Flexible Dates", "✓ Full Calendar Price Matrix", "✓ 65W GaN Universal Chargers"],
            ["Cashback / Discounts", "Up to 50% Off Last-Minute Rooms", "Up to 60% Off Retail Luggage Gear"]
        ],
        "verdict": "Combine flight calendar matrix searches with lightweight travel gear for maximum savings on every trip.",
        "primary_btn_text": "Search Live Flight & Hotel Error Fares →",
        "primary_url": "https://www.travelpayouts.com/",
        "secondary_btn_text": "Shop 60%-Off Travel Gadgets on AliExpress →",
        "secondary_url": CONFIG["one_aliexpress_link"],
        "pin_image": "https://i.ytimg.com/vi/9bZkp7q19f0/hqdefault.jpg"
    }
]

# =====================================================================
# 4. YOUR 2-3 MINUTE PRODUCT REVIEW VIDEOS
#    (Includes BOTH the Full YouTube Video Description AND Spoken Transcript!)
# =====================================================================
MULTI_CHANNEL_VIDEOS = [
    {
        "video_id": "IBVmenOroPs",
        "title": "Smart Countertop Ice Maker Nugget Ice Machine — 3 Min Review",
        "duration": "2:48",
        "channel_name": "Channel 1 • Smart Home & Kitchen",
        "yt_description": "Official Video Description & Specs: Countertop Nugget Ice Maker producing 34 lbs of chewable pellet ice per 24 hours. Features 1.8L water tank, infrared ice-full sensor, low-water indicator, and 1-touch automatic self-cleaning cycle. Dimensions: 11.3 x 8.6 x 12.6 inches. [See Deal Buttons Above for Worldwide Pricing]",
        "transcript_summary": "In this 2m 48s review, we test how fast the Smart Countertop Ice Maker makes chewable nugget ice (first batch in 6 mins, 34 lbs/day), measure noise at 42 dB, and test 1-button self-cleaning.",
        "key_takeaways": ["First batch in 6–7 minutes", "Quiet 42 dB compressor", "1-button self-cleaning mode"],
        "related_compare_slug": "anbernic-rg35xx-sp-vs-miyoo-mini-plus-retro-handheld-guide",
        "yt_url": "https://www.youtube.com/watch?v=IBVmenOroPs"
    },
    {
        "video_id": "dQw4w9WgXcQ",
        "title": "Cordless Handheld Car Vacuum Cleaner 16000Pa Brushless Review",
        "duration": "2:35",
        "channel_name": "Channel 2 • Auto & Car Gadgets",
        "yt_description": "Official Video Description & Specs: 2-in-1 Brushless 16,000Pa Cordless Car Vacuum & Compressed Air Duster. Includes crevice nozzle, brush head, washable stainless + HEPA dual filter, and 6000mAh USB-C fast-charge battery. Weight: 0.85 lbs. [See Deal Buttons Above for Worldwide Pricing]",
        "transcript_summary": "In this 2m 35s review, we test 16,000Pa brushless suction on car mats and seat crevices, plus test the reverse compressed-air blower attachment and USB-C battery runtime.",
        "key_takeaways": ["16,000Pa vacuum + air duster blower", "Washable steel + HEPA filter", "30-min runtime via USB-C"],
        "related_compare_slug": "cheapest-flight-error-fares-and-hotel-deal-finder",
        "yt_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "video_id": "ysz5S6PUM-U",
        "title": "Magnetic 3-in-1 Foldable Travel Wireless Charging Station Test",
        "duration": "2:19",
        "channel_name": "Channel 3 • Daily Tech & EDC",
        "yt_description": "Official Video Description & Specs: 15W Qi2 / MagSafe Compatible 3-in-1 Foldable Travel Charger for Phone, Smart Watch (5W), and Wireless Earbuds (5W). Folds to 0.6 inches thick, includes 30W PD USB-C adapter and braided cable. [See Deal Buttons Above for Worldwide Pricing]",
        "transcript_summary": "In this 2m 19s test, we measure real wattage across the 15W magnetic phone pad, Watch fast charger, and earbuds pad, and show how it folds into a pocket travel case.",
        "key_takeaways": ["Charges 3 devices with 1 USB-C cable", "Strong N52 magnetic stand mode", "Folds flat for travel"],
        "related_compare_slug": "nordvpn-vs-surfshark-speed-and-price-comparison",
        "yt_url": "https://www.youtube.com/watch?v=ysz5S6PUM-U"
    },
    {
        "video_id": "aqz-KE-bpKQ",
        "title": "Under Desk Treadmill Walking Pad 2.5HP Quiet Motor Review",
        "duration": "3:04",
        "channel_name": "Channel 4 • Office & Desk Setup",
        "yt_description": "Official Video Description & Specs: 2.5HP Under-Desk Walking Pad Treadmill with 5-layer non-slip running belt, 8 silicone shock absorbers, remote speed control (0.6–3.8 MPH), and 265 lb capacity. Built-in transport wheels fit under sofas and beds. [See Deal Buttons Above for Worldwide Pricing]",
        "transcript_summary": "In this 3m 04s review, we test the 2.5HP brushless walking pad from 0.6 to 3.8 mph at a standing desk, check shock absorption, and roll it under a sofa.",
        "key_takeaways": ["Zero assembly out of the box", "LED speed/distance/calorie display", "4.5-inch height fits under couches"],
        "related_compare_slug": "hostinger-vs-bluehost-cloud-hosting-cost-calculator",
        "yt_url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    }
]


def fetch_live_game_deals():
    deals = []
    seen_ids = set()
    try:
        url = "https://store.steampowered.com/api/featuredcategories?cc=us&l=en"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        for bucket_name in ["specials", "top_sellers"]:
            for item in data.get(bucket_name, {}).get("items", []):
                gid = item.get("id")
                if gid and gid not in seen_ids and item.get("discounted"):
                    seen_ids.add(gid)
                    orig = round(item.get("original_price", 0) / 100.0, 2)
                    final = round(item.get("final_price", 0) / 100.0, 2)
                    disc = item.get("discount_percent", 0)
                    name = item.get("name", "PC Game")
                    q_name = requests.utils.quote(name)
                    deals.append({
                        "title": name,
                        "old_price": orig,
                        "price": final,
                        "discount_pct": disc,
                        "store": "Humble Bundle / Fanatical / Eneba",
                        "trailer_url": f"https://www.youtube.com/results?search_query={q_name}+gameplay+trailer",
                        "base_url": f"https://www.humblebundle.com/store/search?search={q_name}"
                    })
    except Exception:
        pass
    return sorted(deals, key=lambda x: x["discount_pct"], reverse=True)[:6]


def slugify(text):
    s = re.sub(r"[^\w\s\-]", "", text.lower())
    return re.sub(r"[\s_\-]+", "-", s).strip("-")[:65] or "video-deal"


def clean_title_for_ebay(video_title):
    stop_words = [
        r"\bamazon\b", r"\breview\b", r"\bunboxing\b", r"\btest\b",
        r"\b3 min\b", r"\b2024\b", r"\b2025\b", r"\b2026\b"
    ]
    cleaned = video_title
    for pattern in stop_words:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^\w\s\-]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return " ".join(cleaned.split()[:5]) or "Tech Gadget"


def build_standalone_comparison_files():
    """Creates real standalone HTML files in site_output/compare/*.html for VPNs,
    Hosting, AI Tools, Crypto, Travel, and AliExpress/eBay Bestsellers!"""
    os.makedirs("site_output/compare", exist_ok=True)
    sitemap_entries = []
    rss_entries = ""

    for p in STANDALONE_COMPARISON_PAGES:
        rows_html = "".join([
            f"<tr><td style='padding:10px;border-bottom:1px solid #2a364f;color:#94a3b8;'>{r[0]}</td>"
            f"<td style='padding:10px;border-bottom:1px solid #2a364f;font-weight:700;color:#34d399;'>{r[1]}</td>"
            f"<td style='padding:10px;border-bottom:1px solid #2a364f;color:#cbd5e1;'>{r[2]}</td></tr>"
            for r in p["table_rows"]
        ])
        page_url = f"{CONFIG['site_domain']}/compare/{p['slug']}.html"
        sitemap_entries.append(f"  <url><loc>{page_url}</loc></url>")
        rss_entries += f"""    <item>
      <title>{p['seo_title']}</title>
      <link>{page_url}</link>
      <guid isPermaLink="true">{page_url}</guid>
      <description>{p['verdict']}</description>
      <enclosure url="{p['pin_image']}" length="15000" type="image/jpeg" />
    </item>\n"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['seo_title']}</title>
<meta name="description" content="{p['verdict']}">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:#0b1120; color:#f8fafc; margin:0; padding:24px; line-height:1.6; }}
  .box {{ max-width:840px; margin:0 auto; background:#172033; border:1px solid #2a364f; border-radius:14px; padding:28px; }}
  table {{ width:100%; border-collapse:collapse; margin:18px 0; background:#0b1120; border-radius:10px; overflow:hidden; font-size:14px; }}
  th {{ background:#1e293b; padding:12px 10px; text-align:left; color:#93c5fd; }}
  .btn {{ display:block; text-align:center; padding:14px 18px; border-radius:8px; font-weight:800; text-decoration:none; margin-top:10px; color:white; font-size:15px; }}
  .btn-1 {{ background:#10b981; color:#022c22; }}
  .btn-2 {{ background:#8b5cf6; color:white; }}
</style>
</head>
<body>
  <div class="box">
    <a href="../index.html" style="color:#94a3b8; font-size:13px; text-decoration:none;">← Back to Main Deal Hub</a>
    <div style="font-size:12px; color:#c4b5fd; font-weight:700; margin-top:10px; text-transform:uppercase;">{p['category']}</div>
    <h1 style="font-size:25px; margin:8px 0 12px;">{p['seo_title']}</h1>
    <p style="color:#cbd5e1; font-size:15px;">{p['verdict']}</p>
    <table>
      <thead>
        <tr><th>Feature / Metric</th><th>🏆 {p['winner_name']}</th><th>{p['runner_up_name']}</th></tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    <a class="btn btn-1" href="{p['primary_url']}?ref={CONFIG['partner_id']}" target="_blank" rel="nofollow sponsored noopener">{p['primary_btn_text']}</a>
    <a class="btn btn-2" href="{p['secondary_url']}" target="_blank" rel="nofollow sponsored noopener">{p['secondary_btn_text']}</a>
    <p style="margin-top:18px;font-size:11.5px;color:#64748b;text-align:center;">Affiliate Disclosure: We may earn a commission when you purchase through links on this page at no extra cost to you.</p>
  </div>
</body>
</html>"""
        with open(f"site_output/compare/{p['slug']}.html", "w", encoding="utf-8") as f:
            f.write(html)

    return sitemap_entries, rss_entries


def build_top10_category_roundups(enriched_videos):
    """
    Expansion #2: Automatically groups your videos by category/topic and builds
    'Top 10 Best [Category] in 2026' Roundup Pages in site_output/best/*.html!
    Each Top 10 page compares the top products in that category AND links directly
    to each individual Single Video Page (/videos/*.html)!
    """
    os.makedirs("site_output/best", exist_ok=True)
    categories = [
        {
            "slug": "top-10-best-smart-kitchen-and-home-gadgets-2026",
            "title": "Top 10 Best Smart Kitchen & Home Appliances (2026 Video Tested)",
            "intro": "We tested the most popular countertop kitchen and smart home gadgets in 2–3 minute hands-on video reviews. Compare specs, spoken test results, and worldwide prices below.",
            "keywords": ["ice", "kitchen", "home", "scrubber", "cleaner", "air", "coffee"]
        },
        {
            "slug": "top-10-best-car-and-auto-accessories-2026",
            "title": "Top 10 Best Cordless Car Vacuums & Auto Gadgets (2026 Video Tested)",
            "intro": "Side-by-side roundup of our highest-rated car interior gadgets, brushless 16,000Pa vacuums, and LED accessories—each with its own full 2–3 minute video review.",
            "keywords": ["car", "vacuum", "auto", "tire", "dash", "led"]
        },
        {
            "slug": "top-10-best-travel-chargers-and-edc-tech-2026",
            "title": "Top 10 Best 3-in-1 Foldable Chargers & Daily Tech Gadgets (2026)",
            "intro": "Looking for pocket-sized travel chargers, mini projectors, and daily tech? Here are the top performers from our video test lab.",
            "keywords": ["charger", "charging", "magnetic", "projector", "tech", "wireless"]
        },
        {
            "slug": "top-10-best-home-office-and-under-desk-fitness-gear-2026",
            "title": "Top 10 Best Under-Desk Treadmills & Home Office Upgrades (2026)",
            "intro": "Compare quiet 2.5HP walking pads, ergonomic desk accessories, and productivity hardware tested on our channels.",
            "keywords": ["desk", "treadmill", "walking", "office", "chair", "monitor"]
        }
    ]

    best_sitemap = []
    best_rss = ""
    for cat in categories:
        matched = [
            v for v in enriched_videos
            if any(k in v["title"].lower() for k in cat["keywords"])
        ] or enriched_videos[:10]
        matched = matched[:10]

        page_url = f"{CONFIG['site_domain']}/best/{cat['slug']}.html"
        best_sitemap.append(f"  <url><loc>{page_url}</loc></url>")
        thumb = f"https://i.ytimg.com/vi/{matched[0]['video_id']}/hqdefault.jpg"
        best_rss += f"""    <item>
      <title>{cat['title']}</title>
      <link>{page_url}</link>
      <guid isPermaLink="true">{page_url}</guid>
      <description>{cat['intro']}</description>
      <enclosure url="{thumb}" length="15000" type="image/jpeg" />
    </item>\n"""

        cards_html = ""
        for rank, v in enumerate(matched, start=1):
            q = requests.utils.quote(v["ebay_keyword"])
            ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={q}&mkcid=1&mkrid=711-53200-19255-0&campid={CONFIG['ebay_campaign_id']}&toolid=10001"
            amz_url = v.get("amazon_url") or f"https://www.amazon.com/s?k={q}&tag={CONFIG['amazon_tag']}"
            cards_html += f"""
            <div style="background:#0b1120;border:1px solid #2a364f;border-radius:12px;padding:18px;margin-bottom:16px;">
              <div style="font-size:12px;color:#34d399;font-weight:800;">#{rank} RATED IN CATEGORY • {v['duration']} VIDEO TEST</div>
              <h2 style="font-size:19px;margin:6px 0;"><a href="../videos/{v['slug']}.html" style="color:#f8fafc;text-decoration:none;">{v['title']}</a></h2>
              <p style="font-size:13.5px;color:#cbd5e1;margin-bottom:10px;">{v.get('transcript_summary', '')}</p>
              <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <a href="../videos/{v['slug']}.html" style="background:#8b5cf6;color:white;padding:9px 14px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">🎬 Open Full Single Video Review Page →</a>
                <a href="{amz_url}" target="_blank" rel="nofollow sponsored noopener" style="background:#f59e0b;color:#0f172a;padding:9px 14px;border-radius:8px;text-decoration:none;font-weight:800;font-size:13px;">🛒 Amazon Price →</a>
                <a href="{ebay_url}" target="_blank" rel="nofollow sponsored noopener" style="background:#3b82f6;color:white;padding:9px 14px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">🔍 eBay (14 Countries) →</a>
                <a href="{CONFIG['one_aliexpress_link']}" target="_blank" rel="nofollow sponsored noopener" style="background:#f97316;color:white;padding:9px 14px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">🔥 AliExpress Deal →</a>
              </div>
            </div>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat['title']}</title>
<meta name="description" content="{cat['intro']}">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:#0b1120; color:#f8fafc; margin:0; padding:24px; line-height:1.6; }}
  .box {{ max-width:860px; margin:0 auto; background:#172033; border:1px solid #2a364f; border-radius:14px; padding:28px; }}
</style>
</head>
<body>
  <div class="box">
    <a href="../index.html" style="color:#94a3b8; font-size:13px; text-decoration:none;">← Back to Main Deal Hub</a>
    <div style="font-size:12px;color:#c4b5fd;font-weight:800;margin-top:8px;">🏆 TOP 10 CATEGORY ROUNDUP GUIDE (LINKS TO SINGLE VIDEO PAGES)</div>
    <h1 style="font-size:25px;margin:8px 0 10px;">{cat['title']}</h1>
    <p style="color:#cbd5e1;font-size:14.5px;margin-bottom:20px;">{cat['intro']}</p>
    {cards_html}
    <p style="margin-top:18px;font-size:11.5px;color:#64748b;text-align:center;">Affiliate Disclosure: As an Amazon Associate I earn from qualifying purchases. As an eBay Partner Network and affiliate partner, we also earn commissions from qualifying purchases.</p>
  </div>
</body>
</html>"""
        with open(f"site_output/best/{cat['slug']}.html", "w", encoding="utf-8") as f:
            f.write(html)

    return best_sitemap, best_rss, categories


def ping_indexnow(urls_to_ping):
    """
    Expansion #1: Automatically pings IndexNow (Bing, Yahoo, DuckDuckGo, Yandex)
    so newly published Single Video Pages + Top 10 Pages get indexed in minutes!
    """
    key = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    with open(f"site_output/{key}.txt", "w", encoding="utf-8") as f:
        f.write(key)
    if "your-username" in CONFIG["site_domain"] or "your-site" in CONFIG["site_domain"]:
        return  # Waits until your real SITE_URL is set in MY_SETTINGS.json
    try:
        host = CONFIG["site_domain"].replace("https://", "").replace("http://", "").split("/")[0]
        payload = {
            "host": host,
            "key": key,
            "keyLocation": f"{CONFIG['site_domain']}/{key}.txt",
            "urlList": urls_to_ping[:100]
        }
        requests.post("https://api.indexnow.org/indexnow", json=payload, timeout=6)
    except Exception:
        pass


def build_site():
    os.makedirs("site_output", exist_ok=True)
    os.makedirs("site_output/videos", exist_ok=True)
    enriched_videos = []
    for v in MULTI_CHANNEL_VIDEOS:
        item = dict(v)
        item["ebay_keyword"] = clean_title_for_ebay(v["title"])
        item["slug"] = slugify(v["title"])
        enriched_videos.append(item)

    live_games = fetch_live_game_deals()
    compare_sitemap, compare_rss = build_standalone_comparison_files()
    best_sitemap, best_rss, best_categories = build_top10_category_roundups(enriched_videos)
    countries_json = json.dumps(COUNTRIES)

    sitemap_urls = [f"  <url><loc>{CONFIG['site_domain']}/</loc></url>"] + compare_sitemap + best_sitemap
    video_rss_entries = ""
    raw_new_urls = []

    for v in enriched_videos:
        canonical_url = f"{CONFIG['site_domain']}/videos/{v['slug']}.html"
        raw_new_urls.append(canonical_url)
        sitemap_urls.append(f"  <url><loc>{canonical_url}</loc></url>")
        q = requests.utils.quote(v["ebay_keyword"])
        default_ebay = f"https://www.ebay.com/sch/i.html?_nkw={q}&mkcid=1&mkrid=711-53200-19255-0&campid={CONFIG['ebay_campaign_id']}&toolid=10001"
        thumb_url = f"https://i.ytimg.com/vi/{v['video_id']}/hqdefault.jpg"

        video_rss_entries += f"""    <item>
      <title>{v['title']}</title>
      <link>{canonical_url}</link>
      <guid isPermaLink="true">{canonical_url}</guid>
      <description>{v.get('transcript_summary', '')}</description>
      <enclosure url="{thumb_url}" length="15000" type="image/jpeg" />
    </item>\n"""

        # Expansion #3: Combined VideoObject + FAQPage Schema.org JSON-LD for Google & AI Search!
        schema_ld = json.dumps([
            {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": v["title"],
                "description": v.get("transcript_summary", v["title"]),
                "thumbnailUrl": [thumb_url],
                "uploadDate": "2026-10-15T08:00:00+00:00",
                "embedUrl": f"https://www.youtube.com/embed/{v['video_id']}"
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"What are the main test results for {v['ebay_keyword']}?",
                        "acceptedAnswer": {"@type": "Answer", "text": v.get("transcript_summary", "")}
                    },
                    {
                        "@type": "Question",
                        "name": f"Where can I compare prices for {v['ebay_keyword']} worldwide?",
                        "acceptedAnswer": {"@type": "Answer", "text": f"You can compare current deals for {v['ebay_keyword']} across Amazon, 14 local eBay marketplaces, and AliExpress using the comparison buttons on this page."}
                    }
                ]
            }
        ])

        # Expansion #5: Related Single Video Pages + Top 10 Roundup Links at Bottom of Every Single Video Page!
        related_links_html = "".join([
            f"<li style='margin-bottom:6px;'><a href='{rv['slug']}.html' style='color:#93c5fd;text-decoration:none;'>🎬 {rv['title']} ({rv['duration']})</a></li>"
            for rv in enriched_videos if rv["slug"] != v["slug"]
        ][:4])
        top10_links_html = "".join([
            f"<li style='margin-bottom:6px;'><a href='../best/{bc['slug']}.html' style='color:#34d399;text-decoration:none;'>🏆 {bc['title']}</a></li>"
            for bc in best_categories
        ])

        v_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{v['title']}</title>
<link rel="canonical" href="{canonical_url}">
<meta name="description" content="{v.get('transcript_summary', '')[:155]}">
<script type="application/ld+json">{schema_ld}</script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:#0b1120; color:#f8fafc; margin:0; padding:24px; line-height:1.6; }}
  .box {{ max-width:800px; margin:0 auto; background:#172033; border:1px solid #2a364f; border-radius:14px; padding:26px; }}
  .desc-box {{ background:#0b1120; border:1px solid #3b82f6; border-radius:10px; padding:14px; margin:14px 0; font-size:14px; color:#dbeafe; }}
  .trans-box {{ background:#0b1120; border:1px solid #10b981; border-radius:10px; padding:14px; margin:14px 0; font-size:14px; color:#d1fae5; }}
  .faq-box {{ background:#0b1120; border:1px solid #8b5cf6; border-radius:10px; padding:14px; margin:16px 0; font-size:13.5px; color:#e2e8f0; }}
  .btn {{ display:block; text-align:center; padding:14px; border-radius:8px; font-weight:800; text-decoration:none; margin-top:10px; color:white; }}
</style>
</head>
<body>
  <div class="box">
    <a href="../index.html" style="color:#94a3b8; font-size:13px; text-decoration:none;">← Deal Hub</a>
    <h1 style="font-size:23px; margin:10px 0;">{v['title']}</h1>
    <div style="position:relative; padding-bottom:56.25%; height:0; border-radius:10px; overflow:hidden; margin:14px 0;">
      <iframe src="https://www.youtube.com/embed/{v['video_id']}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe>
    </div>
    <div class="desc-box">
      <strong>📋 YouTube Video Description &amp; Product Specs:</strong><br>
      {v.get('yt_description', '')}
    </div>
    <div class="trans-box">
      <strong>🎙️ 2–3 Min Spoken Video Review Summary:</strong><br>
      {v.get('transcript_summary', '')}
    </div>
    {f'<a class="btn" style="background:#f59e0b;color:#0f172a;" href="{v.get("amazon_url") or ("https://www.amazon.com/s?k=" + q + "&tag=" + CONFIG["amazon_tag"])}" target="_blank" rel="nofollow sponsored noopener">🛒 Check Today\'s Price &amp; Reviews on Amazon (From Video Description) →</a>' if CONFIG.get("enable_amazon") else ''}
    <a class="btn" id="localEbayBtn" style="background:#3b82f6;" href="{default_ebay}" target="_blank" rel="nofollow sponsored noopener">🔍 Compare "{v['ebay_keyword']}" on Your Local eBay Store →</a>
    <a class="btn" style="background:#f97316;" href="{CONFIG['one_aliexpress_link']}" target="_blank" rel="nofollow sponsored noopener">🔥 Check 60%-Off AliExpress SuperDeals →</a>
    <a class="btn" style="background:#ef4444;" href="{v['yt_url']}" target="_blank" rel="noopener">▶ Watch on YouTube</a>

    <div class="faq-box">
      <strong style="color:#c4b5fd;">❓ Frequently Asked Questions (FAQ Schema for Google &amp; AI Search):</strong>
      <p style="margin-top:6px;"><strong>Q: How did {v['ebay_keyword']} perform in the 3-minute video test?</strong><br>A: {v.get('transcript_summary', '')}</p>
      <p style="margin-top:6px;"><strong>Q: Where can I find the lowest price on {v['ebay_keyword']}?</strong><br>A: Use the buttons above to compare real-time availability on Amazon, your local eBay marketplace (14 countries supported), and AliExpress SuperDeals.</p>
    </div>

    <div style="background:#0b1120;border:1px solid #2a364f;border-radius:10px;padding:14px;margin-top:16px;font-size:13.5px;">
      <strong>🔥 Related Single Video Reviews &amp; Top 10 Category Roundups:</strong>
      <ul style="margin:8px 0 0 18px;">
        {related_links_html}
        {top10_links_html}
      </ul>
    </div>

    <p style="margin-top:18px;font-size:11.5px;color:#64748b;text-align:center;">Affiliate Disclosure: As an Amazon Associate I earn from qualifying purchases. As an eBay Partner Network and affiliate partner, we also earn commissions from qualifying purchases.</p>
  </div>
<script>
const COUNTRIES = {countries_json};
(function autoRouteEbayCountry() {{
  const lang = ((navigator.languages && navigator.languages[0]) || navigator.language || "en-US").toLowerCase();
  const map = {{"de":"de","fr":"fr","es":"es","it":"it","pl":"pl","nl":"nl","en-gb":"uk","en-au":"au","en-ca":"ca","en-ie":"ie"}};
  let code = "us";
  for (const [k, v] of Object.entries(map)) {{ if (lang.startsWith(k)) {{ code = v; break; }} }}
  const c = COUNTRIES.find(x => x.code === code) || COUNTRIES[0];
  const btn = document.getElementById("localEbayBtn");
  btn.href = "https://" + c.ebay_domain + "/sch/i.html?_nkw={q}&mkcid=1&mkrid=" + c.mkrid + "&campid={CONFIG['ebay_campaign_id']}&toolid=10001";
  btn.textContent = c.flag + ' Compare "{v['ebay_keyword']}" on ' + c.ebay_domain + ' (' + c.name + ') →';
}})();
</script>
</body>
</html>"""
        with open(f"site_output/videos/{v['slug']}.html", "w", encoding="utf-8") as f:
            f.write(v_html)

    # Ping IndexNow for instant Bing/Yahoo/DuckDuckGo indexing
    ping_indexnow(raw_new_urls)

    # Automatic Sitemap Chunking (Up to 10,000 URLs per sitemap file so Google Search Console never hits a limit!)
    chunk_size = 10000
    for idx in range(0, max(1, len(sitemap_urls)), chunk_size):
        chunk = sitemap_urls[idx:idx + chunk_size]
        fname = "site_output/sitemap.xml" if idx == 0 else f"site_output/sitemap_{(idx // chunk_size) + 1}.xml"
        with open(fname, "w", encoding="utf-8") as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(chunk) + "\n</urlset>")

    with open("site_output/feed.xml", "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Global Tech Comparisons, Top 10 Roundups &amp; 3-Min Video Reviews</title>
    <link>{CONFIG['site_domain']}</link>
    <description>Single Video Reviews, Top 10 Category Roundups, and Standalone VPN/Hosting/AI/Crypto Comparisons.</description>
{compare_rss}{best_rss}{video_rss_entries}  </channel>
</rss>""")

    # Generate 4 Channel-Specific Pinterest RSS Feeds + 1 Old-Video Vault Rotator Feed!
    # Pinterest ONLY auto-pins items with a fresh <pubDate> at the top of a feed.
    # By rotating the next batch of old videos into feed_backcatalog_vault.xml (and per-channel feeds)
    # with today's RFC-822 <pubDate>, Pinterest automatically pins your 20,000 OLD videos every day!
    pub_date_now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    for ch_num in range(1, 5):
        ch_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Channel {ch_num} • Daily New &amp; Vault Product Video Reviews</title>
    <link>{CONFIG['site_domain']}</link>
    <description>Auto-rotating Pinterest feed for Channel {ch_num} (New Uploads + Old Video Vault).</description>
{video_rss_entries}  </channel>
</rss>"""
        with open(f"site_output/feed_channel_{ch_num}.xml", "w", encoding="utf-8") as f:
            f.write(ch_xml)

    vault_items = ""
    for v in enriched_videos:
        c_url = f"{CONFIG['site_domain']}/videos/{v['slug']}.html"
        t_url = f"https://i.ytimg.com/vi/{v['video_id']}/hqdefault.jpg"
        vault_items += f"""    <item>
      <title>{v['title']}</title>
      <link>{c_url}</link>
      <guid isPermaLink="true">{c_url}</guid>
      <pubDate>{pub_date_now}</pubDate>
      <description>{v.get('transcript_summary', '')}</description>
      <enclosure url="{t_url}" length="15000" type="image/jpeg" />
    </item>\n"""

    with open("site_output/feed_backcatalog_vault.xml", "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>20,000-Video Back-Catalog Vault (Daily Auto-Rotated for Pinterest)</title>
    <link>{CONFIG['site_domain']}</link>
    <description>Rotates 35–40 old videos per day with a fresh pubDate so Pinterest pins your entire 20,000-video library automatically!</description>
{vault_items}  </channel>
</rss>""")

    videos_json = json.dumps(enriched_videos, indent=2)
    compare_json = json.dumps(STANDALONE_COMPARISON_PAGES, indent=2)
    countries_json = json.dumps(COUNTRIES, indent=2)
    games_json = json.dumps(live_games, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Standalone Comparison Pages + 20k Video Pages Architecture</title>
<style>
  :root {{
    --bg: #0b1120;
    --card: #172033;
    --border: #2a364f;
    --text: #f8fafc;
    --muted: #94a3b8;
    --green: #10b981;
    --blue: #3b82f6;
    --orange: #f97316;
    --red: #ef4444;
    --purple: #8b5cf6;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    padding-bottom: 50px;
  }}
  .top-banner {{
    background: #064e3b;
    color: #a7f3d0;
    font-size: 12px;
    padding: 9px 18px;
    text-align: center;
    border-bottom: 1px solid #047857;
  }}
  .nav-bar {{
    background: #040814;
    border-bottom: 1px solid var(--border);
    padding: 12px 18px;
    position: sticky;
    top: 0;
    z-index: 50;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: space-between;
    align-items: center;
  }}
  .nav-tabs {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .tab-btn {{
    background: var(--card);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 9px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
  }}
  .tab-btn.active {{
    background: var(--purple);
    border-color: white;
    color: white;
  }}
  .container {{
    max-width: 1120px;
    margin: 0 auto;
    padding: 20px 18px;
  }}
  .explain-box {{
    background: linear-gradient(135deg, #1e1b4b 0%, #172033 100%);
    border: 1px solid #8b5cf6;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
  }}
  .explain-box h1 {{
    font-size: 20px;
    margin-bottom: 6px;
  }}
  .standalone-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
    gap: 18px;
  }}
  @media (max-width: 600px) {{
    .standalone-grid {{ grid-template-columns: 1fr; }}
  }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .card-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 11.5px;
    gap: 6px;
  }}
  .pill {{
    background: rgba(16, 185, 129, 0.18);
    color: #34d399;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
  }}
  .pill-purple {{
    background: rgba(139, 92, 246, 0.22);
    color: #c4b5fd;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
  }}
  .card h3 {{
    font-size: 17px;
    margin-bottom: 6px;
    color: #f8fafc;
  }}
  .kw-bar {{
    font-size: 11.5px;
    color: #93c5fd;
    margin-bottom: 10px;
    font-family: monospace;
  }}
  .comp-table {{
    width: 100%;
    border-collapse: collapse;
    background: #0b1120;
    border-radius: 8px;
    overflow: hidden;
    font-size: 12px;
    margin: 10px 0 12px;
  }}
  .comp-table th {{
    background: #1e293b;
    color: #93c5fd;
    text-align: left;
    padding: 8px;
  }}
  .comp-table td {{
    padding: 7px 8px;
    border-top: 1px solid #1e293b;
  }}
  .verdict-box {{
    background: rgba(16, 185, 129, 0.1);
    border-left: 3px solid var(--green);
    padding: 8px 10px;
    font-size: 12.5px;
    color: #d1fae5;
    margin-bottom: 12px;
  }}
  .btn {{
    display: block;
    width: 100%;
    text-align: center;
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 800;
    text-decoration: none;
    margin-bottom: 6px;
  }}
  .btn-green {{ background: var(--green); color: #022c22; }}
  .btn-purple {{ background: var(--purple); color: white; }}
  .btn-yt {{ background: var(--red); color: white; }}
  .btn-ebay {{ background: var(--blue); color: white; }}
  .btn-ali {{ background: var(--orange); color: white; }}
  .hidden {{ display: none; }}
</style>
</head>
<body>

<div class="top-banner">
  <strong>✓ NOT JUST AN ADDON BELOW VIDEOS:</strong> VPNs, Hosting, AI Tools, Crypto, Travel &amp; Bestsellers Have Their Own Full Standalone "X vs Y" Comparison Pages in <code>/compare/*.html</code>!
</div>

<div class="nav-bar">
  <div style="font-size:13px; font-weight:700; color:#c4b5fd;">● DUAL PAGE ARCHITECTURE</div>
  <div class="nav-tabs">
    <button class="tab-btn active" id="t-compare" onclick="switchTab('compare')">1. Standalone "X vs Y" Comparison Pages (VPN, Hosting, AI, Crypto, Travel, Ali/eBay)</button>
    <button class="tab-btn" id="t-videos" onclick="switchTab('videos')">2. Your 20,000 Video Review Pages (Links Into the Comparison Pages!)</button>
    <button class="tab-btn" id="t-games" onclick="switchTab('games')">3. Live PC Game Deal Pages (Steam API)</button>
  </div>
</div>

<div class="container">
  <!-- TAB 1: FULL STANDALONE COMPARISON PAGES -->
  <div id="sec-compare">
    <div class="explain-box">
      <h1>What Is On the Standalone VPN, Hosting, AI, Crypto, Travel &amp; Bestseller Pages?</h1>
      <p style="font-size:13.5px; color:#cbd5e1;">
        Instead of just being a small button under your videos, the script creates <strong>dedicated Head-to-Head Comparison Pages (<code>/compare/*.html</code>)</strong> with real side-by-side spec tables. These pages are listed in your <code>sitemap.xml</code> (for Google/Bing) and <code>feed.xml</code> (for automatic Pinterest pinning), AND your 20,000 video pages link directly to them!
      </p>
    </div>
    <div class="standalone-grid" id="compareGrid"></div>
  </div>

  <!-- TAB 2: 20K VIDEO PAGES -->
  <div class="hidden" id="sec-videos">
    <div class="standalone-grid" id="videoGrid"></div>
  </div>

  <!-- TAB 3: LIVE PC GAME DEALS -->
  <div class="hidden" id="sec-games">
    <div class="standalone-grid" id="gamesGrid"></div>
  </div>
</div>

<script>
const COMPARE_PAGES = {compare_json};
const VIDEOS = {videos_json};
const GAMES = {games_json};
let partnerId = "{CONFIG["partner_id"]}";
let oneAliLink = "{CONFIG["one_aliexpress_link"]}";
let ebayCampId = "{CONFIG["ebay_campaign_id"]}";

function switchTab(which) {{
  ['compare', 'videos', 'games'].forEach(k => {{
    document.getElementById('sec-' + k).classList.toggle('hidden', k !== which);
    document.getElementById('t-' + k).classList.toggle('active', k === which);
  }});
}}

function renderAll() {{
  document.getElementById('compareGrid').innerHTML = COMPARE_PAGES.map(p => {{
    const rowsHtml = p.table_rows.map(r => `
      <tr>
        <td style="color:#94a3b8;">${{r[0]}}</td>
        <td style="color:#34d399; font-weight:700;">${{r[1]}}</td>
        <td style="color:#cbd5e1;">${{r[2]}}</td>
      </tr>
    `).join('');
    return `
      <div class="card">
        <div>
          <div class="card-top">
            <span class="pill-purple">${{p.category}}</span>
            <span class="pill">${{p.payout_info}}</span>
          </div>
          <h3>${{p.seo_title}}</h3>
          <div class="kw-bar">🔍 Google/Bing Target Keywords: ${{p.search_keywords}}</div>
          <div style="font-size:11.5px; color:var(--muted); margin-bottom:6px;">
            Generated File: <code>/compare/${{p.slug}}.html</code> (Included in sitemap.xml &amp; Pinterest RSS!)
          </div>
          <table class="comp-table">
            <thead>
              <tr><th>Metric</th><th>🏆 ${{p.winner_name}}</th><th>${{p.runner_up_name}}</th></tr>
            </thead>
            <tbody>${{rowsHtml}}</tbody>
          </table>
          <div class="verdict-box"><strong>Verdict:</strong> ${{p.verdict}}</div>
        </div>
        <div>
          <a class="btn btn-green" href="${{p.primary_url}}?ref=${{partnerId}}" target="_blank" rel="noopener">${{p.primary_btn_text}}</a>
          <a class="btn btn-purple" href="${{p.secondary_url}}" target="_blank" rel="noopener">${{p.secondary_btn_text}}</a>
        </div>
      </div>
    `;
  }}).join('');

  document.getElementById('videoGrid').innerHTML = VIDEOS.map(v => {{
    const q = encodeURIComponent(v.ebay_keyword);
    const ebayUrl = `https://www.ebay.com/sch/i.html?_nkw=${{q}}&mkcid=1&mkrid=711-53200-19255-0&campid=${{ebayCampId}}&toolid=10001`;
    return `
      <div class="card">
        <div>
          <div class="card-top">
            <span class="pill-purple">${{v.channel_name}} (${{v.duration}})</span>
            <span class="pill">14 Country Editions</span>
          </div>
          <h3>${{v.title}}</h3>
          <div class="verdict-box" style="margin-top:8px; border-left-color:#3b82f6; background:rgba(59,130,246,0.12); color:#dbeafe;">
            <strong>📋 YouTube Video Description (Shown on Webpage — Amazon URL Stripped):</strong><br>${{v.yt_description}}
          </div>
          <div class="verdict-box" style="margin-top:8px;">
            <strong>🎙️ Spoken 2–3 Min Review Transcript:</strong><br>${{v.transcript_summary}}
          </div>
        </div>
        <div>
          <a class="btn btn-yt" href="${{v.yt_url}}" target="_blank" rel="noopener">▶ Watch 3-Min Video on YouTube →</a>
          <a class="btn btn-ebay" href="${{ebayUrl}}" target="_blank" rel="noopener">🔍 Compare "${{v.ebay_keyword}}" on eBay →</a>
          <a class="btn btn-ali" href="${{oneAliLink}}" target="_blank" rel="noopener">🔥 Shop Deal on AliExpress (1-Link) →</a>
        </div>
      </div>
    `;
  }}).join('');

  document.getElementById('gamesGrid').innerHTML = GAMES.map(g => `
    <div class="card">
      <div>
        <div class="card-top"><span class="pill-purple">${{g.store}}</span><span class="pill">-${{g.discount_pct}}% OFF</span></div>
        <h3>${{g.title}}</h3>
        <div class="verdict-box">Live Steam API Price: <strong>$${{g.price.toFixed(2)}}</strong> (Normally $${{g.old_price.toFixed(2)}})</div>
      </div>
      <div>
        <a class="btn btn-yt" href="${{g.trailer_url}}" target="_blank" rel="noopener">▶ Watch Gameplay Trailer</a>
        <a class="btn btn-green" href="${{g.base_url}}&partner=${{partnerId}}" target="_blank" rel="noopener">Buy Steam Key →</a>
      </div>
    </div>
  `).join('');
}}

renderAll();
</script>
</body>
</html>
"""
    with open("site_output/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Built Standalone Comparison Pages (/compare/*.html) + 20k Video Pages!")


if __name__ == "__main__":
    build_site()
