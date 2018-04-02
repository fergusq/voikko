from setuptools import setup

with open("README.md") as f:
	long_description = f.read()

setup(
	name='voikko',
	version='0.2',
	description='Python 3 version of libvoikko and the word inflecting library',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='http://github.com/fergusq/voikko',
	author='Harri Pitkänen and Iikka Hauhio',
	author_email='iikka.hauhio@gmail.com',
	license='GPL',
	classifiers=[
		'Programming Language :: Python :: 3'
	],
	packages=['voikko'],
	package_data={
		'voikko': ['sanat.txt', 'subst.aff', 'verb.aff'],
	},
	python_requires='>=3',
	install_requires=[],
)
