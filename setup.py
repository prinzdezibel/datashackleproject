from setuptools import setup, find_packages

_description = (
    "Script that creates a Grok project directory, installs Grok, the Grok "
    "Toolkit and the Zope Toolkit and sets up a complete skeleton for "
    "a new Grok web application."
    )

long_description = (
    "===========\n"
    "Grokproject\n"
    "===========\n"
    "\n"
    "%s\n"
    "\n"
    ".. contents::\n"
    "\n"
    "Description\n"
    "===========\n"
    "\n" +
    open('README.txt').read() +
    '\n' +
    open('CHANGES.txt').read()
    ) % _description

setup(
    name='datashackleproject',
    version='0.1',
    author='Michael Jenny',
    author_email='michael.jenny@projekt-und-partner.de',
    url='',
    #download_url='http://pypi.python.org/pypi/grokproject',
    description=_description,
    long_description=long_description,
    license='ZPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['PasteScript>=1.6'],
    test_suite='tests.test_suite',
    entry_points={
        'console_scripts': ['datashackleproject = datashackleproject:main'],
        'paste.paster_create_template': ['datashackle = datashackleproject:DatashackleProject']},
    )
