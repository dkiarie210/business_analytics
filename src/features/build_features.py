from pathlib import Path
import pandas as pd

INPUT = Path("data/interim/cleaned_ratings.csv")
OUTPUT = Path("data/processed/customer_features.csv")

def build_customer_features(df: pd.DataFrame, min_customer_ratings: int = 5) -> pd.DataFrame:
    df = df.copy()
    df["rating_date"] = pd.to_datetime(df["rating_date"], errors="coerce")
    df["title_age_at_rating"] = df["rating_date"].dt.year - df["release_year"]
    max_date = df["rating_date"].max()
    grouped = df.groupby("customer_id")
    features = grouped.agg(
        rating_count=("rating", "count"),
        average_rating=("rating", "mean"),
        rating_std_dev=("rating", "std"),
        first_rating_date=("rating_date", "min"),
        last_rating_date=("rating_date", "max"),
        average_title_release_year=("release_year", "mean"),
        average_title_age_at_rating=("title_age_at_rating", "mean"),
    ).reset_index()
    features["rating_std_dev"] = features["rating_std_dev"].fillna(0)
    ratios = grouped["rating"].agg(
        high_rating_ratio=lambda s: (s >= 4).mean(),
        low_rating_ratio=lambda s: (s <= 2).mean(),
    ).reset_index()
    features = features.merge(ratios, on="customer_id", how="left")
    features["active_days"] = (features["last_rating_date"] - features["first_rating_date"]).dt.days + 1
    features["customer_tenure_days"] = features["active_days"]
    features["recency_days"] = (max_date - features["last_rating_date"]).dt.days
    features["monthly_rating_frequency"] = features["rating_count"] / (features["active_days"].clip(lower=1) / 30.0)
    monthly = df.assign(month=df["rating_date"].dt.to_period("M")).groupby(["customer_id", "month"]).size().reset_index(name="monthly_count")
    variability = monthly.groupby("customer_id")["monthly_count"].std().fillna(0).reset_index(name="rating_frequency_variability")
    features = features.merge(variability, on="customer_id", how="left")
    features = features[features["rating_count"] >= min_customer_ratings]
    return features.sort_values("customer_id")

def main() -> None:
    df = pd.read_csv(INPUT)
    features = build_customer_features(df)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT, index=False)

if __name__ == "__main__":
    main()
