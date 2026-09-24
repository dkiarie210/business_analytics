import pandas as pd
from src.data.clean import clean_ratings
from src.features.build_features import build_customer_features

def test_clean_ratings_removes_invalid_values():
    df = pd.DataFrame({
        "customer_id": ["C1", "C1", "C2"],
        "movie_id": [1, 1, 2],
        "movie_title": ["A", "A", "B"],
        "release_year": [2000, 2000, 2001],
        "rating": [5, 6, None],
        "rating_date": ["2001-01-01", "2001-01-01", "bad-date"]
    })
    cleaned = clean_ratings(df)
    assert len(cleaned) == 1
    assert cleaned["rating"].between(1, 5).all()

def test_build_customer_features_outputs_expected_columns():
    df = pd.DataFrame({
        "customer_id": ["C1"] * 5,
        "movie_id": [1, 2, 3, 4, 5],
        "movie_title": list("ABCDE"),
        "release_year": [1999, 2000, 2001, 2002, 2003],
        "rating": [5, 4, 3, 2, 1],
        "rating_date": pd.to_datetime(["2004-01-01", "2004-02-01", "2004-03-01", "2004-04-01", "2004-05-01"]),
    })
    features = build_customer_features(df, min_customer_ratings=5)
    assert "rating_count" in features.columns
    assert "recency_days" in features.columns
    assert features.iloc[0]["rating_count"] == 5
