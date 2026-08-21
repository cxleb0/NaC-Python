import logging
import sys

from modules.audit_engine import generate_findings
from modules.cli import cli
from modules.exceptions import FirewallAuditError
from modules.loader import load_config
from modules.logging import setup_logging
from modules.parser import get_rules
from modules.policy_loader import load_policies
from modules.report import generate_reports


def main():
    setup_logging()
    args = cli()
    try: 
        logging.info("[*] Loading XML Configuration...")
        xml_content = load_config(args.config)
        logging.info("[*] Parsing Firewall Rules...")
        rules = get_rules(xml_content)
        logging.info(f"[*] Parsed {len(rules)} Rules...")
    
        logging.info("[*] Loading Policies...")
        policies = load_policies()
        findings = generate_findings(rules, policies)
        
        logging.info("[*] Generating Reports...")
        generate_reports(findings, args)
        logging.info("[*] Reports Generated.")
    except FirewallAuditError as e:
        logging.error(e)
        print(f"[!] {e}")
        sys.exit(1)
        
if __name__ == '__main__':
    main()





