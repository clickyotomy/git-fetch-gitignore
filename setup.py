#! /usr/bin/env python2.7

'''
Installs fetch-gitignore.
'''

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README')) as f:
    LONG_DESC = f.read()

setup(
    name='git-fetch-gitignore',
    version='0.0.1',
    description='Fetch .gitignore files from GitHub',
    long_description=LONG_DESC,
    url='https://github.com/clickyotomy/git-fetch-gitignore',
    author='Srinidhi Kaushik',
    author_email='clickyotomy@users.noreply.github.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='git .gitignore',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests'],
    include_package_data=True,
    data_files=[
        ('/usr/local/man/man1/git-fetch-gitignore.1',
         ['./git-fetch-gitignore.1'])
    ],
    scripts=['bin/git_fetch_gitignore.py'],
    entry_points={
        'console_scripts': [
            "git-fetch-gitignore=bin.git_fetch_gitignore:main",
        ],
    },
)
