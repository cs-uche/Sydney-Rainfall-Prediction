from pathlib import Path

ARTICLE_ID = 14096681
API_URL = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
HEADERS = {"Content-Type": "application/json"}
OUTPUT_DIR = "../data/raw/"
IGNORE_FILE = "observed_daily_rainfall_SYD.csv"
ZIP_FILE_NAME = "data.zip"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
