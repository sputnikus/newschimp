#!/usr/bin/env python
from setuptools import setup

setup(
    name='NewsChimp',
    packages=['newschimp', 'newschimp.social'],
    version='0.1.1',
    description='Newsletter generator for MailChimp',
    long_description=open('README.md').read(),
    author='Martin Putniorz',
    author_email='mputniorz@gmail.cpm',
    url='https://github.com/sputnikus/newschimp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
    ],
    install_requires=[
        'Jinja2>=2.7',
        'PyYAML>=3.11',
        'click>=2.0',
        'lxml>=3.3',
        'mailchimp>=2.0',
        'requests>=2.3',
        'selenium>=2.42',
        'smartypants>=1.8',
        'typogrify>=2.0',
    ],
    scripts=['bin/chimpgen'],
    license='BSD',
    keywords = ['newsletter', 'mail', 'mailchimp']
)
