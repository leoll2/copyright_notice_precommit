#!/usr/bin/env python

"""Utility functions"""

import subprocess
from typing import Any, Optional, Set


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    """
    Execute a command in a subprocess, check the exit code and return the stdout.

    :param cmd: Command to execute
    :param retcode: Expected exit code
    :param kwargs: Keyword args for the command
    :return: Stdout as string
    :raises RuntimeError: if the command failed or returned with an unexpected code
    """
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise RuntimeError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def added_files() -> Set[str]:
    """
    Get the set of Git added files in the staging area.

    :return: Set of added staged file paths
    """
    cmd = ("git", "diff", "--staged", "--name-only", "--diff-filter=A")
    return set(cmd_output(*cmd).splitlines())


def parse_file_as_bytes(filepath: str) -> bytes:
    """
    Read a file as raw bytes.

    :param filepath: Path to the file
    :return: Bytes contained in the file
    """
    with open(filepath, "rb") as fpath:
        return fpath.read()
