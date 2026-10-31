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
MIN_WO
