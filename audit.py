import sys
import argparse
import logging
from pathlib import Path
from modules.loader import load_config
from modules.parser import get_rules
from modules.policy_loader import load_policies
from modules.exceptions import FirewallAuditError
from modules.checks import (
    check_any_any,
    check_missing_description,
    check_logging,
    check_disabled
)
from modules.reporter import (
    generate_csv,
    generate_json,
    generate_xml,
    summarize_findings
)



logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description="Firewall Policy Engine")
def main():
    parser.add_argument(
        "--config",
        required=True,
        help="Directory where XML configurations reside."
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        required=True,
        help="Where to save generated reports,"
    )
    parser.add_argument(
        "--format",
        choices=["csv","json","xml","all"],
        default="all",
        help="Format to generate reports."
    )
    args = parser.parse_args()
    
    logging.basicConfig(
        filename="audit.log",
        level=logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )
    try: 
        logging.info("Loading XML Configuration...")
        xml_content = load_config(args.config)
        logging.info("Parsing Firewall Rules...")
        rules = get_rules(xml_content)
        logging.info(f"Parsed {len(rules)} Rules...")
        #print(f"Found {len(rules)} rules!")
        logger.info("Loading Policies...")
        policies = load_policies()
        rule_checks = {
            "any_any": check_any_any,
            "description": check_missing_description,
            "logging": check_logging,
            "disabled": check_disabled
        }
        findings = []
        for rule in rules:
            for policy_name, check_function in rule_checks.items():
                policy = policies[policy_name]
                result = check_function(rule, policy)
                if result:
                    findings.append(result)

            logging.info("Generating Reports...")
            if args.format in ("csv", "all"):
                generate_csv(findings, args.report_dir/"csv_report.csv")
            if args.format in ("json", "all"):
                generate_json(findings, args.report_dir/"json_report.json")
            if args.format in ("xml", "all"):    
                generate_xml(findings, args.report_dir/"xml_report.xml")
            summarize_findings(findings)
            logging.info("Reports Generated.")
    except FirewallAuditError as e:
        logging.error(e)
        print(e)
        sys.exit(1)
if __name__ == '__main__':
    main()





