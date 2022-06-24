import pytest

from csc_docker_pool.skeleton import main

__author__ = "maso"
__copyright__ = "maso"
__license__ = "MIT"


def test_main(capsys):
    """CLI relay list"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["relay", "list"])
    captured = capsys.readouterr()
    assert "name" in captured.out
    assert "network" in captured.out
    assert "is_initialized" in captured.out
