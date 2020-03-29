import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alphareader", # Replace with your own username
    version="0.0.5",
    author="Herminio Vazquez",
    author_email="canimus@gmail.com",
    description="A reader for large files with custom delimiters and encodings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canimus/alphareader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
)