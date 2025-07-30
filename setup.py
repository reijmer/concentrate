from setuptools import setup, find_packages

setup(
    name="concentrate",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "concentrate": ["blocked_sites.txt"],
    },
    entry_points={
        "console_scripts": [
            "concentrate = concentrate.cli:main",
        ],
    },
)
