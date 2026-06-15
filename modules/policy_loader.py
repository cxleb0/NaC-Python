#!/usr/bin/env python3
from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR/"policies"/"firewall_policies.yaml"

def load_policies():
    with POLICY_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
