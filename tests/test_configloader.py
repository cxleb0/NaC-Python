#!/usr/bin/env python3
import pytest
from pathlib import Path
from modules.loader import load_config
from modules.exceptions import ConfigLoadError

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "tests" / "fixtures" / "test.xml"

def test_configloader():
    content = load_config(CONFIG_FILE)
    assert isinstance(content, str)
    assert len(content) > 0

    missing = Path("testxml.xml")
    with pytest.raises(ConfigLoadError):
        load_config(missing)
