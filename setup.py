import setuptools
from pathlib import Path
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_version():
    init_text = Path("mailinator/__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', init_text, re.MULTILINE)
    if not match:
        raise RuntimeError("Unable to find __version__ in mailinator/__init__.py")
    return match.group(1)

setuptools.setup(
    name="mailinator_python_client_2",
    version=read_version(),
    author="Manybrain, LLC",
    author_email="support@manybrain.com",
    description="Official SDK for Mailinator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manybrain/mailinator-python-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.9',
)
