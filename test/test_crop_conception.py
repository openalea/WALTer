import walter.crop_conception as ccptn


def test_crop_mesh_for_nplants():
    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0, dist_border_y=0)
    assert cs['nb_rang'] == 2
    assert cs['nb_plante_par_rang'] == 2
    assert cs['nplant_peupl'] == 4
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5

    cs = ccptn.design_crop_mesh_for_nplants(densite=4, nb_plt_utiles=4, dist_border_x=0.5, dist_border_y=0.5)
    assert cs['nb_rang'] == 4
    assert cs['nb_plante_par_rang'] == 4
    assert cs['nplant_peupl'] == 16
    assert cs['dist_inter_rang'] == cs['dist_intra_rang'] == 0.5


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