import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='vanguard',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple API authentication library for Django REST Framework',
    long_description=README,
    url='https://github.com/svalleru/vanguard',
    author='Shan Valleru',
    author_email='shanvalleru@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    keywords='Django REST Framework Authentication, API Authentication',
    install_requires=['djangorestframework', 'cryptography'],
)
