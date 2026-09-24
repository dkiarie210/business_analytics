import argparse
import os
from pathlib import Path
from typing import Dict, Any

import boto3
import pandas as pd
import yaml


def upload_cleaned_csv_to_s3(local_file: str, bucket: str, s3_key: str) -> str:
    """Upload the cleaned/anonymized CSV to AWS S3.

    Credentials should come from AWS CLI, environment variables, or an IAM role.
    Do not hard-code AWS keys in the project.
    """
    path = Path(local_file)
    if not path.exists():
        raise FileNotFoundError(f"Cannot upload missing file: {path}")
    if not bucket or bucket.startswith("${"):
        raise ValueError("S3 bucket is not configured. Set S3_BUCKET_NAME or update config/pipeline_config.yaml")

    s3 = boto3.client("s3")
    s3.upload_file(
        Filename=str(path),
        Bucket=bucket,
        Key=s3_key,
        ExtraArgs={"ServerSideEncryption": "AES256"}
    )
    return f"s3://{bucket}/{s3_key}"

