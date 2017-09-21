#!/bin/bash

# pas d'argument => on ecrit le message d'erreur sur la sortie d'erreur et on renvoie une valeur > 0 
[[ -z $1 ]] && echo >&2 "Error: fucking argument missing !" && exit 1

> combi_param.csv

# chemin vers le script python
script_py="./WALTer_launcher.py"

# Si le 1er argument est total_diallel (A FAIRE)
if [[ $1 == "total_diallel" ]]
then
	# TODO
	exit 0 # on quitte en retournant zero => pas d'erreur
fi

# sinon, les combinaisons sont indiquees dans un fichier tabulé 
filename=$1

# 2eme argument (optionnel): dit comment sonr representees les donnee manquante dans le fichier input
md=$2
# ATTENTION: si pas de 2eme argument, on remplace les champs vides par des "NA" dans le fichier input
[[ -z $md ]] && md=NA && sed -i -e 's/\tNA\t/\tNA\t/g' -e 's/\tNA/\tNA/' -e 's/NA\t/NA\t/' $filename
# => le fichier input est modifié

# noms des parametres (vide)
param_names=

# on itere sur chaque ligne (line est un tableau)
while read -a line
do
	# Si le tableau param_names est vide, on le remplit avec le contenu de la 1ere ligne
	# continue => on passe a l'iteration suivante sans executer le reste du bloc
#	[[ -z $param_names ]] && param_names=(${line[@]}) && identifiant="ID" && OLD_IFS="$IFS" && IFS=$'\t' && echo -e "${line[*]}""\t"$identifiant >> combi_param.csv && IFS="$OLD_IFS" && continue
	[[ -z $param_names ]] && param_names=(${line[@]}) && identifiant="ID" && OLD_IFS="$IFS" && IFS=$'\t' && echo -ne "${line[*]}\t$identifiant\n" >> combi_param.csv && IFS="$OLD_IFS" && continue

	i=0 # indice des tableaux
	
	# tous les parametres pour une simulation (vide) 
	script_params=
	
	# on itere sur chaque valeur
	for value in ${line[@]}
	do
		# si value != NA, on ajoute le couple param=value a script_params
		[[ $value != $md ]] && script_params="$script_params ${param_names[$i]}=$value"
		# incremente l'indice
		((i++))
	done

	echo -e "\033[31m$script_params\033[0m"
		
	# suffixe pour des noms de fichiers de sortie standard et d'erreur
	#suffixe="`echo ${line[@]} | tr ' ' '_'`.txt"

	identifiant=`cat ID_simul.txt`
	suffixe=$identifiant

	# lancement d'une simulation (script python avec tous ses parametres)
	#echo "$script_py $script_params >>Outs/out.$suffixe 2>Errors/err.$suffixe"
	date | tee Times/time.$suffixe
	{ time $script_py $script_params >>Outs/out.$suffixe 2>Errors/err.$suffixe ; } 2>&1 | tee -a Times/time.$suffixe

	OLD_IFS="$IFS"
	IFS=$'\t'
	#echo -e "${line[*]}""\t"$identifiant >> combi_param.csv
	echo -ne "${line[*]}\t$identifiant\n" >> combi_param.csv
	IFS="$OLD_IFS"
	
	#./WALTer_launcher-v1-17_dev.py densite=$a tillering_prob_Maxwell=$b LAIc_Maxwell=$c PARseuil=$d expe_related=$e rep=$r CARIBU_state=$CARIBU >>out.$a.$b.$c.$d.$e.$r.txt 2>err.$a.$b.$c.$d.$e.$r.txt

done < $filename

