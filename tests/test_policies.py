import pytest
from modules.policy_loader import load_policies
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
YAML_FILE = BASE_DIR / "tests" / "fixtures" / "test_policies.yaml"
def test_policies():
    with YAML_FILE.open('r', encoding='utf-8') as file:
        content = file.read()

        policies = yaml.safe_load(content)

        assert len(policies) > 0
        assert policies["policies"]["any_any"]["severity"] == "HIGH"
        assert policies["policies"]["safe_rule"]["severity"] == "HIGH" 
        
