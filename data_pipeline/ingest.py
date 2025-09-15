from urllib.request import urlretrieve
from pathlib import Path
import requests
import zipfile

from data_pipeline.config import (
    API_URL,
    HEADERS,
    OUTPUT_DIR,
    IGNORE_FILE,
    ZIP_FILE_NAME,
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_figshare_file(file_name=ZIP_FILE_NAME):
    """Download a specific file from Figshare article if it doesn't exist."""
    file_path = OUTPUT_DIR / file_name

    if file_path.exists():
        print(f"✅ File already exists: {file_name}")
        return file_path

    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch article metadata. Status code: {response.status_code}"
        )
    files = response.json()["files"]

    download_url = next(
        (f["download_url"] for f in files if f["name"] == file_name), None
    )

    if not download_url:
        raise Exception(f"File {file_name} not found in Figshare article.")

    print(f"⬇️ Downloading: {file_name} ...")
    urlretrieve(download_url, file_path)
    print(f"✅ Download complete: {file_name}")
    return file_path


def unzip_and_clean(zip_path, ignore_file=IGNORE_FILE):
    """Unzip the downloaded file and remove ignored files."""
    zip_path = Path(zip_path)
    extracted_flag_file = OUTPUT_DIR / ".unzipped"

    if zip_path.exists() and not extracted_flag_file.exists():
        print("🔄 Extracting zip file...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(OUTPUT_DIR)
        # Create a small file to mark extraction is done
        extracted_flag_file.touch()
        print(f"📦 Unzipped: {zip_path}")
    else:
        print("✅ Files already extracted or zip missing")

    ignore_path = OUTPUT_DIR / ignore_file
    if ignore_path.exists():
        ignore_path.unlink()
        print(f"❌ Removed ignored file: {ignore_file}")


def list_downloaded_files():
    """List the first few downloaded files."""
    downloaded_files = list(OUTPUT_DIR.iterdir())
    print(f"Downloaded {len(downloaded_files)} files")
    print("Contents include:", "\n".join([f.name for f in downloaded_files[:5]]))


if __name__ == "__main__":
    print("🔄 Starting download and preprocessing ...")
    zip_path = download_figshare_file()
    unzip_and_clean(zip_path)
    list_downloaded_files()
