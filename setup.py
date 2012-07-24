import os
from setuptools import setup, find_packages

f = open('README.rst', 'r')
long_description = f.read()
f.close()

setup(name="van.resumelb",
      version='0.5',
      license='BSD-derived',
      long_description=long_description,
      url='http://pypi.python.org/pypi/van.resumelb',
      author_email='brian@vanguardistas.net',
      packages=find_packages(),
      author="Vanguardistas LLC",
      description="Pool class for zc.resumelb which divides workers by version",
      test_suite="van.resumelb.tests",
      namespace_packages=["van"],
      tests_require=['zc-zookeeper-static'],
      install_requires=[
          'setuptools',
          'zc.resumelb',
          ],
      include_package_data = True,
      )
