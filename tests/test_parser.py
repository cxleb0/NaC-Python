from pathlib import Path

import pytest

from modules.exceptions import ConfigParseError
from modules.module import FirewallRule
from modules.parser import get_rules

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "tests" / "fixtures" /"test.xml"

#test parsing the correct number of rules
def test_config_parser():
    #config file var is a path variable, get rules expects a str, so read the file first and store in content
    with CONFIG_FILE.open('r', encoding='utf-8') as file:
        content = file.read()
    rules = get_rules(content)
    assert len(rules) == 3

#test a list of FW rule objects is getting returned
def test_config_object():
    with CONFIG_FILE.open('r', encoding='utf-8') as file:
        content = file.read()

    rules = get_rules(content)
    assert isinstance(rules[0], FirewallRule)
         

def test_config_extraction():
    #testing the extracted values in the list of FW objects
    with CONFIG_FILE.open('r', encoding='utf-8') as file:
        content = file.read()
    rules = get_rules(content)

    rule = rules[0]
    assert rule.name == "Any Any Rule"
    assert rule.source == ["any"]
    assert rule.destination == ["any"]
    assert rule.application == ["any"]
    assert rule.description == ""
    assert rule.disabled is False
    assert rule.log_end is True

    if rule.name is None:
        raise ValueError
    
def test_config_customexception():
    with pytest.raises(ConfigParseError):
        get_rules("not an xml")
    
    
