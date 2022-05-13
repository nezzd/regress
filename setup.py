import setuptools

with open("README.md", "r") as d:
    long_description = d.read()

setuptools.setup(
    name="decision",
    version="0.1.0",
    author="Nicolò Giannini",
    author_email="nicogiannini@yahoo.com",
    description="Decision tree from scratch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicologiannini/decision-kit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)