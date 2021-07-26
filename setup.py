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
    version="0.1.0",
    description="diff commits to your kedro pipeline",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Framework :: kedro",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    url="https://github.com/WaylonWalker/kedro-diff",
    packages=find_packages(),
    platforms="any",
    license="OSI APPROVED :: MIT LICENSE",
    author="Waylon Walker",
    keywords="pipelines, machine learning, data pipelines, data science, data engineering",
    install_requires=requires,
    extras_require={"dev": dev_requires},
    entry_points={
        "kedro.project_commands": ["kedro-diff = kedro_diff.cli:cli"],
        "console_scripts": ["kedro-diff = kedro_diff.cli:cli"],
    },
)
