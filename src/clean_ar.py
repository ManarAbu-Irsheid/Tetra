import re

DIACRITICS = re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670\u06D6-\u06ED]')
URLS = re.compile(r'https?://\S+|www\.\S+')
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def clean_light(text):
    """تنظيف خفيف لـ AraBERT: روابط + تشكيل + تطويل + أرقام"""
    if not isinstance(text, str):
        return ""
    text = text.strip().strip('"')
    text = URLS.sub(" ", text)
    text = DIACRITICS.sub("", text)
    text = text.replace("\u0640", "")
    text = text.translate(AR_DIGITS)
    return re.sub(r"\s+", " ", text).strip()

def clean_ar(text):
    """تنظيف كامل لـ TF-IDF والـ embeddings"""
    text = clean_light(text)
    text = re.sub("[إأآٱ]", "ا", text)
    text = text.replace("ى", "ي")
    text = re.sub(r"[^\u0600-\u06FF0-9\s\.\,\؟\?\!\:\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
