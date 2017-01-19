#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''The program renders a pipeline diagram from a YAML file'''


setup(
    name='pipeline_yaml-py',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['pipeline_yaml'],
    package_dir={'pipeline_yaml': 'pipeline_yaml'},
    entry_points={
        'console_scripts': ['pipeline_yaml-py = pipeline_yaml.pipeline_yaml:main']
    },
    url='https://github.com/bjpop/pipeline_yaml',
    license='LICENSE',
    description=('A prototypical bioinformatics command line tool'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["yaml"],
)
