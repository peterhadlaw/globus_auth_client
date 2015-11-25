import os
from setuptools import setup, find_packages


pkg_dir = os.path.join(os.path.dirname(__file__), 'globusauth_client')
static_dir = os.path.join(pkg_dir, 'static')


def all_static_files():
    return reduce(lambda x, y: x+y,
                  [[os.path.join(d, f)[len(pkg_dir)+1:] for f in fs]
                   for (d, sds, fs) in os.walk(static_dir)])

setup(
    name='globusauth_client',
    include_package_data=True,
    package_data={'': ['templates/*.html'] + all_static_files()},
    packages=find_packages(),
    package_dir={'': '.'},
    zip_safe=False
)
