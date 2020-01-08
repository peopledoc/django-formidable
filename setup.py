import os
from setuptools import setup, find_packages

import formidable


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django-formidable',
    version=formidable.version,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='django-formidable is a full django application which '
                'allows you to create, edit, delete and use forms.',
    long_description=README,
    url='https://github.com/peopledoc/django-formidable',
    author='Guillaume Camera, Guillaume Gérard',
    author_email='guillaume.camera@people-doc.com, '
                 'guillaume.gerard@people-doc.com',
    install_requires=[
        'Django',
        'djangorestframework<4.0.0',
        'markdown',
        'python-dateutil',
        'jsonfield',
        'pytz',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
