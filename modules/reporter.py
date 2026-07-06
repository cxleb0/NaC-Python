import csv
import json
from xml.etree.ElementTree import Element, tostring, SubElement, ElementTree
from pathlib import Path
from modules.module import Finding
from dataclasses import asdict
BASE_DIR = Path(__file__).resolve().parent.parent
csv_report = BASE_DIR / "reports" / "csv_report.csv"
json_report = BASE_DIR / "reports" / "json_report.json"
xml_report = BASE_DIR / "reports" / "xml_report.xml"

def generate_csv(findings: list[Finding]) -> None:
    with open(csv_report, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["rule", "issue", "severity", "message"])
        writer.writeheader()
        writer.writerows(asdict(f) for f in findings)


def generate_json(findings: list[Finding]) -> None:
    with open(json_report, "w", newline="") as file:
        json.dump([asdict(f) for f in findings], file, indent=4)


def generate_xml(findings: list[Finding]) -> None:
    root = Element('report')
    
    for f in findings:
        finding_element = SubElement(root, "finding")

        SubElement(finding_element, "rule").text = f.rule
        SubElement(finding_element, "issue").text = f.issue
        SubElement(finding_element, "severity").text = f.severity
        SubElement(finding_element, "message").text = f.message

    tree = ElementTree(root)
    tree.write(xml_report, encoding='utf-8', xml_declaration=True)


def summarize_findings(findings: list[Finding]) -> None:
    low = 0
    medium = 0
    high = 0
    
    high = sum(1 for f in findings if f.severity == "HIGH")
    medium = sum(1 for f in findings if f.severity == "MEDIUM")
    low = sum(1 for f in findings if f.severity == "LOW")

    total = len(findings)
    status = "FAIL" if high >= 1 else "PASS"
    
    print(f"Total: {total}")
    print(f"HIGH: {high}")
    print(f"MEDIUM: {medium}")
    print(f"LOW: {low}")
    print(status)
        

