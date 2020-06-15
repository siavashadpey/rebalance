from os.path import realpath, dirname, join
from setuptools import setup, find_packages
import re

DISTNAME = 'rebalance'
DESCRIPTION = "A calculator which tells you how to split your investment amongst your portfolio's assets based on your target asset allocation."
AUTHOR = 'Siavosh Shadpey'
AUTHOR_EMAIL = 'siavosh@ualberta.ca'


PROJECT_ROOT = dirname(realpath(__file__))

# Get the long description from the README file
with open(join(PROJECT_ROOT, 'README.md'), encoding='utf-8') as buff:
    LONG_DESCRIPTION = buff.read()

REQUIREMENTS_FILE = join(PROJECT_ROOT, 'requirements.txt')

with open(REQUIREMENTS_FILE) as f:
    install_reqs = f.read().splitlines()

test_reqs = ['unittest']

def get_version():
    VERSIONFILE = join('rebalance','__init__.py')
    lines = open(VERSIONFILE, 'rt').readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in lines:
        mo = re.search(version_regex, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version in %s.' % (VERSIONFILE,))

if __name__ == "__main__":
    setup(name=DISTNAME,
          version=get_version(),
          maintainer=AUTHOR,
          maintainer_email=AUTHOR_EMAIL,
          description=DESCRIPTION,
          packages=find_packages(),
          python_requires=">=3.6",
          tests_require=test_reqs,
          url="https://rebalance.readthedocs.io/",
          install_requires=install_reqs)