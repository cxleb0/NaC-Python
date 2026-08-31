from pathlib import Path

from modules.exceptions import ConfigLoadError

# file_path = Path("/home/t0rment/Documents/NaC-python/configs/config1.xml")


# BASE_DIR = Path(__file__).resolve().parent.parent
# CONFIG_FILE = BASE_DIR / "configs" / "config2.xml"
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
