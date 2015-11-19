import os
from setuptools import setup, find_packages

setup(
    name='globusauth_client',
    include_package_data=True,
    package_data={'': ['*']},
    packages=find_packages(),
    package_dir={'': '.'}
)
