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


def total_proj_surface(scene, direction=None):
    """

    Parameters
    ----------
    plant geometry
    radiation direction (vertical by default)

    Returns
    -------
        plant projected surface on the ground with occlusions (holes are filled), i.e when plant triangles are projected on xy plan it is the surface within edges
    """

def real_proj_surface(scene, direction=None):
    """

    Parameters
    ----------
    plant geometry
    radiation direction (vertical by default)

    Returns
    -------
        plant projected surface on the ground without occlusions (holes are not filled), i.e surface projection of all triangles (maybe juste leaf triangles?) for a given plant
    """

def surface(geometry):
    """

    Parameters
    ----------
    geometry

    Returns
    -------
		real surface per structure, maybe specify scale of the surface (organ or plant), get total leaf surface of one plant for example
    """


def foliage_exposed_surface(geometry):
    """

    Parameters
    ----------
    geometry

    Returns
    -------
		leaf exposed surface (that will intercept light and do photosynthesis) for a given plant
    """


def gap_fraction(geometry):
    """
    
    Parameters
    ----------
    geometry

    Returns
    -------
    	gap fraction per structure
    """

def dominance_propability(geometry):
    """ may be mutual shading
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
    """A cylinder that has equivalent property of geometry, witto interception

    Parameters
    ----------
    geometry

    Returns
    -------

    """
    
def distribution_LAI(geometry):
    """ Repartition of LAI along z axis at a given time

    Parameters
    ----------
    geometry

    Returns
    -------
	data frame with z coordinates and corresponding LAI (Ea?) for a given plant
    """

