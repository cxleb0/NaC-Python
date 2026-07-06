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
def main():
    
    xml_content = load_config()
    rules = get_rules(xml_content)
    print(f"Found {len(rules)} rules!")
    policies = load_policies()
    """any_any_policy = policies["policies"]["any_any"]
    logging_policy = policies["policies"]["logging"]
    description_policy = policies["policies"]["description"]
    disabled_policy = policies["policies"]["disabled"]
    """
    rule_checks = [
        #tuples
        ("any_any", check_any_any),
        ("description", check_missing_description),
        ("logging", check_logging),
        ("disabled", check_disabled)
    ]
    findings = []
    for rule in rules:
        for policy_name, check_function in rule_checks:
            policy = policies[policy_name]
            result = check_function(rule, policy)
            if result:
                findings.append(result)

    print("Generating Reports...")
    generate_csv(findings)
    generate_json(findings)
    generate_xml(findings)
    summarize_findings(findings)
    print("Report Generated.")
if __name__ == '__main__':
    main()





