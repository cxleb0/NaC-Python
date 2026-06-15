#!/usr/bin/env python3
from pathlib import Path

#file_path = Path("/home/t0rment/Documents/NaC-python/configs/config1.xml")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "configs" / "config2.xml"
def load_config():
    with CONFIG_FILE.open('r', encoding='utf-8') as file:
        content = file.read()
    return content


