#!/usr/bin/env python

"""Entry point and core logic of the copyright-notice-precommit"""

import argparse
import logging
import mmap
import os.path
import sys
from typing import Optional, Sequence

from scripts.error import (
    CopyrightNoticeParsingError,
    CopyrightNoticeTemplateFileNotFoundError,
    CopyrightNoticeValidationError,
    SourceCodeFileNotFoundError,
    exception_to_retcode_mapping,
)

from .util import added_files, parse_file_as_bytes


class CopyrightNoticeChecker:
    """Copyright notice checker for source code files"""

    @staticmethod
    def file_contains_valid_notice(filepath: str, notice_pattern: bytes) -> bool:
        """
        Check if a file contains the required copyright notice.

        :param filepath: Path to the file to check
        :param notice_pattern: Bytes representation of the copyright notice
        :return: Bool indicating if the file contains a valid copyright notice or not
        """
        if not os.path.exists(filepath):
            raise SourceCodeFileNotFoundError(filepath)
        ret = False
        with open(filepath, "rb", 0) as f_src, mmap.mmap(
            f_src.fileno(), 0, access=mmap.ACCESS_READ
        ) as src_bytes:
            found_pos = src_bytes.find(notice_pattern)
            if found_pos != -1:
                ret = True
        logging.debug("File: %s  NoticePos: %d", filepath, found_pos)
        return ret

    @staticmethod
    def check_files_have_notice(
        filenames: Sequence[str], notice_path: str, *, enforce_all: bool = False
    ) -> bool:
        """
        Check if a set of files contains the required copyright notice.

        Returns a bool.

        :param filenames: List of file paths to check
        :param notice_path: Path to the copyright notice template
        :param enforce_all: If False, checks only added staged files
        :return: Bool indicating if all the files contains a copyright notice or not
        :raises SourceCodeFileNotFoundError:
            if one of the files to validate is not found at the given path
        :raises CopyrightNoticeTemplateFileNotFoundError:
            if the copyright notice template file is not found at the given path
        :raises CopyrightNoticeParsingError:
            if the copyright notice template file cannot be parsed correctly
        :raises CopyrightNoticeValidationError:
            if an error occurs while validating a file
        """
        # Load notice
        try:
            notice_pattern = parse_file_as_bytes(notice_path)
        except FileNotFoundError as exc:
            raise CopyrightNoticeTemplateFileNotFoundError(notice_path) from exc
        except Exception as exc:
            raise CopyrightNoticeParsingError(notice_path, str(exc)) from exc

        # Define the set of files to check
        filepaths_filtered = set(filenames)
        if not enforce_all:
            filepaths_filtered &= added_files()

        # Iterate over the files to check
        ret = True
        for filepath in filepaths_filtered:
            try:
                if not CopyrightNoticeChecker.file_contains_valid_notice(
                    filepath, notice_pattern
                ):
                    logging.warning(
                        "File %s does not contain a valid copyright notice.", filepath
                    )
                    ret = False
            except Exception as exc:
                raise CopyrightNoticeValidationError(notice_path, str(exc)) from exc
        return ret

    @staticmethod
    def check_files_have_notice_with_retcode(
        filenames: Sequence[str], notice_path: str, *, enforce_all: bool = False
    ) -> int:
        """
        Check if a set of files contains the required copyright notice.

        Returns an appropriate exit code.

        :param filenames: List of file paths to check
        :param notice_path: Path to the copyright notice template
        :param enforce_all: If False, checks only added staged files
        :return: unsigned exit code (0 for success)
        """
        try:
            has_notice = CopyrightNoticeChecker.check_files_have_notice(
                filenames=filenames, notice_path=notice_path, enforce_all=enforce_all
            )
            return 0 if has_notice else 1
        except Exception as exc:  # pylint: disable=broad-except
            return exception_to_retcode_mapping.get(exc.__class__, 255)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """copyright-notice-precommit entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--notice",
        default="copyright.txt",
        help="Path to a file containing the copyright notice to match.",
    )
    parser.add_argument(
        "--enforce-all",
        action="store_true",
        help="Enforce all files are checked, not just staged files.",
    )
    args = parser.parse_args(argv)

    return CopyrightNoticeChecker.check_files_have_notice_with_retcode(
        args.filenames, args.notice, enforce_all=args.enforce_all
    )


if __name__ == "__main__":
    sys.exit(main())
