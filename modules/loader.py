from pathlib import Path

from modules.exceptions import ConfigLoadError


def load_config(config_path: Path) -> str:
    """
    Opens and reads a firewall XML configuration file and returns it as a string.
    Args:
        config_path: a path to the configuration file that is accepted as an argument.
    Returns:
        A string version of the xml configuration file.
    Raises:
        FileNotFoundError: If file cannot be found.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        raise ConfigLoadError(f"Unable to load configuration {config_path}") from e
    except IsADirectoryError as e:
        raise ConfigLoadError(f"An error occurred {e}") from e
