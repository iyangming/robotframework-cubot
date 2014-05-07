#!/usr/bin/env python

from distutils.core import setup

setup(name='robotframework-cubot',
      version='0.1',
      description='Script for RobotFramework to process and execute cucumber .feature files',
      author='Maurice Koster',
      author_email='maurice@mauricekoster.com',
      scripts=['scripts/cubot.py'],
      install_requires=[
          'colorama',
      ],
     )
