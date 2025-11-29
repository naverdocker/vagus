from setuptools import setup, find_packages

setup(
        name="vagus",
        version="0.1.2",
        description="The Neural Interface for your Terminal",
        author="naverdocker",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        install_requires=[
            "litellm",
        ],
        entry_points={
            "console_scripts": [
                "vagus=vagus.main:entry_point",
            ],
        },
)
