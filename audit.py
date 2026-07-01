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
    summarize_findings,
    print_report
)

xml_content = load_config()
rules = get_rules(xml_content)
print(f"Found {len(rules)} rules!")

    
policies = load_policies()
any_any_policy = policies["policies"]["any_any"]
logging_policy = policies["policies"]["logging"]
description_policy = policies["policies"]["description"]
disabled_policy = policies["policies"]["disabled"]


findings = []
for rule in rules:
    checks = [
        check_any_any(rule, any_any_policy),
        check_missing_description(rule, description_policy),
        check_logging(rule, logging_policy),
        check_disabled(rule, disabled_policy)
    ]
    for c in checks:
        if c:
            findings.append(c)
            
print("Findings: ")
for finding in findings:
    print(
        f"{finding['rule']} -> "
        f"{finding['issue']} "
        f"({finding['severity']}): "
        f"{finding['message']}"

    )
print("Generating Reports...")
generate_csv(findings)
generate_json(findings)
generate_xml(findings)
summarize_findings(findings)
print_report(findings)
print("Report Generated.")






