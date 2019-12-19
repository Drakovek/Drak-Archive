import setuptools

console_scripts = [
    "dvk-same-ids = dvk_archive.error.same_ids:main",
    "dvk-unlinked = dvk_archive.error.unlinked:main",
    "dvk-missing-media = dvk_archive.error.missing_media:main",
    "dvk-rename = dvk_archive.reformat.rename_files:main"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvk-archive",
    version="0.1.8",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description="Modules for loading and handling .dvk files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/dvk_archive",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "requests",
        "selenium",
        "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    entry_points={"console_scripts": console_scripts}
)
