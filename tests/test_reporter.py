#!/usr/bin/env python3
import json
import xml.etree.ElementTree as xml

from modules.module import Finding
from modules.reporter import (
    generate_csv,
    generate_json,
    generate_xml,
)

findings = [Finding(
    rule = "Any Any rule",
    issue = "Any Any rule found",
    message = "Any Any rule detected",
    severity = "HIGH"
)]


def test_generate_csv(tmp_path):
    output_file = tmp_path/'testcsv_report.csv'
    generate_csv(findings, output_file)
    assert output_file.exists()

    content = output_file.read_text(encoding='utf-8')
    assert "Any Any rule" in content
    assert "Any Any rule found" in content
    assert "Any Any rule detected" in content
    assert "HIGH" in content

    
def test_generate_json(tmp_path):
    output_file = tmp_path/'testjson_report.json'
    generate_json(findings, output_file)
    assert output_file.exists()

    with output_file.open('r', encoding='utf-8') as file:
        content = json.load(file)
        assert content[0]["rule"] == "Any Any rule"

def test_generate_xml(tmp_path):
    output_file = tmp_path/'testxml_report.xml'
    generate_xml(findings, output_file)
    assert output_file.exists()
    xmltree = xml.parse(output_file)
    root = xmltree.getroot()

    assert root.tag == "report"
    finding = root.find('finding')
    assert finding is not None
    assert finding.find('rule').text == 'Any Any rule'
    
