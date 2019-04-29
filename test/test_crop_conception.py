import walter.crop_conception as ccptn


def test_crop_mesh_for_nplants():
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0, dist_border_y=0)
    assert cs['nb_rang'] == 2
    assert cs['nb_plante_par_rang'] == 2
    assert cs['nplant_peupl'] == 4
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5
    assert cs['nplant_peupl'] / cs['surface_sol'] == 4

    # choosing border > 0 triggers creation of a border
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0.1, dist_border_y=0.1)
    assert cs['nb_rang'] == 4
    assert cs['nb_plante_par_rang'] == 4
    assert cs['nplant_peupl'] == 16
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5
    assert cs['nplant_peupl'] / cs['surface_sol'] == 4

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0.5, dist_border_y=0.5)
    assert cs['nb_rang'] == 4
    assert cs['nb_plante_par_rang'] == 4
    assert cs['nplant_peupl'] == 16
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5
    assert cs['nplant_peupl'] / cs['surface_sol'] == 4

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=1, dist_border_y=1)
    assert cs['nb_rang'] == 6
    assert cs['nb_plante_par_rang'] == 6
    assert cs['nplant_peupl'] == 36
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5
    assert cs['nplant_peupl'] / cs['surface_sol'] == 4


def test_plant_disposition():
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0, dist_border_y=0)
    maillage, plant_map = ccptn.plant_disposition(cs)
    nbrg = len(maillage)
    nbprg = len(maillage[0])
    assert nbrg == nbprg == 2
    # check centering on (0,0,0)
    x = [pos['x'] for pos in plant_map.values()]
    y = [pos['y'] for pos in plant_map.values()]
    assert len([p for p in x if p >= 0]) == 2
    assert sum(x) == 0
    assert len([p for p in y if p >= 0]) == 2
    assert sum(y) == 0

    # single plant case
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=1, dist_border_x=0, dist_border_y=0)
    assert cs['nplant_peupl'] == 1
    maillage, plant_map = ccptn.plant_disposition(cs)
    x = [pos['x'] for pos in plant_map.values()]
    y = [pos['y'] for pos in plant_map.values()]
    assert sum(x) == 0
    assert sum(y) == 0


def test_domain():
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=1, dist_border_x=0, dist_border_y=0)
    xmin, ymin, xmax, ymax = ccptn.domain(cs)
    assert xmin == ymin == -25
    assert xmax == ymax == 25

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0, dist_border_y=0)
    xmin, ymin, xmax, ymax = ccptn.domain(cs)
    assert xmin == ymin == -50
    assert xmax == ymax == 50

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0.01, dist_border_y=0.01)
    xmin, ymin, xmax, ymax = ccptn.domain(cs)
    assert xmin == ymin == -100
    assert xmax == ymax == 100

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0.5, dist_border_y=0.5)
    xmin, ymin, xmax, ymax = ccptn.domain(cs)
    assert xmin == ymin == -100
    assert xmax == ymax == 100


def test_central_domain():
    # no_border, central_domain = domain
    dist_border_x = 0
    dist_border_y = 0
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    xmin, ymin, xmax, ymax = ccptn.central_domain(cs, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    assert xmin == ymin == -50
    assert xmax == ymax == 50

    # dist_border > 0 : triggers creation of a border
    dist_border_x = 1e-6
    dist_border_y = 1e-6
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    xmin, ymin, xmax, ymax = ccptn.central_domain(cs, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    assert xmin == ymin == -50
    assert xmax == ymax == 50

    # central zone still around the four central plants if border increases
    dist_border_x = 1
    dist_border_y = 1
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    xmin, ymin, xmax, ymax = ccptn.central_domain(cs, dist_border_x=dist_border_x, dist_border_y=dist_border_y)
    assert xmin == ymin == -50
    assert xmax == ymax == 50