import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT = BASE_DIR / "reports" / "report.csv" 
def generate_report(list):
    with open(REPORT, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["rule", "issue", "severity", "message"])
        writer.writeheader()
        writer.writerows(list)
