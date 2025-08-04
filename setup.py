# qingping - python tools for air monitor
# Copyright (C) 2025  bitrate16 (bitrate16@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Setup for qingping
"""

import os

from setuptools import setup, find_packages


cwd = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='qingping',
    version='0.3',
    py_modules=[ 'qingping' ],
    packages=[ 'qingping' ],
    install_requires=[
        'pygatt',
        'attrs',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    license='GNU Affero General Public License v3',
    author='bitrate16',
    author_email='bitrate16@gmail.com',
    description='Qingping utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bitrate16/qingping',
)
