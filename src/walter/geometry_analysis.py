"""
Specification
"""

def load_lstring_lscene(output_dir, date):
    """reload lstring and lscene from walter output dir"""

def structured_scene(lstring, lscene):
    """

    Parameters
    ----------
    lstring
    lscene

    Returns
    -------
     mtg or equivalent pandas that tag geometry with label of different elements
    """
    pass

def query(scene, plant=None, genotype=None, organ=None):
    """

    Parameters
    ----------
    scene
    plant
    genotype
    organ

    Returns
    -------
        a scene corresponding to the selection
    """

###############################################################################


def proj_surface(scene, direction=None):
    """

    Parameters
    ----------
    geometry
    direction

    Returns
    -------
        projected surface per structure (int)
    """

def surface(geometry):
    """

    Parameters
    ----------
    geometry

    Returns
    -------
		real surface per structure
    """

def gap_fraction(geometry):
    """
    
    Parameters
    ----------
    geometry

    Returns
    -------
    	gap fraction of per structure
    """

def dominance_propability():
    """ may be mutual_shading
    Parameters
    ----------
    geometry (plant)

    Returns
    -------
    Difference in projected surface for a plant with and without its neighbours
    """

def bounding_cylinder(geometry):
    """

    Parameters
    ----------
    geometry

    Returns
    -------

    """


def equivalent_cylinder(geometry):
    """A cylinder that has equivalent property of geometry, witto interseption

    Parameters
    ----------
    geometry

    Returns
    -------

    """
    
def distribution_LAI(geometry)
    """ Repartition of LAI along z axis at a given time

    Parameters
    ----------
    geometry

    Returns
    -------
	data frame with z coordinates and corresponding LAI (Ea?)
    """

