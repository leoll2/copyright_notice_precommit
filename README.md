## copyright-notice-precommit

[![GitHub](https://img.shields.io/github/license/leoll2/copyright_notice_precommit)](https://opensource.org/licenses/MIT)
[![PyPI - Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/leoll2/copyright_notice_precommit.svg?branch=main)](https://travis-ci.com/leoll2/copyright_notice_precommit)
[![codecov](https://codecov.io/gh/leoll2/copyright_notice_precommit/branch/main/graph/badge.svg?token=6F45J0MPOD)](https://codecov.io/gh/leoll2/copyright_notice_precommit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/leoll2/copyright_notice_precommit/main.svg)](https://results.pre-commit.ci/latest/github/leoll2/copyright_notice_precommit/main)
[![Code quality: Inspector](https://www.code-inspector.com/project/28978/status/svg)](https://www.code-inspector.com/public/project/28978/copyright_notice_precommit/dashboard)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a [pre-commit](https://pre-commit.com/) hook to make sure you don't forget adding the copyright notice when committing a (new) file.

### Usage

If you haven't installed pre-commit yet, please follow the instructions in the [official website](https://pre-commit.com/#install).

To install this hook, add the following to your `.pre-commit-config.yaml`:
```yaml
-   repo: https://github.com/leoll2/copyright_notice_precommit
    rev: latest
    hooks:
    -   id: copyright-notice
        args: [--notice=copyright.txt]
```
with `--notice` pointing to a template file containing the copyright to match.

*Note: the template file must contain exclusively the copyright notice as text.
It's recommended not to insert extra spaces or linebreaks at the beginning and end of the file.*

### Example

Let's assume this is your copyright notice template file:
```
# Copyright (C) ACME Inc - All Rights Reserved
```
Then, this file will pass the pre-commit check:
```
#!/usr/bin/env python

# Copyright (C) ACME Inc - All Rights Reserved

print("hello world")
```
Conversely, this one shall NOT pass (due to missing notice):
```
#!/usr/bin/env python

print("hello world")
```

### License

This hook is released under the [MIT License](LICENSE).

### Contributing

Do you want to report a bug? Would you like to see new features?
Feel free to open an issue or a pull request. All contributions are welcome!
