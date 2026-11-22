import csv
import json
from dataclasses import asdict
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, SubElement

from modules.module import Finding


def generate_csv(findings: list[Finding], output_path: Path) -> None:
    """
    Creates a csv file from the list of Findings recieves.
    Args:
         Findings: List of Findings objects.
         Output_path: File path to save the csv file.
    """
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["rule", "issue", "severity", "message"]
        )
        writer.writeheader()
        writer.writerows(asdict(f) for f in findings)


def generate_json(findings: list[Finding], output_path: Path) -> None:
    """
    Creates a json file from the list of Findings recieves.
    Args:
         Findings: List of Findings objects.
         Output_path: File path to save the json file.
    """
    with output_path.open("w", newline="", encoding="utf-8") as file:
        json.dump([asdict(f) for f in findings], file, indent=4)


def generate_xml(findings: list[Finding], output_path: Path) -> None:
    """
    Creates a csv file from the list of Findings recieves.
    Args:
         Findings: List of Findings objects.
         Output_path: File path to save the csv file.
    """
    root = Element("report")

    for f in findings:
        finding_element = SubElement(root, "finding")

        SubElement(finding_element, "rule").text = f.rule
        SubElement(finding_element, "issue").text = f.issue
        SubElement(finding_element, "severity").text = f.severity
        SubElement(finding_element, "message").text = f.message

    tree = ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def summarize_findings(findings: list[Finding]) -> None:
    """
    Displays a summary of results found from the list of Findings.
    Args:
         Findings: List of Findings objects.
    """
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
