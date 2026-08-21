import pytest
from modules.module import FirewallRule, Policy, Finding
from modules.audit_engine import generate_findings
from modules.checks import (
    check_any_any,
    check_missing_description,
    check_logging,
    check_disabled
)



def test_generate_findings():
    rules = [
        FirewallRule(
            name="Any-Any",
            source=["any"],
            destination=["any"],
            application=["any"],
            description="This is an Any Any rule",
            disabled=False,
            log_end=True
        ),
        FirewallRule(
            name="Allow Web",
            source=["internal"],
            destination=["any"],
            application=["web-browsing"],
            description="This rule allows internet browsing.",
            disabled=False,
            log_end=False
        )
    ]

    policies = {
        "any_any": Policy(
            name="any_any",
            enabled=True,
            severity="HIGH",
            message="Any-Any rule detected." 
        ),
        "logging": Policy(
            name="logging",
            enabled=True,
            severity="MEDIUM",
            message="Session-End-Logging disabled."
        ),
        "description": Policy(
            name="description",
            enabled=True,
            severity="MEDIUM",
            message="Security rule missing description."
        ),
        "disabled": Policy(
            name="Disabled",
            enabled=True,
            severity="LOW",
            message="Security rule is disabled."
        )       
    }


    findings = generate_findings(rules, policies)
    assert len(findings) == 2
    assert isinstance(findings[0], Finding)
    print(findings) 
