# Install

Install Conda
=============

`Conda <https://conda.io/docs/user-guide/install/index.html>`_ is a package manager that can be installed on Linux, Windows, and Mac. If you have not yet installed conda on your computer, follow these instructions:

`Conda <https://conda.io/miniconda.html>`_ Installation. Follow instructions for Miniconda. Use the Python 2.7 based installation.


Install OpenAlea
================

Create an environment named walter:
::
    conda create -n walter -c openalea openalea.lpy boost=1.66

Activate the walter environment (do not type 'source' on windows):
::
    [source] activate walter

Install the different packages:
::
    conda install -c openalea openalea.mtg alinea.caribu notebook matplotlib pandas scipy
    conda install -c openalea -c conda-forge pvlib-python pytables

Download the last version of astk:
::
    git clone https://github.com/openalea-incubator/astk.git

Then, in the newly downloaded astk directory, run:
::
    python setup.py install


Install WALTer
==============

Download WALTer from `this repository <https://forgemia.inra.fr/walter/walter>`_, then, in the walter directory, run:
::
    python setup.py install

or:
::
    python setup.py develop


# Usage

User
====

If the WALTer environment in which you want to perform the simulations is not yet activated, do it, for instance (`source` may be optional, depending on the version of Conda):
::
    conda -env list
    [source] conda activate

Create a project:
::
    walter -p [project_name]

This will create a directory named ``project_name`` and, inside, it will save several files (default meteo data, geometric rules to create organs, output list).

Then you need to create a configuration file.
This file has a header row and as many rows as simulations.
Each genotype has its own set of parameters (one per column).

Run simulations (first, enter the directory created just before, and run the following command):
::
    walter -i [sim_scheme.csv]

Enjoy the outputs!

Once done, desactivate the Condaenvironment:
::
    [source] conda deactivate


Developer
=========

Simple usage:

.. code-block:: python

    from WALTer import *


# Acknowledgments

