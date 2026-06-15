import pytest
from modules.parser import get_rules
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "tests" / "fixtures" /"text_xml.xml"
def test_config_parser():
    with CONFIG_FILE.open('r', encoding='utf-8') as file:
        content = file.read()

        rules = get_rules(content)

        assert len(rules) == 3
        assert rules[0]["name"] == "Any Any Rule"
        assert rules[1]["name"] == "Allow DNS"
        assert rules[2]["name"] == "Good Rule"

        
         
