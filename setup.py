"""
FastAPI Plus
"""

from setuptools import find_packages, setup

setup(
    name='fastapi_plus',
    version='1.0.2.20200831',
    author="szq",
    author_email="zhenqiang.sun@qq.com",
    description='FastAPI项目工程库',
    long_description='这是一个Python FastAPI项目工程库，包含DB、Redis、MongoDB、JSON等工具和基础服务类。',
    url="https://github.com/zhenqiang-sun/fastapi_plus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

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

    # List additional groups of dependencies here
    extras_require={},
)
