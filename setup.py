import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mu-auth-sudo",
    version="0.0.1",
    author="Michaël Dierick",
    author_email="michael.dierick@redpencil.io",
    description="sparql with mu-auth-sudo helpers for mu-python-template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        "SPARQLWrapper",
        "flask"
    ],
    url="https://github.com/MikiDi/python-mu-auth-sudo",
    packages=setuptools.find_packages(),
    keywords = ["mu.semte.ch", "semantic.works", "mu-authorization", "mu-auth-sudo", "sparql"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
