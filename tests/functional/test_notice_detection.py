#!/usr/bin/env python
# mypy: ignore-errors

"""
Test the ability of the script to detect copyright notices.
"""

import filecmp

from scripts.copyright_notice import CopyrightNoticeChecker


def show_file_and_notice(source_code_filepath, notice_template_filepath):
    with open(source_code_filepath) as sc, open(notice_template_filepath) as nt:
        print(f"Source code:\n{sc.read()}\n---\nNotice:\n{nt.read()}\n")


class TestNoticeDetection:
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
