from pathlib import Path
import logging

LOG_PATH = Path("logs/privacy_audit.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def audit(event: str, detail: str) -> None:
    """Write a simple privacy/governance audit event."""
    logging.info("%s | %s", event, detail)
