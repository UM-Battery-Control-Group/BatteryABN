import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="batteryabn",
    version="0.0.1",
    author="Ziyi Liu, UMBCLab",
    author_email="ziyiliu@umich.edu",
    description="A Python module for parsing and analyzing battery data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YiLiiu/BatteryABN",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9, <3.12',
    license='MIT',
)
