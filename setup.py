"""
FastAPI Plus
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi_plus",
    version='0.0.3.20200906',
    author="Zhenqiang Sun",
    author_email="zhenqiang.sun@gmail.com",
    description="This is a Python FastAPI project engineering library that includes tools and basic service classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhenqiang-sun/fastapi_plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'fastapi==0.61.1',
        'uvicorn==0.11.8',
        'SQLAlchemy==1.3.19',
        'PyMySQL==0.10.0',
        'sqlacodegen==2.3.0',
        'redis==3.5.3',
        'pymongo==3.11.0',
        'requests==2.24.0',
        'python-multipart==0.0.5',
        'aiofiles==0.5.0'
    ],
)
