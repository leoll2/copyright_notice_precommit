#!/usr/bin/env python
# mypy: ignore-errors

"""
Fixtures to generate sample source code files

A generic source file is structured following the layout:
  <preamble>
  <license>
  <body>
where 'preamble' is a section of text preceding the 'license' block (if any),
while 'body' comes right after the 'license'.
Any of these sections can be empty/missing (i.e. null string).
The above sections are assumed to be concatenated;
a line-break is inserted if not already present.
"""
import itertools

import lorem
import pytest

DUMMY_TEXT_1 = ""
DUMMY_TEXT_2 = "\n"
DUMMY_TEXT_3 = "\r\n"
DUMMY_TEXT_4 = """#!/usr/bin python env

# one comment
# another comment
"""
DUMMY_TEXT_5 = """#~!@$%^&*()_+{}:"|<>?[];',/.\\
1234567890
abcdefgh
"""
DUMMY_TEXT_6 = lorem.text()

DUMMY_TEXTS = (
    DUMMY_TEXT_1,
    DUMMY_TEXT_2,
    DUMMY_TEXT_4,
    DUMMY_TEXT_3,
    DUMMY_TEXT_5,
    DUMMY_TEXT_6,
)


@pytest.fixture(params=itertools.product(DUMMY_TEXTS, DUMMY_TEXTS))
def source_code_with_notice(notice_cpy, request):  # type: ignore
    preamble: str = request.param[0]
    body: str = request.param[1]
    post_preamble_lb = "\n" if not preamble.endswith("\n") else ""
    post_notice_lb = "\n" if not notice_cpy.endswith("\n") else ""
    yield preamble + post_preamble_lb + notice_cpy + post_notice_lb + body, notice_cpy


@pytest.fixture
def source_code_with_notice_as_files(source_code_with_notice, tmp_path):  # type: ignore
    source_code, notice = source_code_with_notice
    source_code_path = tmp_path / "source_code.py"
    notice_path = tmp_path / "source_code_notice.txt"
    source_code_path.write_text(source_code)
    notice_path.write_text(notice)
    yield source_code_path, notice_path
