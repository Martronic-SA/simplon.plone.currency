from setuptools import setup, find_packages
import os

version = '3.0.1'

setup(name='simplon.plone.currency',
      version=version,
      description="Solgema",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Solgema',
      author='Martronic SA',
      author_email='martronic@martronic.ch',
      url='http://www.martronic.ch/plone_products/martronic.Solgema',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplon', 'simplon.plone'],
      package_data = {
        '': ['*.txt', '*.rst', '*.zcml', '*.xml', '*.pot', '*.po', '*.sh', '*.mo'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
