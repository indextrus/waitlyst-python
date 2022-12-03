from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
]

setup(
    name="waitlyst-python",
    version="0.0.1",
    author="Aaron Kazah",
    author_email="aaron@indextrus.com",
    description="The easiest way to track product-analytics using python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/indextrus/waitlyst-python/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)