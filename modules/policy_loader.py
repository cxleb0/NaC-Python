from pathlib import Path

import yaml

from modules.exceptions import PolicyLoadError
from modules.module import Policy

#BASE_DIR = Path(__file__).resolve().parent.parent
#POLICY_FILE = BASE_DIR / "policies" / "firewall_policies.yaml"


def load_policies(policy_path:Path) -> dict[str, Policy]:
    """
    Opens and reads a .yaml policy file and creates a dictionariy with the policy name
    as the key, and a Policy dataclass object as the value.
    Returns:
        A dictionary with a string, Policy object key value pair.
    Raises:
        FileNotFoundError: if .yaml file is not found.
    """

    try:
        with open(policy_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise PolicyLoadError("Failed to load YAML file.") from e
    policies = {}
    for name, config in data["policies"].items():
        policies[name] = Policy(
            name=name,
            enabled=config.get("enabled", False),
            severity=config.get("severity", "LOW"),
            message=config.get("message", ""),
        )
    return policies
