from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="vagus",
    version="0.2.1",
    description="The Neural Interface for your Terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Naveen Chandar J",
    url="https://github.com/naverdocker/vagus",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
        install_requires=[
            "litellm~=1.80",
        ],
        extras_require={
            "rag": [
                "chromadb~=1.3",
                "pypdf~=6.0",
                "sentence-transformers~=5.1"
            ],
            "dev": [
                "pytest~=8.0",
                "pytest-mock~=3.0"
            ]
        },
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
