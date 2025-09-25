from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docx-json-replacer",
    version="0.5.1",
    author="liuspatt",
    description="Replace template placeholders in DOCX files with JSON data, supports tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuspatt/docx-json-replacer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "python-docx>=0.8.11",
        "docxtpl>=0.20.0",
    ],
    entry_points={
        "console_scripts": [
            "docx-json-replacer=docx_json_replacer.cli:main",
        ],
    },
)