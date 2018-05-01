#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from os import walk
from os.path import abspath, normpath
from os.path import join as pj

from setuptools import setup, find_packages


short_descr = "WALTer : a 3D FSPM Wheat model that simulates the tillering plasticity based on light competition"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/walter/version.py
version = {}
with open("src/walter/version.py") as fp:
    exec(fp.read(), version)


data_files = []

nb = len(normpath(abspath("src/walter_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/walter_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


setup_kwds = dict(
    name='walter',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Christophe Lecarpentier, Emmanuelle Blanc, ",
    author_email="christophe.lecarpentier@inra.fr, emmanuelle.blanc@u-psud.fr, ",
    url='https://github.com/openalea-incubator/WALTer',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},

    include_package_data=True,
    package_data={'walter_data': data_files},
    install_requires=[
        ],
    tests_require=[
        "mock",
        "nose",
        ],
    entry_points={},
    keywords='wheat, FSPM, tillering, light competition',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['console_scripts'] = ['walter = walter.walter_command:main', ]
# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
