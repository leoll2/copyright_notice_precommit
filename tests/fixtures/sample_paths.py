#!/usr/bin/env python
# mypy: ignore-errors

"""Fixtures to generate sample file-system paths"""
import os
from sys import platform

import pytest

DUMMY_FILE_1 = "foo.txt"
DUMMY_FILE_2 = "bar.py"
DUMMY_FILE_3 = "README.md"
DUMMY_FILE_4 = ".DS_Store"
DUMMY_FILE_5 = "some-very_long-and_weird-file_name-that_is-long_65-characters.exe"

DUMMY_FOLDER_1 = "home"
DUMMY_FOLDER_2 = ".cache"

DUMMY_PATHS_COMMON = (
    os.path.join(DUMMY_FOLDER_1, DUMMY_FILE_1),
    os.path.join(DUMMY_FOLDER_1, DUMMY_FILE_2),
    os.path.join(DUMMY_FOLDER_2, DUMMY_FILE_3),
    os.path.join(DUMMY_FOLDER_2, DUMMY_FILE_4),
    os.path.join(DUMMY_FOLDER_1, DUMMY_FOLDER_2, DUMMY_FILE_4),
    os.path.join(DUMMY_FOLDER_2, DUMMY_FOLDER_1, DUMMY_FILE_5),
)

DUMMY_PATHS_WIN_ABS = tuple(
    "C:" + os.sep + dummy_path for dummy_path in DUMMY_PATHS_COMMON
)
DUMMY_PATHS_WIN = DUMMY_PATHS_WIN_ABS + DUMMY_PATHS_COMMON

DUMMY_PATHS_UNIX_ABS = tuple(os.sep + dummy_path for dummy_path in DUMMY_PATHS_COMMON)
DUMMY_PATHS_UNIX_EXTRA = ("./foo", "../bar.txt", "a//b/./../c.py")
DUMMY_PATHS_UNIX = DUMMY_PATHS_UNIX_ABS + DUMMY_PATHS_UNIX_EXTRA + DUMMY_PATHS_COMMON


@pytest.fixture
def file_path():
    def _get_path(idx: int = 0) -> str:
        if platform in ("linux", "linux2", "darwin"):  # Linux or OS-X
            return DUMMY_PATHS_UNIX[idx % len(DUMMY_PATHS_UNIX)]
        elif platform == "win32":  # Windows
            return DUMMY_PATHS_WIN[idx % len(DUMMY_PATHS_WIN)]
        else:
            raise RuntimeError(f"Unsupported platform: {platform}")

    yield _get_path


@pytest.fixture
def file_paths():
    if platform in ("linux", "linux2", "darwin"):  # Linux or OS-X
        yield DUMMY_PATHS_UNIX
    elif platform == "win32":  # Windows
        yield DUMMY_PATHS_WIN
    else:
        raise RuntimeError(f"Unsupported platform: {platform}")
