# Netflix Customer Segmentation

A business analytics project that uses the **Netflix Prize dataset** to identify meaningful customer behavior segments using unsupervised machine learning.

## Project Goal

Transform raw customer rating activity into clear, explainable customer segments that support product, content, and marketing analysis while maintaining privacy and responsible data use.

## Tech Stack

- **Cloud:** AWS
- **Storage:** Amazon S3
- **Data Processing:** AWS Glue, Python
- **Analytics:** pandas, NumPy, DuckDB
- **Machine Learning:** scikit-learn
- **Visualization:** Matplotlib, Power BI
- **Development:** Jupyter / SageMaker
- **Version Control:** Git, GitHub, DVC


## Setup

```bash
pip install -r requirements.txt
```

## Project Workflow

1. Ingest and validate Netflix Prize data
2. Build customer-level behavioral features
3. Perform exploratory data analysis
4. Develop and compare clustering models
5. Evaluate cluster quality and stability
6. Profile customer segments
7. Build Power BI dashboards
8. Document privacy, fairness, and governance

## Data Privacy

Raw Netflix Prize data is **not stored in this public repository**. The project uses anonymized customer identifiers and publishes only approved analytical outputs.

## Key Evaluation Metrics

- Silhouette Score
- Davies-Bouldin Index
- Cluster Stability
- Segment Population Balance
- Data Quality and Coverage