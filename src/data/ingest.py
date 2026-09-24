import os
from pathlib import Path

import kagglehub
import pandas as pd

RAW = Path("data/raw/kaggle_netflix_ratings.csv")
INTERIM = Path("data/interim/ingested_ratings.csv")

DATASET = "netflix-inc/netflix-prize-data"
# Full dataset is ~100M rows; cap it for local runs. Set MAX_ROWS=0 for everything.
MAX_ROWS = int(os.getenv("MAX_ROWS", "1000000"))

REQUIRED = {"customer_id", "movie_id", "movie_title", "release_year", "rating", "rating_date"}


def download_dataset() -> Path:
    path = Path(kagglehub.dataset_download(DATASET))
    print(f"Dataset downloaded to: {path}")
    return path


def load_movie_titles(path: Path) -> pd.DataFrame:
    rows = []
    with open(path / "movie_titles.csv", encoding="latin-1") as f:
        for line in f:
            # Titles can contain commas, so only split on the first two
            movie_id, year, title = line.rstrip("\n").split(",", 2)
            rows.append((int(movie_id), None if year == "NULL" else int(year), title))
    df = pd.DataFrame(rows, columns=["movie_id", "release_year", "movie_title"])
    df["release_year"] = df["release_year"].astype("Int64")
    return df


def load_ratings(path: Path, max_rows: int) -> pd.DataFrame:
    rows = []
    files = sorted(path.glob("combined_data_*.txt"))
    if not files:
        raise FileNotFoundError(f"No combined_data_*.txt files found in {path}")

    for file in files:
        movie_id = None
        with open(file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.endswith(":"):
                    movie_id = int(line[:-1])
                    continue
                customer_id, rating, rating_date = line.split(",")
                rows.append((int(customer_id), movie_id, int(rating), rating_date))
                if max_rows and len(rows) >= max_rows:
                    return pd.DataFrame(rows, columns=["customer_id", "movie_id", "rating", "rating_date"])

    return pd.DataFrame(rows, columns=["customer_id", "movie_id", "rating", "rating_date"])


def main() -> None:
    path = download_dataset()

    ratings = load_ratings(path, MAX_ROWS)
    titles = load_movie_titles(path)
    df = ratings.merge(titles, on="movie_id", how="left")
    df = df[["customer_id", "movie_id", "movie_title", "release_year", "rating", "rating_date"]]

    RAW.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW, index=False)
    print(f"Saved {len(df):,} rows to {RAW}")

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    INTERIM.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(INTERIM, index=False)
    print(f"Saved {len(df):,} rows to {INTERIM}")


if __name__ == "__main__":
    main()