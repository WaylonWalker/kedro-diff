"""
kedro-diff uses setup tools for packaging.

To Build kedro-diff as a Python package

    $ python setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

Regular install

    $ pip install -e .

To setup local Development

    $ pip install -e ".[dev]"

"""
from pathlib import Path

from setuptools import find_packages, setup

NAME = "kedro-diff"

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

with open("requirements_dev.txt", "r", encoding="utf-8") as f:
    dev_requires = [x.strip() for x in f if x.strip()]

setup(
    name=NAME,
    version="0.0.0",
    url="https://github.com/WaylonWalker/kedro-diff",
    packages=find_packages(),
    platforms="any",
    license="MIT",
    install_requires=requires,
    extras_require={"dev": dev_requires},
    entry_points={
        # "kedro.global_commands": ["kedro-diff = kedro_diff.cli:cli"],
        "kedro.project_commands": ["kedro-diff = kedro_diff.cli:cli"],
        # "kedro.cli_hooks": ["kedro-diff = kedro_diff.cli:cli_hooks"],
        "console_scripts": ["kedro-diff = kedro_diff.cli:cli"],
    },
)
