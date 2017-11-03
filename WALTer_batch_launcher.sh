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
#	[[ -z $param_names ]] && param_names=(${line[@]}) && identifiant="ID" && OLD_IFS="$IFS" && IFS="   " && echo -e "${line[*]}""\t"$identifiant >> combi_param.csv && IFS="$OLD_IFS" && continue
	if [[ -z $param_names ]]; then
		param_names=(${line[@]}) && identifiant="ID" && OLD_IFS="$IFS" && IFS=$'\t' && echo -ne "${line[*]}\t$identifiant\n" >> combi_param.csv && IFS="$OLD_IFS"
		# numero de colonne de la variable rep		
		col_rep=`tr '\t' '\n' < combi_param.csv | grep -n "^rep$" | cut -d":" -f1`
		# 1er indice du tableau line = zero
		((col_rep--))
		continue
	fi
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
	suffixe="`echo ${line[@]} | tr ' ' '_'`.txt"
	
	# lancement d'une simulation (script python avec tous ses parametres)
	#echo "$script_py $script_params >>Outs/out.$suffixe 2>Errors/err.$suffixe"
	date | tee Times/time.$suffixe
	{ time $script_py $script_params >>Outs/out.$suffixe 2>Errors/err.$suffixe ; } 2>&1 | tee -a Times/time.$suffixe
		
	identifiant=`cat ID_simul.txt`
	
	# numero de la rep concernee
	rep=${line[$col_rep]}	
	
	try_nb=0; th=15
	# tester la presence du fichier error_caribu.txt
	while [[ -f output/$identifiant/error_caribu.txt && $try_nb -le $th ]]
	do
		
		# on redefinit la chaine de parametres avec la nouvelle valeur de rep (graine)
		#echo "script_params avant: $script_params"
		script_params=${script_params/rep=$rep/rep=$((++rep))}
		#echo "script_params apres: $script_params"
		
		# nettoyage des fichiers dans Times, Outs et Errors et du dossier identifiant
		rm -r output/$identifiant Outs/out.$suffixe Errors/err.$suffixe Times/time.$suffixe
				
		# relance du bousin avec la nouvelle graine
		{ time $script_py $script_params >>Outs/out.$suffixe 2>Errors/err.$suffixe ; } 2>&1 | tee -a Times/time.$suffixe
		identifiant=`cat ID_simul.txt`
		((try_nb++))
	done
	
	echo "Victoire, j'ai trouvé une graine suffisamment satisfaisante: $rep, car l'autre d'avant puait du fion => ${line[$col_rep]}"
	OLD_IFS="$IFS"
	IFS=$'\t'	
	#echo -e "${line[*]}""\t"$identifiant >> combi_param.csv
	echo -ne "${line[*]}\t$identifiant\n" >> combi_param.csv	
	IFS="$OLD_IFS"
	
	#./WALTer_launcher-v1-17_dev.py densite=$a tillering_prob_Maxwell=$b LAIc_Maxwell=$c PARseuil=$d expe_related=$e rep=$r CARIBU_state=$CARIBU >>out.$a.$b.$c.$d.$e.$r.txt 2>err.$a.$b.$c.$d.$e.$r.txt

done < $filename

