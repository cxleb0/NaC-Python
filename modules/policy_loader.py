#!/usr/bin/env python3
from pathlib import Path
import yaml
from modules.module import Policy


BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR/"policies"/"firewall_policies.yaml"

def load_policies() -> dict[str,Policy]:
    with POLICY_FILE.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    policies = {}
    for name, config in data["policies"].items(): #.items() makes the dict an iterable of tupels
        policies[name] = Policy(
            name=name,
            enabled=config.get("enabled", False),
            severity=config.get("severity","LOW"),
            message=config.get("message","")            
        )
    return policies
