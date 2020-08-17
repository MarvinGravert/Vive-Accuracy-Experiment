from setuptools import setup, find_packages

setup( 
	name='vive_accuracy_data',#name which will be used to install via pip
	version='1',#version number simple as that
	description='',
	long_description='',
	author='Marvin Gravert',
	author_email='marvin.gravert@gmail.com',

	license='MIT',
	#which directories to search for imports. Importable dirs are marked by 
	packages=find_packages(include=["analysis","analysis.*"]),
	#packages=find_packages()#also possible but may include unwanted dir such as tests
	zip_safe=False,
	
)