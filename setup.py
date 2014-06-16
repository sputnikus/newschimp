#!/usr/bin/env python
from setuptools import setup

setup(
    name='NewsChimp',
    version='0.1',
    description='Newsletter generator for MailChimp',
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
    scripts=['bin/_loader', 'bin/chimpgen'],
    license='BSD',
    keywords = ['newsletter', 'mail', 'mailchimp']
)
