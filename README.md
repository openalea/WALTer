# Installation of OpenAlea

## Conda Installation

[Conda](https://conda.io/docs/user-guide/install/index.html) is a package manager that can be installed on Linux, Windows, and Mac. If you have not yet installed conda on your computer, follow these instructions:

[Conda Installation](https://conda.io/miniconda.html). Follow instructions for Miniconda.

[Conda Download](https://conda.io/miniconda.html). Use the Python 2.7 based installation.

### Windows, Linux, Mac

Create an environment named walter:

`conda create -n walter -c openalea openalea.lpy boost=1.66`

Activate the walter environment (do not type 'source' on windows):

`[source] activate walter`

Install the different packages

`conda install -c openalea openalea.mtg alinea.caribu notebook matplotlib pandas scipy`

`conda install -c openalea -c conda-forge pvlib-python pytables`

`conda install rpy2`

`git clone https://github.com/openalea-incubator/astk.git`

Then, in the newly downloaded astk directory, run :
`python setup.py install`

`conda install nose`
