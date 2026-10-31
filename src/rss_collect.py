import sys, re, time, html, hashlib, datetime as dt
sys.path.append("src")
import feedparser, trafilatura
import pandas as pd
from clean_ar import clean_ar, clean_light

feedparser.USER_AGENT = "Mozilla/5.0 (compatible; TetraNewsBot/0.1; university project)"

FEEDS = {
    "bbc_arabic": "https://feeds.bbci.co.uk/arabic/rss.xml",
    "aljazeera":  "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a84db769f779/73d0e1b4-532f-45ef-b135-bfdff8b8cab9",
    "aawsat":     "https://aawsat.com/feed",
    "okaz":       "https://www.okaz.com.sa/rssFeed/0",
    "skynews":    "https://www.skynewsarabia.com/rss.xml",
}

OUT = sys.argv[1] if len(sys.argv) > 1 else "rss_today.parquet"
MAX_PER_FEED = 20
MIN_WORDS = 60
FEED_TEXT_MIN_WORDS = 120

BOILER = re.compile(
    r"^(Published( On)?\b.*|\|?\s*آخر تحديث.*|(عاجل)+[\s,،|]*|المصدر\s*:.*|التفاصيل بعد قليل.*)$"
)


def strip_html(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()


def remove_boilerplate(text, title):
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line == title.strip() or BOILER.match(line):
            continue
        out.append(line)
    return "\n".join(out)


def get_text(e):
    raw = e.content[0].get("value", "") if e.get("content") else e.get("summary", "")
    feed_text = strip_html(raw)
    if len(feed_text.split()) >= FEED_TEXT_MIN_WORDS:
        return feed_text
    page = trafilatura.fetch_url(e.link)
    page_text = trafilatura.extract(page) if page else None
    time.sleep(1)
    return page_text or feed_text


def get_date(e):
    t = e.get("published_parsed") or e.get("updated_parsed")
    if t:
        return dt.date(*t[:3]).isoformat()
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


rows, seen = [], set()
for source, url in FEEDS.items():
    feed = feedparser.parse(url)
    n = 0
    for e in feed.entries[:MAX_PER_FEED]:
        link = e.get("link")
        if not link or link in seen:
            continue
        seen.add(link)
        title = strip_html(e.get("title", ""))
        text = remove_boilerplate(get_text(e), title)
        if len(text.split()) < MIN_WORDS:
            continue
        rows.append({
            "id": "rss_" + hashlib.md5(link.encode()).hexdigest()[:10],
            "source": source,
            "dataset": "rss",
            "date": get_date(e),
            "date_reliable": True,
            "title": title,
            "text": text,
            "title_clean": clean_ar(title),
            "text_clean": clean_ar(text),
            "text_light": clean_light(text),
            "url": link,
        })
        n += 1
    print(source, "→", n, "خبر")

df = pd.DataFrame(rows)
df.to_parquet(OUT, index=False)
print("المجموع:", len(df), "→", OUT)
