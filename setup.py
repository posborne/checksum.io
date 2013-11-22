import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='checksumio',
      version='0.0',
      description='checksumio',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      package_dir={'checksumio': 'src/checksumio'},
      packages=find_packages("src"),
      include_package_data=True,
      zip_safe=False,
      test_suite='checksumio',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = checksumio:main
      [console_scripts]
      initialize_checksumio_db = checksumio.scripts.initializedb:main
      """,
      )
