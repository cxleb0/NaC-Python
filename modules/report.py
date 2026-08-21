
from modules.reporter import (
    generate_csv,
    generate_json,
    generate_xml,
    summarize_findings,
)


def generate_reports(findings, args):
    if args.format in ("csv", "all"):
        generate_csv(findings, args.report_dir/"csv_report.csv")
    if args.format in ("json", "all"):
        generate_json(findings, args.report_dir/"json_report.json")
    if args.format in ("xml", "all"):    
        generate_xml(findings, args.report_dir/"xml_report.xml")
    summarize_findings(findings)

