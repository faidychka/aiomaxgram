from setuptools import setup, find_packages

setup(
    name="aiomaxgram",
    version="0.1.5.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "aiohttp>=3.11",
        "pydantic>=2.6.0",
    ],
    author="Sobolev Faidy",
    author_email="minecraftsobolev@gmail.com",
    description="Python client (unofficial) for MAX API. Early version for Async version.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/faidychka/aiomaxgram",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
) 