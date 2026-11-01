import subprocess

import pytest

from modules.git import get_file_at_revision


def test_get_file_at_revision():
    content = get_file_at_revision("71de3d5", "configs/config2.xml")
    assert isinstance(content, str)
    assert len(content) > 0
    assert "Allow Web" in content


def test_get_file_at_revision_invalid_revision():
    with pytest.raises(subprocess.CalledProcessError):
        get_file_at_revision("invalid_revision", "configs/config2.xml")


def test_get_file_at_revision_invalid_file():
    with pytest.raises(subprocess.CalledProcessError):
        get_file_at_revision("71de3d5", "configs/nonexistent.xml")
