from pathlib import Path
import pandas as pd

INPUT = Path("data/interim/ingested_ratings.csv")
OUTPUT = Path("data/interim/cleaned_ratings.csv")

def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    before = len(df)
    df = df.drop_duplicates()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df["rating_date"] = pd.to_datetime(df["rating_date"], errors="coerce")
    df = df[df["rating"].between(1, 5)]
    df = df[df["rating_date"].notna()]
    df = df[df["release_year"].between(1900, 2005)]
    df["rating_date"] = df["rating_date"].dt.date.astype(str)
    audit("CLEAN", f"Rows before={before}; after={len(df)}; removed={before-len(df)}")
    return df

def main() -> None:
    df = pd.read_csv(INPUT)
    cleaned = clean_ratings(df)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT, index=False)

if __name__ == "__main__":
    main()
