#!/usr/bin/env python3
"""
Nexus Programming Language - Installation Setup
Allows system-wide installation: just run 'nexus' command
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="nexus-lang",
    version="1.0.0",
    description="A completely original programming language with unique syntax and paradigms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nexus Community",
    author_email="dev@nexus-lang.dev",
    url="https://github.com/nekocd10/maybe-a-custom-language",
    license="MIT",
    
    py_modules=[
        "nexus_cli",
        "nexus_interpreter",
        "nexus_lexer",
        "nexus_parser",
        "nxs_pm",
        "nxs_frontend",
        "nxs_backend",
        "nxs_build",
        "nxs_interop"
    ],
    
    entry_points={
        "console_scripts": [
            "nexus=nexus_cli:main",
            "nxs=nxs_pm:main"
        ]
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Compilers",
        "Topic :: Internet :: WWW/HTTP",
    ],
    
    python_requires=">=3.8",
    
    project_urls={
        "Documentation": "https://github.com/nekocd10/maybe-a-custom-language/blob/main/README.md",
        "Source": "https://github.com/nekocd10/maybe-a-custom-language",
        "Tracker": "https://github.com/nekocd10/maybe-a-custom-language/issues",
    },
)
