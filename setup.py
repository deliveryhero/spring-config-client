from distutils.core import setup

from setuptools import find_packages

__version__ = '1.5.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='spring-config-client',
    version=__version__,
    author='',
    author_email='',
    description='Sprint Config Server Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/deliveryhero/spring-config-client',
    project_urls={
        "Bug Tracker": "https://github.com/deliveryhero/spring-config-client"
    },
    license='MIT',
    packages=find_packages(include=['spring_config_client', 'spring_config_client.*']),
    install_requires=['requests==2.28.1', 'config-client==1.3.0'],
)
