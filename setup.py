#!/usr/bin/env python3

"""
Setuptools setup file.
"""

import setuptools

console_scripts = ["dvk-archive-test = dvk_archive.test.all_tests:main",
                   "dvk-rename = dvk_archive.main.file.rename:main",
                   "dvk-reformat = dvk_archive.main.file.reformat:main",
                   "dvk-missing-media = dvk_archive.main.error_finding.missing_media:main",
                   "dvk-unlinked = dvk_archive.main.error_finding.unlinked_media:main",
                   "dvk-same-ids = dvk_archive.main.error_finding.same_ids:main"]

with open("README.md", "r") as fh:
    long_description = fh.read()

desc = "Utility for loading and handling media files in the DVK file format."

setuptools.setup(
    name="dvk-archive",
    version="0.10.0",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/dvk_archive",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4",
        "filetype",
        "lxml",
        "requests",
        "selenium",
        "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.0',
    entry_points={"console_scripts": console_scripts}
)
