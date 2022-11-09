from setuptools import setup, find_packages
from os import path


__version__ = '0.0.1'
URL = ''

HERE = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requirements = [
    'pandas',
    'requests',
    'numpy',
    'matplotlib',
    'PyYAML'
]

setup(
    name="Rapid Finance",
    version=__version__,
    description="Finance library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author="Marco Latella",
    author_email="mrclatella@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=install_requirements,
)