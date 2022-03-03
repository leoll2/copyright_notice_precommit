#!/usr/bin/env python
# mypy: ignore-errors

"""
Unit tests for CopyrightNoticeChecker methods
"""

import sys
from unittest.mock import patch

import pytest
from scripts.copyright_notice import CopyrightNoticeChecker
from scripts.error import (
    CopyrightNoticeParsingError,
    CopyrightNoticeTemplateFileNotFoundError,
    CopyrightNoticeValidationError,
    SourceCodeFileNotFoundError,
    exception_to_retcode_mapping,
)

if sys.version_info >= (3, 7):
    from contextlib import nullcontext


# (
#   mock return for parse_file_as_bytes
#   mock return for file_contains_valid_notice
#   side effect raised by parse_file_as_bytes,
#   side effect raised by file_contains_valid_notice
#   expected return for check_files_have_notice,
#   expected exception raised by check_files_have_notice
# )
check_files_have_notice_test_data = [
    (b"abc", True, None, None, True, None),
    (b"abc", False, None, None, False, None),
    (
        b"abc",
        True,
        FileNotFoundError,
        None,
        None,
        CopyrightNoticeTemplateFileNotFoundError,
    ),
    (b"abc", True, Exception, None, None, CopyrightNoticeParsingError),
    (
        b"abc",
        True,
        None,
        SourceCodeFileNotFoundError,
        None,
        SourceCodeFileNotFoundError,
    ),
    (b"abc", True, None, Exception, None, CopyrightNoticeValidationError),
]

# (
#   mock return for check_files_have_notice,
#   side effect raised by check_files_have_notice,
#   expected return for check_files_have_notice_with_retcode,
# )
check_files_have_notice_with_retcode_test_data = [
    (True, None, 0, False),
    (False, None, 1, False),
    (None, Exception, 255, False),
] + [(None, exc, code, False) for exc, code in exception_to_retcode_mapping.items()]


class TestCopyrightNoticeChecker:
    """Unit tests for CopyrightNoticeChecker methods"""

    @pytest.mark.skipif(
        sys.version_info < (3, 7), reason="contextlib.nullcontex requires Python >= 3.7"
    )
    @pytest.mark.parametrize(
        "mock_return_parse, mock_return_contains, side_effect_parse, "
        "side_effect_contains, expected_return, expected_side_effect",
        check_files_have_notice_test_data,
    )
    def test_check_files_have_notice(
        self,
        mock_return_parse,
        mock_return_contains,
        side_effect_parse,
        side_effect_contains,
        expected_return,
        expected_side_effect,
    ):
        filenames = ["foo.cpp", "bar.py"]
        notice = "copyright.txt"

        if expected_side_effect is not None:
            pytest_raises_ctx = pytest.raises(expected_side_effect)
        else:
            pytest_raises_ctx = nullcontext()

        mock_parse_ctx = patch("scripts.copyright_notice.parse_file_as_bytes")
        mock_contains_ctx = patch.object(
            CopyrightNoticeChecker, "file_contains_valid_notice"
        )

        with mock_parse_ctx as mock_parse_fn, mock_contains_ctx as mock_contains_fn, pytest_raises_ctx:  # noqa: E501
            mock_parse_fn.return_value = mock_return_parse
            mock_contains_fn.return_value = mock_return_contains
            if side_effect_parse is not None:
                mock_parse_fn.side_effect = side_effect_parse(
                    "intentionally raised error"
                )
            if side_effect_contains is not None:
                mock_contains_fn.side_effect = side_effect_contains(
                    "intentionally raised error"
                )

            return_value = CopyrightNoticeChecker.check_files_have_notice(
                filenames=filenames, notice_path=notice, enforce_all=True, autofix=False
            )

            mock_parse_fn.assert_called_once_with(notice)

            assert mock_contains_fn.call_count == 2
            for filename in filenames:
                mock_contains_fn.assert_any_call(filename, mock_return_parse)

            if expected_side_effect is None:
                assert return_value == expected_return

    @pytest.mark.parametrize(
        "mock_return, side_effect, expected_return, autofix",
        check_files_have_notice_with_retcode_test_data,
    )
    def test_check_files_have_notice_with_retcode(
        self,
        mock_return,
        side_effect,
        expected_return,
        autofix,
    ):
        filenames = ["foo.cpp", "bar.py"]
        notice = "copyright.txt"

        with patch.object(CopyrightNoticeChecker, "check_files_have_notice") as mock_fn:
            mock_fn.return_value = mock_return
            if side_effect is not None:
                mock_fn.side_effect = side_effect("intentionally raised error")

            exit_code = CopyrightNoticeChecker.check_files_have_notice_with_retcode(
                filenames=filenames,
                notice_path=notice,
                enforce_all=True,
                autofix=autofix,
            )

            mock_fn.assert_called_once_with(
                filenames=filenames,
                notice_path=notice,
                enforce_all=True,
                autofix=autofix,
            )
            if side_effect is None:
                assert exit_code == expected_return
