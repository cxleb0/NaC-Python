import csv
import json
from xml.etree.ElementTree import Element, tostring, SubElement, ElementTree
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_report = BASE_DIR / "reports" / "csv_report.csv"
json_report = BASE_DIR / "reports" / "json_report.json"
xml_report = BASE_DIR / "reports" / "xml_report.xml"
def generate_csv(findings):
    with open(csv_report, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["rule", "issue", "severity", "message"])
        writer.writeheader()
        writer.writerows(findings)


def generate_json(findings):
    with open(json_report, "w", newline="") as file:
        json.dump(findings, file, indent=4)


def generate_xml(findings):
    root = Element('report')
    for finding in findings:
        finding_element = SubElement(root, "finding")

        rule = SubElement(finding_element, "rule")
        rule.text = finding["rule"]

        issue = SubElement(finding_element, "issue")
        issue.text = finding["issue"]

        severity = SubElement(finding_element, "severity")
        severity.text = finding["severity"]

        message = SubElement(finding_element, "message")
        message.text = finding["message"]

    tree = ElementTree(root)
    tree.write(xml_report, encoding='utf-8', xml_declaration=True)


def summarize_findings(findings):
    low = 0
    medium = 0
    high = 0
    for finding in findings:
        severity = finding["severity"]        
        if severity == 'HIGH':
            high += 1
        elif severity == "MEDIUM":
            medium += 1
        elif severity == "LOW":
            low += 1

    total = len(findings)
    status = "FAIL" if high >= 1 else "PASS"
    
    return  {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "status": status
        }
def print_report(findings):
    summary = summarize_findings(findings)

    print("=" * 35)
    print("Firewall Audit Report")
    print("=" * 35)

    print(f"Total Findings: {summary['total']}")
    print(f"HIGH:   {summary['high']}")
    print(f"MEDIUM: {summary['medium']}")
    print(f"LOW:    {summary['low']}")
    print()
    print(f"STATUS: {summary['status']}")
