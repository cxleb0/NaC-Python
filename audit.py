import logging
import sys

from modules.audit_engine import generate_findings
from modules.cli import cli
from modules.exceptions import FirewallAuditError, FirewallGitAuditError
from modules.git import (
    compare_findings,
    display_findings,
    get_file_at_revision,
    list_changed_rules,
    list_revision_changes,
)
from modules.loader import load_config
from modules.logging import setup_logging
from modules.parser import get_rules
from modules.policy_loader import load_policies
from modules.report import generate_reports

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    args = cli()
    if args.git:
        try:
            run_git_audit(args)
        except (FirewallGitAuditError, FirewallAuditError) as e:
            logger.error("Firewall configuration comparison failed %s", e)
            print(f"[!] {e}")
            sys.exit(1)
    else:
        try:
            run_standard_audit(args)
        except FirewallAuditError as e:
            logger.error("Firewall Audit failed %s", e)
            print(f"[!] {e}")
            sys.exit(1)


def run_standard_audit(args):
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


def run_git_audit(args):
    logger.info("[*] Loading old Git configuration.")
    old_xml = get_file_at_revision(args.old_config, args.config)

    logger.info("[*] Loading new Git configuration.")
    new_xml = get_file_at_revision(args.new_config, args.config)

    logger.info("[*] Parsing old firewall configutation...")
    old_rules = get_rules(old_xml)

    logger.info("[*] Parsing new firewall configuration...")
    new_rules = get_rules(new_xml)

    logger.info("Generating firewall rule changes...")
    changed_rules = list_revision_changes(old_rules, new_rules)
    list_changed_rules(changed_rules)

    logger.info("[*] Loading firewall policies...")
    policies = load_policies(args.policy)
    logger.info("Auditing old firewall configuration...")
    old_findings = generate_findings(old_rules, policies)
    logger.info("Auditing new firewall configuration")
    new_findings = generate_findings(new_rules, policies)
    results = compare_findings(old_findings, new_findings)
    display_findings(results)


if __name__ == "__main__":
    main()
