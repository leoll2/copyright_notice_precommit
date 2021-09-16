#!/usr/bin/env python

"""Errors and exceptions"""

import logging
from typing import Dict, Type


class CopyrightNoticeTemplateFileNotFoundError(FileNotFoundError):
    """Copyright notice template file not found"""

    def __init__(self, filepath: str):
        msg = f"Copyright notice template not found at: {filepath}"
        logging.error(msg)
        super().__init__(msg)


class SourceCodeFileNotFoundError(FileNotFoundError):
    """Source code file not found"""

    def __init__(self, filepath: str):
        msg = f"Source code file not found at: {filepath}"
        logging.error(msg)
        super().__init__(msg)


class CopyrightNoticeParsingError(RuntimeError):
    """Error while parsing the copyright notice file"""

    def __init__(self, filepath: str, reason: str = ""):
        msg = f"Failed to parse copyright notice at: {filepath}. Reason: {reason}"
        logging.error(msg)
        super().__init__(msg)


class CopyrightNoticeValidationError(RuntimeError):
    """Error while checking the code for a copyright notice"""

    def __init__(self, filepath: str, reason: str = ""):
        msg = f"Failed to parse copyright notice at: {filepath}. Reason: {reason}"
        logging.error(msg)
        super().__init__(msg)


exception_to_retcode_mapping: Dict[Type[Exception], int] = {
    # success (notice found in file): 1
    # failure (notice not found in file): 2
    CopyrightNoticeTemplateFileNotFoundError: 3,
    SourceCodeFileNotFoundError: 4,
    CopyrightNoticeParsingError: 5,
    CopyrightNoticeValidationError: 6,
}
