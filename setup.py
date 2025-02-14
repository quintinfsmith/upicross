import setuptools
from upicross import __version__, __author__, __email__, __url__, __license__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upicross",
    version=__version__,
    description="Very simple in-console implementation of picross.",
    author="Quintin Smith",
    author_email="smith.quintin@protonmail.com",
    install_requires=['wrecked'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=__license__,
    keywords=[],
    python_requires="~=3.7",
    entry_points={ "console_scripts": ["upicross = upicross.__main__:main"] },
    url=__url__,
    packages=['upicross'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ]
)
