import pytest
import subprocess
from modules.git import get_diff

def test_get_diff():
    difference = get_diff("50c6d29","71de3d5","../configs/config2.xml")
    assert len(difference) > 0
    assert isinstance(difference, str)
    assert "Allow DHCP" in difference
    assert "Test Rule" in difference

def test_invalid_oldconfig():
    with pytest.raises(subprocess.CalledProcessError):
        get_diff("invalid","71de3d5","../configs/config2.xml")

def test_invalid_newconfig():
     with pytest.raises(subprocess.CalledProcessError):
        get_diff("50c6d29","invalid","../configs/config2.xml")


