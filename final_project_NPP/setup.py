import os
import zipfile
from setuptools import setup, find_packages

def unzip_data():
    """Unzip data.zip to the data directory."""
    zip_path = os.path.join(os.path.dirname(__file__), 'data', 'data.zip')  # Path to the zip file
    extract_path = os.path.join(os.path.dirname(__file__), 'data')  # Folder where it will be extracted

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# Call the unzip logic before installing the package
unzip_data()

setup(
    name='final_project_NPP',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    include_package_data=True,
    author='Krystian Wrotniak',
    description='The final assignment for NPP subject',
    url='https://github.com/wrotniakk/MyProjects/tree/final_project_NPP/final_project_NPP',
)
