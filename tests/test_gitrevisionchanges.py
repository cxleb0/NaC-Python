from modules.module import (FirewallRule, RuleFieldChange)
from modules.git import list_revision_changes
old_rule = FirewallRule(
    name="Allow Web",
    source=["Internal"],
    destination=["Internet"],
    application=["web-browsing"],
    description="Allow web traffic",
    disabled=False,
    log_end=True
)

new_rule = FirewallRule(
    name="Allow Web",
    source=["Internal"],
    destination=["Internet"],
    application=["web-browsing"],
    description="Allow web traffic",
    disabled=False,
    log_end=True
)

def test_unmodified_rule():
    old_rules = [old_rule]
    new_rules = [new_rule]

    results = list_revision_changes(old_rules, new_rules)

    assert len(results["unmodified"]) == 1
    assert len(results["modified"]) == 0
    assert len(results["added"]) == 0
    assert len(results["deleted"]) == 0

def test_added_rule():
    new_rule = FirewallRule(
        name="Allow DHCP",
        source=["Internal"],
        destination=["Internet"],
        application=["DHCP"],
        description="Allow DHCP traffic",
        disabled=False,
        log_end=True
    )
    old_rules = []
    new_rules = [new_rule]

    results = list_revision_changes(old_rules, new_rules)
    assert len(results["unmodified"]) == 0
    assert len(results["modified"]) == 0
    assert len(results["added"]) == 1
    assert len(results["deleted"]) == 0

def test_modified_rule():
    new_rule = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=True,
        log_end=True
    )
    old_rules = [old_rule]
    new_rules = [new_rule]

    results = list_revision_changes(old_rules, new_rules)
    assert len(results["unmodified"]) == 0
    assert len(results["modified"]) == 1
    assert len(results["added"]) == 0
    assert len(results["deleted"]) == 0

def test_deleted_rule():
    new_rules = []
    old_rules = [old_rule]

    results = list_revision_changes(old_rules, new_rules)
    assert len(results["unmodified"]) == 0
    assert len(results["modified"]) == 0
    assert len(results["added"]) == 0
    assert len(results["deleted"]) == 1
