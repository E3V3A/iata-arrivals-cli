from setuptools import setup, find_packages
from os import path

#------------------------------------------------------------------------------
# The current standard for setup info.
# For details, see:
#  https://packaging.python.org/guides/distributing-packages-using-setuptools/
#  https://github.com/pypa/sampleproject/blob/master/setup.py
#  https://pypi.org/classifiers/
#  https://choosealicense.com/
#------------------------------------------------------------------------------

def readme():
    # Get the long description from the README file
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name             = 'iata-arrivals-cli',
    version          = '1.0.2',
    author           = 'E:V:A',
    author_email     = 'xdae3v3a@gmail.com',
    description      = 'Get airport arrivals, departures, details and METAR weather info from CLI.',
    long_description = 'Get various airport information by providing an airport IATA code or country name.',
    long_description_content_type='text/plain',
    #long_description = readme(),
    #long_description_content_type = 'text/markdown',
    license='LICENSE.txt',
    url = 'https://github.com/e3v3a/iata-arrivals-cli/',
    packages = find_packages(),
    scripts=['arrivals.py'],
    keywords = 'airport flights arrivals departures iata icao metar pip package cli',
    install_requires=[
        'lxml',
        'requests',
        'beautifulsoup4',
        'jsonpath-rw',
        'metar',
        'pyflightdata'
    ],
    python_requires = '>=3',
    classifiers=[
        #'Private :: Do Not Upload',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/e3v3a/iata-arrivals-cli/issues',
        #'Funding' : 'https://donate.pypi.org',
        #'Credits' : 'http://saythanks.io/to/example',
        #'Source'  : 'https://github.com/pypa/sampleproject/',
    },
    #zip_safe = False,
)
