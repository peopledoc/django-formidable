import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
        README = readme.read()

setup(
    name='django-formidable',
    version='0.1.0dev0',
    packages=['formidable'],
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='https://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    install_requires=[
        'django<1.9',
        'djangorestframework',
        'dateutils',
        'markdown',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
