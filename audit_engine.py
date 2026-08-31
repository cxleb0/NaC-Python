from modules.checks import (
    check_any_any,
    check_disabled,
    check_logging,
    check_missing_description,
)
from modules.module import FirewallRule, Policy


def generate_findings(
    rules: list[FirewallRule], policies: dict[str, Policy]
) -> list[str]:
    rule_checks = {
        "any_any": check_any_any,
        "description": check_missing_description,
        "logging": check_logging,
        "disabled": check_disabled,
    }
    findings = []
    for rule in rules:
        for policy_name, check_function in rule_checks.items():
            policy = policies[policy_name]
            result = check_function(rule, policy)
            if result:
                findings.append(result)
    return findings
