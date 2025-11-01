from setuptools import setup, find_packages

setup(
    name="pdf-manager",
    version="0.1.0",
    description="A CLI tool for managing PDF files",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "reportlab>=3.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-manager=pdf_manager.cli:main",
        ],
    },
    python_requires=">=3.7",
)