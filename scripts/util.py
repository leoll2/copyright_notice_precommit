#!/usr/bin/env python

import subprocess
from typing import Any, Optional, Set


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise RuntimeError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def added_files() -> Set[str]:
    cmd = ("git", "diff", "--staged", "--name-only", "--diff-filter=A")
    return set(cmd_output(*cmd).splitlines())


def parse_file_as_bytes(filepath: str) -> bytes:
    with open(filepath, "rb") as fp:
        return fp.read()
