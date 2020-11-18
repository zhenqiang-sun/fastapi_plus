"""
FastAPI Plus
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi_plus",
    version='0.1.1.20201118',
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
        'fastapi==0.61.2',
        'uvicorn==0.12.2',
        'sqlalchemy==1.3.19',
        'pymysql==0.10.0',
        'sqlacodegen==2.3.0',
        'redis==3.5.3',
        'pymongo==3.11.1',
        'requests==2.25.0',
        'python-multipart==0.0.5',
        'aiofiles==0.6.0'
    ],
)
