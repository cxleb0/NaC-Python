import pytest
from modules.module import FirewallRule
from modules.git import get_field_changes

old_rule = FirewallRule(
    name="Allow Web",
    source=["Internal"],
    destination=["Internet"],
    application=["web-browsing"],
    description="Allow web traffic",
    disabled=False,
    log_end=True
)

def test_source_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["External"],
        destination=["Internet"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=False,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "source"
    assert results[0].old_value == ["Internal"]
    assert results[0].new_value == ["External"]

def test_destination_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["External"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=False,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "destination"
    assert results[0].old_value == ["Internet"]
    assert results[0].new_value == ["External"]

def test_application_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["https"],
        description="Allow web traffic",
        disabled=False,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "application"
    assert results[0].old_value == ["web-browsing"]
    assert results[0].new_value == ["https"]

def test_description_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["web-browsing"],
        description="web traffic",
        disabled=False,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "description"
    assert results[0].old_value == "Allow web traffic"
    assert results[0].new_value == "web traffic"

def test_disabled_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=True,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "disabled"
    assert results[0].old_value == False
    assert results[0].new_value == True

def test_log_end_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=False,
        log_end=False
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 1
    assert results[0].field == "logging"
    assert results[0].old_value == True
    assert results[0].new_value == False

def test_no_field_change():
    old_rules = old_rule
    new_rules = FirewallRule(
        name="Allow Web",
        source=["Internal"],
        destination=["Internet"],
        application=["web-browsing"],
        description="Allow web traffic",
        disabled=False,
        log_end=True
    )
    results = get_field_changes(old_rules, new_rules)
    assert len(results) == 0


