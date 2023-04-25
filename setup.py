from setuptools import find_packages, setup

setup(
    name="simple_database",
    version="0.1",
    description="A simple in-memory database with replication support",
    author="Francisco Iago Lira Passos",
    author_email="bosonshiggsteam@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)