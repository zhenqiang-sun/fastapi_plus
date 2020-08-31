"""
FastAPI Utils
"""

from setuptools import find_packages, setup

setup(
    name='fastapi_plus',
    version='1.0.1.20200831',
    author="szq",
    author_email="zhenqiang.sun@qq.com",
    description='FastAPI项目工程库',
    long_description='这是一个Python FastAPI项目工程库，包含DB、Redis、MongoDB、JSON等工具和基础服务类。',
    url="https://gitee.com/erlitech/fastapi_plus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=['fastapi', 'uvicorn', 'sqlalchemy', 'pymysql', 'sqlacodegen', 'redis', 'pymongo', 'requests'],

    # List additional groups of dependencies here
    extras_require={},
)
