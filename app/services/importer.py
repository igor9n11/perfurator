import re
import string

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Fragrance

GENDERS = {"women", "men", "unisex"}

COLUMNS = {
    "Perfume": "name",
    "Brand": "brand",
    "Gender": "gender",
    "Year": "year",
    "Country": "country",
    "Top": "top_notes",
    "Middle": "middle_notes",
    "Base": "base_notes",
    "Rating Value": "source_rating",
    "Rating Count": "source_votes",
}
ACCORD_COLUMNS = [f"mainaccord{i}" for i in range(1, 6)]


def slug_to_title(slug: str) -> str:
    text = slug.strip().lower()
    text = re.sub(r"-s(?=-|$)", "'s", text)
    text = re.sub(r"(^|-)([ld])-", r"\1\2'", text)
    return string.capwords(text.replace("-", " "))


def read_catalog(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", encoding="cp1252", decimal=",")


def clean_catalog(raw: pd.DataFrame, min_votes: int) -> tuple[pd.DataFrame, dict]:
    stats = {"в файле": len(raw)}

    df = raw[raw["Rating Count"] >= min_votes].copy()
    stats[f"после фильтра голосов >= {min_votes}"] = len(df)

    df["accords"] = df[ACCORD_COLUMNS].apply(
        lambda row: ", ".join(a.strip() for a in row.dropna() if a.strip()), axis=1
    )
    df = df.rename(columns=COLUMNS)[list(COLUMNS.values()) + ["accords"]]

    text_columns = ["name", "brand", "gender", "country",
                    "top_notes", "middle_notes", "base_notes", "accords"]
    for col in text_columns:
        df[col] = df[col].str.strip().replace({"": None, "unknown": None})

    before = len(df)
    df = df.dropna(subset=["name", "brand"])
    df = df[df["gender"].isin(GENDERS)]
    stats["удалено: нет названия/бренда/пола"] = before - len(df)

    df["name"] = df["name"].map(slug_to_title)
    df["brand"] = df["brand"].map(slug_to_title)

    before = len(df)
    df = df.sort_values("source_votes", ascending=False)
    df = df.drop_duplicates(subset=["name", "brand", "gender"])
    stats["удалено дубликатов"] = before - len(df)

    stats["итого к импорту"] = len(df)
    stats["брендов"] = df["brand"].nunique()
    return df, stats


def save_catalog(db: Session, df: pd.DataFrame) -> dict:
    existing = {
        (f.name, f.brand, f.gender): f for f in db.scalars(select(Fragrance))
    }
    added = updated = 0

    records = df.astype(object).where(df.notna(), None).to_dict("records")
    for rec in records:
        if rec["year"] is not None:
            rec["year"] = int(rec["year"])
        key = (rec["name"], rec["brand"], rec["gender"])
        if key in existing:
            for field, value in rec.items():
                setattr(existing[key], field, value)
            updated += 1
        else:
            db.add(Fragrance(**rec))
            added += 1

    db.commit()
    return {"добавлено": added, "обновлено": updated}
