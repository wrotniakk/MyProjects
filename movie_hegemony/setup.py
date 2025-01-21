import os
from setuptools import setup, find_packages


setup(
    name='final_project_NPP',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    include_package_data=True,
    author='Krystian Wrotniak',
    description='The final assignment for NPP subject',
    url='https://github.com/wrotniakk/MyProjects/tree/final_project_NPP/final_project_NPP',
)
