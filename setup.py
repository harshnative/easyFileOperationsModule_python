import setuptools

# include additional packages as well - requests , tabulate , json

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyFileShare", # Replace with your own username
    version="0.16",
    author="Harsh Native",
    author_email="Harshnative@gmail.com",
    description="This module to used to quickly add network file sharing capabilities to a python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshnative/easyFileShare_module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)