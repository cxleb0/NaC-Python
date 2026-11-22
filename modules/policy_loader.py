from pathlib import Path

import yaml

from modules.exceptions import PolicyLoadError
from modules.module import Policy


def load_policies(policy_path: Path) -> dict[str, Policy]:
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
        raise PolicyLoadError("Failed to load YAML file. " f"{e}") from e
    except yaml.YAMLError as e:
        raise PolicyLoadError("Malformed YAML file. " f"{e}") from e
    except IsADirectoryError as e:
        raise PolicyLoadError("No file specified." f"{e}")
    if not isinstance(data, dict) or not isinstance(data.get("policies"), dict):
        raise PolicyLoadError(
            f"Invalid policy file structure: '{policy_path}'. "
            "Expected a top-level 'policies' dictionary."
        )
    policies = {}
    for name, config in data["policies"].items():
        policies[name] = Policy(
            name=name,
            enabled=config.get("enabled", False),
            severity=config.get("severity", "LOW"),
            message=config.get("message", ""),
        )
    return policies
