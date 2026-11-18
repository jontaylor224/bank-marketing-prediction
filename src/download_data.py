"""Download the official UCI Bank Marketing archive and extract bank-full.csv."""
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / "bank-full.csv"
    if target.exists():
        print(f"Dataset already exists: {target}")
        return

    print(f"Downloading {URL}")
    with urlopen(URL, timeout=60) as response:
        outer_bytes = response.read()

    with ZipFile(BytesIO(outer_bytes)) as outer:
        nested_names = [n for n in outer.namelist() if n.lower().endswith("bank.zip")]
        if not nested_names:
            raise FileNotFoundError(f"bank.zip not found; archive contains: {outer.namelist()}")
        nested_bytes = outer.read(nested_names[0])

    with ZipFile(BytesIO(nested_bytes)) as inner:
        matches = [n for n in inner.namelist() if Path(n).name.lower() == "bank-full.csv"]
        if not matches:
            raise FileNotFoundError(f"bank-full.csv not found; archive contains: {inner.namelist()}")
        target.write_bytes(inner.read(matches[0]))

    print(f"Saved {target} ({target.stat().st_size:,} bytes)")
    print("This CSV is semicolon-delimited; load it with pd.read_csv(path, sep=';').")

if __name__ == "__main__":
    main()
