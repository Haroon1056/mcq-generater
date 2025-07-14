from setuptools import setup, find_packages

setup(
    name="mcqgen",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "huggingface",
        "langchain",
        "streamlit",
        "python-dotenv",
        "pyPDF2",
        "langchain-huggingface",
    ],
    author="Haroon Rasheed",
    author_email="haroonrasheed1056@gmail.com"
)