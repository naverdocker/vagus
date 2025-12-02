from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="vagus",
    version="0.1.3",
    description="The Neural Interface for your Terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Naveen Chandar J",
    url="https://github.com/naverdocker/vagus",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "litellm",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "vagus=vagus.main:entry_point",
        ],
    },
)