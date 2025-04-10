from setuptools import setup, find_packages

setup(
	name='ChainBodySim',
	version='0.1',
	packages=find_packages(where='scr'),
	package_dir={'': 'scr'},
	install_requires=[
		'numpy',
		'pygame'
	],
	entry_points={
		'console_scripts': [
			'chainbodysim=main:main'
		]
	},
)
