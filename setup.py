from setuptools import setup, find_packages

setup(
    name="maxgram",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.6.0",
    ],
    author="Ruslan Kayumov",
    author_email="",
    description="Python клиент для API бота Max",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kayumovru/maxgram",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 