#!/usr/bin/env python
# mypy: ignore-errors

"""
Test the ability of the script to detect copyright notices.
"""

import filecmp
import os
from unittest.mock import patch

import pytest
from scripts.copyright_notice import CopyrightNoticeChecker
from scripts.error import (
    CopyrightNoticeParsingError,
    CopyrightNoticeTemplateFileNotFoundError,
    CopyrightNoticeValidationError,
    SourceCodeFileNotFoundError,
)


def show_file_and_notice(source_code_filepath, notice_template_filepath):
    with open(source_code_filepath) as src, open(notice_template_filepath) as ntc:
        print(f"Source code:\n{src.read()}\n---\nNotice:\n{ntc.read()}\n")


class TestNoticeDetection:
    """Test detection of copyright notices in files"""

    def test_detect_notice_in_code(
        self, notice_as_file, source_code_with_notice_as_files
    ):
        (
            source_code_full_path,
            source_code_notice_path,
        ) = source_code_with_notice_as_files
        should_be_found = filecmp.cmp(source_code_notice_path, notice_as_file)
        print(should_be_found)
        assert (
            CopyrightNoticeChecker.check_files_have_notice(
                filenames=[source_code_full_path],
                notice_path=notice_as_file,
                enforce_all=True,
            )
            == should_be_found
        ), show_file_and_notice(source_code_full_path, notice_as_file)

    def test_missing_notice(self, source_code_once_as_file):
        notice_path = "/nonexisting/path"
        with pytest.raises(CopyrightNoticeTemplateFileNotFoundError):
            CopyrightNoticeChecker.check_files_have_notice(
                filenames=[source_code_once_as_file],
                notice_path=notice_path,
                enforce_all=True,
            )

    def test_missing_source_file(self, notice_once_as_file):
        source_code_path = "/nonexisting/path"
        with pytest.raises(SourceCodeFileNotFoundError):
            CopyrightNoticeChecker.check_files_have_notice(
                filenames=[source_code_path],
                notice_path=notice_once_as_file,
                enforce_all=True,
            )

    @pytest.mark.skipif(os.name == "nt", reason="chmod not fully supported in Windows")
    def test_unreadable_notice(
        self, source_code_once_as_file, notice_unreadable_once_as_file
    ):
        with pytest.raises(CopyrightNoticeParsingError):
            CopyrightNoticeChecker.check_files_have_notice(
                filenames=[source_code_once_as_file],
                notice_path=notice_unreadable_once_as_file,
                enforce_all=True,
            )

    def test_validation_error(self, source_code_once_as_file, notice_once_as_file):
        with patch.object(
            CopyrightNoticeChecker, "file_contains_valid_notice"
        ) as mock_fn:
            mock_fn.side_effect = Exception("intentionally raised from mocked method")

            with pytest.raises(CopyrightNoticeValidationError):
                CopyrightNoticeChecker.check_files_have_notice(
                    filenames=[source_code_once_as_file],
                    notice_path=notice_once_as_file,
                    enforce_all=True,
                )
