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
from modules.module import FirewallRule, Policy

def test_any_any_policy_violations():
            
    rule = FirewallRule(
         name= "Any Any Rule",
         source= ["any"],
         destination=["any"],
         application=["any"],
         description="Any-Any rule detected.",
         disabled=False,
         log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="any_any",
        enabled= True,
        severity= "HIGH",
        message= "Any Any rule detected"
    )

    result = check_any_any(rule, policy)

    assert result is not None
    assert result.rule == "Any Any Rule"
    assert result.issue == "Any Any rule found"
    assert result.severity == "HIGH"

def test_no_policy_violations():
            
    rule = FirewallRule(
         name= "Web Access",
         source= ["internal"],
         destination=["external"],
         application=["web browsing"],
         description="Allow web traffic.",
         disabled=False,
         log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="Web Access",
        enabled= True,
        severity= "LOW",
        message= "Allowing web traffic"
    )

    result = check_any_any(rule, policy)

    assert result is None


def test_logging():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="Allow DNS traffic",
        disabled=False,
        log_end=False
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="logging",
        enabled= True,
        severity= "MEDIUM",
        message= "Session-End-Logging disabled."
    )
    
    result = check_logging(rule, policy)
    assert result is not None
    assert result.rule == "Allow DNS"
    assert result.issue == "Logging Disabled"
    assert result.message == "Session-End-Logging disabled."
    assert result.severity == "MEDIUM"

def test_logging_enabled():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="Allow DNS traffic",
        disabled=False,
        log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="logging",
        enabled= True,
        severity= "MEDIUM",
        message= "Session-End-Logging disabled."
    )
    
    result = check_logging(rule, policy)
    assert result is None

def test_missing_description():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="",
        disabled=False,
        log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="description",
        enabled= True,
        severity= "MEDIUM",
        message= "Security rule missing description."
    )   

    result = check_missing_description(rule, policy)
    assert result is not None
    assert result.rule == "Allow DNS"
    assert result.issue == "Missing Description"
    assert result.message == "Security rule missing description."
    assert result.severity == "MEDIUM"


def test_description():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="Allow DNS traffic",
        disabled=False,
        log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="description",
        enabled= True,
        severity= "MEDIUM",
        message= "Security rule missing description."
    )   

    result = check_missing_description(rule, policy)
    assert result is None   
    

def test_disabled_rule():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="Allow DNS traffic",
        disabled=True,
        log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="disabled",
        enabled= True,
        severity= "LOW",
        message= "Security rule is disabled."
    )
    result = check_disabled(rule, policy)
    assert result is not None
    assert result.rule == "Allow DNS"
    assert result.issue == "Disabled rule"
    assert result.message == "Security rule is disabled."
    assert result.severity == "LOW"

def test_enabled_rule():
    rule = FirewallRule(
        name= "Allow DNS",
        source= ["internal"],
        destination=["external"],
        application=["DNS"],
        description="Allow DNS traffic",
        disabled=False,
        log_end=True
    )
    
    #create a policy for testing, not using yaml yet
    policy = Policy(
        name="disabled",
        enabled= True,
        severity= "LOW",
        message= "Security rule is disabled."
    )
    result = check_disabled(rule, policy)
    assert result is None
    

