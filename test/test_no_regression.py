# coding=utf-8
from walter import project
import pandas,os
from walter.data_access import get_data_dir
from pathlib2 import Path
import numpy.testing as np

def test_same_result_zerolight():
    #assert : verify if the same wheat field have the same results for the same chosen parameters.

    p = project.Project(name='same')  # Création du répertoire de simulation
    params = p.csv_parameters('sim_scheme_test.csv')[0] #Récupération des parametres
    params.update(dict(nbj=165)) #Ajout du parametre a faire varier
    outs = p.which_outputs #Créer le fichier de sortie s'il n'est pas déjà existante.
    p.which_outputs = outs #Affecte le fichier de sortie à la sortie du test pour sauvegarder les résultats.
    lsys, lstring = p.run(**params)
    with open(p.dirname/'ID_simul.txt') as f:
        id = f.read() #Récupération de l'id
    reference_directory = get_data_dir() + "/ref_output/" #Dossier de référence.
    list_of_file_ref = os.listdir(reference_directory) #Listage des différents fichiers de référence.
    reference = {} #Dictionnaire Vide
    for i in list_of_file_ref: #Mise en place des différents résultats dans un tableau.
        element = reference_directory + i #Récupère le chemin absolu
        up_date = { i : pandas.read_csv(element, sep='\t')} #Récupère fichier et contenu
        reference.update(up_date) # Dictionnaire de référence.
        result_directory = p.dirname + '/' + 'output' + '/' + id +'/'
        list_of_result = os.listdir(result_directory)
        np.assert_array_equal(list_of_file_ref,list_of_result) #Vérification que les 2 listes sont égaux.
        my_file = Path(result_directory + i)
        if my_file.is_file() :
            dfout = pandas.read_csv(my_file, sep='\t')
            print(' \n Le fichier testé est : '+ i + '\n')
            np.assert_array_equal(dfout, reference[i]) #Comparaison Référence et Simulation.
        else :
            print(' \n Le fichier ' + my_file + ' est inexistant ')


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
    with open(p.dirname/'ID_simul.txt') as f: #Ouvre un document 'ID_simul.txt' dans le répertoire pere (repertoire courant / dans notre cas 'test/zero_light').
        id = f.read()
        #Lis le document est enregistre son écriture dans "id".

    dfout= pandas.read_csv(p.dirname / 'output' / id / 'PAR_per_axes.csv', sep='\t')
    PARout = df.groupby('Num_plante').agg('sum')['Sum_PAR'].values
    assert all(PARout > 0)

    p.deactivate()
    p.remove(force=True)


