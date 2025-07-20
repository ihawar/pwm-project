from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="pwm",
    version="1.0.1",
    description="A terminal password manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="hawar",
    author_email="iaramkhzri@gmail.com",

    license="GPLv3",
    python_requires=">=3.8",

    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0"
    ],

    entry_points={
        'console_scripts': [
            'pwm = pwm.main:main'
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography"
    ],
)
