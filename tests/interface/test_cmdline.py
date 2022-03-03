#!/usr/bin/env python
# mypy: ignore-errors

"""
Test command-line options parsing
"""
import os
import shlex
from pathlib import Path
from typing import List, Sequence
from unittest.mock import patch

from scripts.copyright_notice import CopyrightNoticeChecker, main


class TestCmdline:
    """Test the behavior of the entry-point argument parser"""

    @staticmethod
    def _build_cmd(files: Sequence[str], options: Sequence[str]) -> List[str]:
        files = list(files)
        options = list(options)
        return shlex.split(" ".join(options + files), posix=(os.name != "nt"))

    @staticmethod
    def _test_call(
        files: Sequence[str],
        options: Sequence[str],
        *expected_call_args,
        **expected_call_kwargs,
    ):
        args = TestCmdline._build_cmd(files, options)

        with patch.object(
            CopyrightNoticeChecker, "check_files_have_notice_with_retcode"
        ) as mock_fn:
            mock_fn.return_value = 0

            main(args)

            mock_fn.assert_called_once_with(*expected_call_args, **expected_call_kwargs)

    def test_no_options(self, file_paths):
        options = []

        TestCmdline._test_call(
            file_paths,
            options,
            list(file_paths),
            "copyright.txt",
            enforce_all=False,
            autofix=False,
        )

    def test_with_notice(self, file_paths):
        notice_file = "mynotice.txt"
        options = [f"--notice={notice_file}"]

        TestCmdline._test_call(
            file_paths,
            options,
            list(file_paths),
            notice_file,
            enforce_all=False,
            autofix=False,
        )

    def test_with_enforce_all(self, file_paths):
        options = ["--enforce-all"]

        TestCmdline._test_call(
            file_paths,
            options,
            list(file_paths),
            "copyright.txt",
            enforce_all=True,
            autofix=False,
        )

    def test_autofix_empty_file(self):
        this_init = Path(__file__).parent / "__init__.py"
        notice = Path(__file__).parent.parent / "fixtures" / "notice.txt"
        assert CopyrightNoticeChecker.check_files_have_notice(
            filenames=[str(this_init)],
            notice_path=str(notice),
            enforce_all=True,
            autofix=True,
        )
        with open(this_init, encoding="utf8") as init:
            content = init.read()

        assert "Wile E. Coyote" not in content

    def test_autofix_basic(self, tmp_path):
        file_to_autofix = tmp_path / "file_to_autofix.py"
        with open(file_to_autofix, "w", encoding="utf8") as fta:
            fta.write("a = 42")
        notice = Path(__file__).parent.parent / "fixtures" / "notice.txt"
        CopyrightNoticeChecker.check_files_have_notice(
            filenames=[str(file_to_autofix)],
            notice_path=str(notice),
            enforce_all=True,
            autofix=True,
        )
        with open(file_to_autofix, encoding="utf8") as fta:
            content = fta.read()
        assert "Wile E. Coyote" in content
