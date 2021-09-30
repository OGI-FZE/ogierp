from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in oil_and_gas_international/__init__.py
from oil_and_gas_international import __version__ as version

setup(
	name='oil_and_gas_international',
	version=version,
	description='Oil and Gas International',
	author='Havenir Solutions',
	author_email='support@havenir.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
