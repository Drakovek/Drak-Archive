import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvk-archive",
    version="0.0.1",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description="Modules for loading and handling .dvk files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/dvk_archive",
    packages=setuptools.find_packages(),
    install_requires=["tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
