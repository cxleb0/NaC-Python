#!/usr/bin/env python3
import pytest
from pathlib import Path
from modules.policy_loader import load_policies
from modules.parser import get_rules
from modules.checks import (
    check_any_any,
    check_missing_description,
    check_logging,
    check_disabled
)

def test_any_any_policy_violations():
            
    rule = {
        "name": "Any Any Rule",
        "source": ["any"],
        "destination": ["any"],
        "application": ["any"]
    }
    
    #create a policy for testing, not using yaml yet
    policy = {
        "enabled": True,
        "severity": "HIGH",
        "message": "Any Any rule detected"
    }

    result = check_any_any(rule, policy)
    assert rule is not None
    assert policy["severity"] == "HIGH"

def test_missing_description():
    rule2 = {
        "name": "Logging Disabled",
        "source": ["Internal"],
        "destination": ["Internet"],
        "application": ["web-browsing"],
        "log-end": ["no"]
    }

    policy2 = {
        "enabled": True,
        "severity": "Medium",
        "message": "Logging Disabled" 
    }
    result = check_logging(rule2, policy2)
    assert rule2 is not None
    assert policy2["severity"] == "Medium"
    


