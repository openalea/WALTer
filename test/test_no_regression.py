# coding=utf-8
from walter import project
from walter.light import get_light, scene_pattern
import pandas

def test_same_result_zerolight():
    #assert : verify if the same wheat field have the same results for the same chosen parameters.
    p = project.Project(name='same')
    # reference_file = fichier contenant le tableau de référence.
    # reference = reference_file.read()
    
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    params.update(dict(nbj=165))
    outs = p.which_outputs
    p.which_outputs = outs
    lsys, lstring = p.run(**params)
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']
    dfout = pandas.read_csv(p.dirname / 'output' / id / 'PAR_per_axes.csv', sep='\t')
    assert (dfout == reference), " Not the same results for the same experience. "

    p.deactivate()
    p.remove(force=True)


def test_zero_light():

    #assert : all tillers receive light (value > 0 for Sum_PAR in the PAR_per_axes.csv output file)

    p = project.Project(name='zero_light')
    #Creer un répertoire de sauvegarde qui contient le test.
    params = p.csv_parameters('sim_scheme_test.csv')[0]
    #récupère les parametres dans le fichier en argument.
    params.update(dict(nb_plt_temp=50, nb_rang=10, nbj=156))
    #Initialise le nombre de plantes et les conditions données en leur affectant les parametres à faire varier.
    outs = p.which_outputs
    #Créer le fichier de sortie s'il n'est pas déjà existante.
    p.which_outputs = outs
    #Affecte le fichier de sortie à la sortie du test pour sauvegarder les résultats.
    lsys, lstring = p.run(**params)
    #Lance une simulation en mettant à jour les résultats de parametre pour chaque plantes simulé.
    PAR_per_axes_dico = lsys.context().locals()['PAR_per_axes_dico']#Récupère les variables globales du lsystem.
    df = pandas.DataFrame(PAR_per_axes_dico)
    PAR = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PAR > 0)
    with open(p.dirname/'ID_simul.txt') as f: #Ouvre un document 'ID_simul.txt' dans le répertoire pere (repertoire courant / dans notre cas 'test/zero_light').
        id = f.read()
        #Lis le document est enregistre son écriture dans "id".

    dfout = pandas.read_csv(p.dirname / 'output' / id / 'PAR_per_axes.csv', sep='\t')
    PARout = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PARout > 0)

    p.deactivate()
    p.remove(force=True)


