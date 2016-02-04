from setuptools import setup, find_packages

import os

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "magum", "__about__.py")) as f:
    exec(f.read(), about)

"""readme = os.path.join(base_dir, 'README.rst')
with open(readme) as f:
        long_description = f.read()
"""
CFFI_VERSION = '1.1.0'

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__summary__'],
      long_description=about['__longdescription__'],
      keywords=about['__keywords__'],
      url=about['__uri__'],
      author=about['__author__'],
      author_email=about['__email__'],
      license=about['__license__'],
      classifiers=[
      	'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Intended Audience :: Udooers',
        'Intended Audience :: embedded computing developement',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Hardware',
        'Topic :: System :: Sensors',
      ],
      packages=['magum'],
      install_requires=['cffi >= ' + CFFI_VERSION,'smbus-cffi'],
      setup_requires=['cffi >= ' + CFFI_VERSION, 'smbus-cffi'],
      #cffi_modules=["smbus_cffi_build.py:ffi"],
      include_package_data=True,
      zip_safe=False)