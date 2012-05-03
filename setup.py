from setuptools import setup, find_packages
import sys, os


version = '0.1'
project = 'kotti_navigation'

tests_require = [
    'WebTest',
    'mock',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'wsgi_intercept',
    'zope.testbrowser',
    ]

setup(name=project,
      version=version,
      description="Navigation widget for Kotti",
      long_description="""\
This is an extension to the Kotti CMS that renders a navigation in the
left or right slot.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='kotti addon',
      author='Marco Scheidhuber',
      author_email='marco@jusid.de',
      url='http://jusid.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Kotti>=0.6.2',
      ],
      tests_require=tests_require,
      entry_points="""
      # -*- Entry points: -*-
      """,
      extras_require={
          'testing': tests_require,
          },
      message_extractors={'kotti_navigation': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )
