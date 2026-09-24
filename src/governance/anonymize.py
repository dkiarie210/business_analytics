import hashlib
import pandas as pd

def anonymize_customer_ids(df: pd.DataFrame, salt: str = "academic-demo") -> pd.DataFrame:
    """Replace customer_id with a salted hash for downstream analytics outputs."""
    df = df.copy()
    df["customer_hash"] = df["customer_id"].astype(str).apply(lambda x: hashlib.sha256((salt + x).encode()).hexdigest()[:16])
    return df.drop(columns=["customer_id"])
