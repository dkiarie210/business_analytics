from pathlib import Path
import json
import pandas as pd
from src.governance.privacy_audit import audit

INPUT = Path("data/processed/customer_features.csv")
OUTPUT = Path("reports/bias_detection_results.json")

def activity_band(count: int) -> str:
    if count < 10:
        return "low_activity"
    if count < 25:
        return "medium_activity"
    return "high_activity"

def main() -> None:
    df = pd.read_csv(INPUT)
    df["activity_band"] = df["rating_count"].apply(activity_band)
    distribution = df["activity_band"].value_counts(normalize=True).round(4).to_dict()
    min_share = min(distribution.values()) if distribution else 0
    results = {
        "protected_attributes_used": False,
        "bias_type_checked": "behavioral representation bias",
        "activity_band_distribution": distribution,
        "minimum_band_share": min_share,
        "flag": min_share < 0.05
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    audit("BIAS_CHECK", f"Representation flag={results['flag']} results={OUTPUT}")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
