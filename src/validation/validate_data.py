from pathlib import Path
import json
import pandas as pd
from src.governance.privacy_audit import audit

INPUT = Path("data/interim/cleaned_ratings.csv")
OUTPUT = Path("reports/validation_results.json")

def validate_cleaned_ratings(df: pd.DataFrame) -> dict:
    results = {
        "row_count_at_least_5000": bool(len(df) >= 5000),
        "customer_id_not_null": bool(df["customer_id"].notna().all()),
        "rating_between_1_and_5": bool(df["rating"].between(1, 5).all()),
        "release_year_valid": bool(df["release_year"].between(1900, 2005).all()),
        "rating_date_not_null": bool(df["rating_date"].notna().all()),
        "duplicate_count": int(df.duplicated().sum()),
    }
    results["overall_success"] = bool(all(v for k, v in results.items() if k != "duplicate_count") and results["duplicate_count"] == 0)
    return results

def main() -> None:
    df = pd.read_csv(INPUT)
    results = validate_cleaned_ratings(df)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    audit("VALIDATE", f"Validation success={results['overall_success']} results={OUTPUT}")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
