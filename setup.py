from setuptools import find_packages, setup

setup(
    name="ransomprotect",
    version="dev-0.1.0",
    packages=find_packages(where="./src"),
    package_dir={"": "src"},
)