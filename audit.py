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

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    args = cli()
    try:
        logger.info("[*] Loading XML Configuration...")
        xml_content = load_config(args.config)
        logger.info("[*] Parsing Firewall Rules...")
        rules = get_rules(xml_content)
        logger.info(f"[*] Parsed {len(rules)} Rules...")

        logger.info("[*] Loading Policies...")
        policies = load_policies(args.policy)
        findings = generate_findings(rules, policies)

        logger.info("[*] Generating Reports...")
        generate_reports(findings, args)
        logger.info("[*] Reports Generated.")
    except FirewallAuditError as e:
        logger.error("Firewall Audit failed %s", e)
        print(f"[!] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
