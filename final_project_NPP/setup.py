# setup.py

from setuptools import setup, find_packages

setup(
    name='final_project_NPP',              # Name of the package
    version='1.0.0',                       # Version of the package
    packages=find_packages('src'),         # Automatically discover packages in the 'src' directory
    package_dir={'': 'src'},               # Tell distutils packages are in the 'src' directory
    entry_points={                         
        'console_scripts': [
            'analysis=analysis:main',      
        ],
    },
    include_package_data=True,              
    author='Krystian Wrotniak',             
    description='Final project assignment for NPP subject',
    url='https://github.com/wrotniakk/MyProjects/tree/final_project_NPP/final_project_NPP',  # GitHub URL
)