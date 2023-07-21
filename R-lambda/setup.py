import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="r-lambda",
    version="0.0.1",
    author="xieguigang",
    author_email="xie.guigang@gcmodeller.org",
    packages=["r-lambda"],
    description="A simple package for call a target R# function from commandline",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsharp-lang/IronR",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)