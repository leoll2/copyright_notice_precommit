## copyright-notice-precommit

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
