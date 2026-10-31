import sys
sys.path.append("src")
import pandas as pd
from datasets import load_dataset
from clean_ar import clean_ar, clean_light

ds = load_dataset("inparallel/saudinewsnet", split="train", trust_remote_code=True)
df = ds.to_pandas()
print("الحجم الأصلي:", len(df))

df = df.rename(columns={"content": "text"})
df["dataset"] = "snn"
for c in ["title", "url", "text"]:
    df[c] = df[c].astype(str).str.strip().str.strip('"')

dt = pd.to_datetime(df["date_extracted"], errors="coerce")
df["date"] = dt.dt.strftime("%Y-%m-%d")
df["date_reliable"] = dt >= "2015-08-01"

df = df.dropna(subset=["date"])
print("بعد حذف بدون تاريخ:", len(df))

df = df[df["text"].str.len() > 200]
print("بعد حذف النصوص القصيرة:", len(df))

df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
print("بعد حذف المكرر:", len(df))

df["id"] = ["snn_%06d" % i for i in range(len(df))]
df["title_clean"] = df["title"].map(clean_ar)
df["text_clean"] = df["text"].map(clean_ar)
df["text_light"] = df["text"].map(clean_light)

cols = ["id", "source", "dataset", "date", "date_reliable", "title", "text",
        "title_clean", "text_clean", "text_light", "url"]
df[cols].to_parquet("/kaggle/working/snn.parquet", index=False)

print("المدى:", df["date"].min(), "←", df["date"].max())
print("نسبة التاريخ الموثوق:", round(df["date_reliable"].mean(), 2))
print(df["source"].value_counts())
