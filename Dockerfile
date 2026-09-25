FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["bash", "-c", "python src/data/ingest.py && python src/data/clean.py && python src/features/build_features.py && python src/validation/validate_data.py && python src/bias/bias_detection.py && pytest"]
