import logging
from modules.loader import load_config
from modules.parser import get_rules
from modules.policy_loader import load_policies
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
def main():
    logging.basicConfig(
        filename="audit.log",
        level=logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Loading XML Configuration...")
    xml_content = load_config()
    logging.info("Parsing Firewall Rules...")
    rules = get_rules(xml_content)
    logging.info(f"Parsed {len(rules)} Rules...")
    #print(f"Found {len(rules)} rules!")
    logger.info("Loading Policies...")
    policies = load_policies()
    """any_any_policy = policies["policies"]["any_any"]
    logging_policy = policies["policies"]["logging"]
    description_policy = policies["policies"]["description"]
    disabled_policy = policies["policies"]["disabled"]
    """
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
    generate_csv(findings)
    generate_json(findings)
    generate_xml(findings)
    summarize_findings(findings)
    logging.info("Reports Generated.")
if __name__ == '__main__':
    main()





