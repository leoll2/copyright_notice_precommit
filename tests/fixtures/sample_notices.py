#!/usr/bin/env python
# mypy: ignore-errors

"""Fixtures to generate sample copyright notices"""

import itertools

import pytest

# Note: when writing new dummy test notices, make sure none of them
#   is a prefix string of another one.

NOTICE_TEXT_1 = """Copyright Notice (C) 1970"""

NOTICE_TEXT_2 = """Copyright Notice

This software is distributed under the ACME license.
All rights reserved."""

NOTICE_TEXT_3 = """Copyright (C) ACME Inc - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
Written by Wile E. Coyote <wilecoyote@acme.com>
"""


notice_texts = (
    NOTICE_TEXT_1,
    NOTICE_TEXT_2,
    NOTICE_TEXT_3,
)

assert not any(
    t1 in t2 and t1 != t2 for t1, t2 in itertools.product(notice_texts, notice_texts)
)


@pytest.fixture(params=notice_texts)
def notice(request):
    yield request.param


# Note: make a copy to allow creating two instances of the same fixture
# and avoid aliasing within tests:
# https://stackoverflow.com/questions/36100624/
notice_cpy = notice


@pytest.fixture
def notice_as_file(notice, tmp_path):
    notice_path = tmp_path / "notice.txt"
    notice_path.write_text(notice)
    yield notice_path
