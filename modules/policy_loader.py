#!/usr/bin/env python3
from pathlib import Path
import yaml
from modules.module import Policy
from modules.exceptions import PolicyLoadFail

BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR/"policies"/"firewall_policies.yaml"

def load_policies() -> dict[str,Policy]:
    try:
        with POLICY_FILE.open("r", encoding="utf-8") as file:
            try: 
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise PolicyLoadFail(f"Failed to load YAML file.")
            policies = {}
            for name, config in data["policies"].items():
                policies[name] = Policy(
                    name=name,
                    enabled=config.get("enabled", False),
                    severity=config.get("severity","LOW"),
                    message=config.get("message","")            
                )
            return policies
    except FileNotFoundError as e:
        raise PolicyLoadFail(f"Error loading policy {POLICY_FILE}") from e 
