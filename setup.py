from setuptools import setup, find_packages

setup(
    name="simple_database",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "blist",
        "Pillow",
    ],
    python_requires=">=3.6",
)
