#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="Text Reader From Image",
    version="1.0.0",
    description="GUI for reading text from an image",
    author="Julia Bała Dawid Wojdylak Tomasz Madej",
    url="https://github.com/dawidwojdylak/AO_Projekt",
    install_requires=['PyQt5','opencv-python-headless'],
    packages = find_packages(),
    package_data={'src': ['logo/exit-icon.png']},
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'text-reader = src.main:main'
        ]
    }
)
