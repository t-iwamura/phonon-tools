from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phonon_tools",
    version="1.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description="Useful tools to perform phonon calculation by DFT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwamura-lab/phonon-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">= 3.9",
    install_requires=[
        "dataclasses_json",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "phonon-tools=phonon_tools.scripts.main:main",
        ],
    },
)
