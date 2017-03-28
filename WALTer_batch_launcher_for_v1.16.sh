#!/bin/bash
CARIBU="enabled"
densites=(100 200 400 50 25)
expe_relateds=("Darwinkel_mean")

reps=(0 1)
tillering_prob_Maxwells=(0.88)
LAIc_Maxwells=(0.59)

PARseuils=(280000)
for r in "${reps[@]}"
	do
	for b in "${tillering_prob_Maxwells[@]}"
		do
		for c in "${LAIc_Maxwells[@]}"
			do 
			for d in "${PARseuils[@]}"
				do
				for e in "${expe_relateds[@]}"
					do
					for a in "${densites[@]}"
						do
						date > out.$a.$b.$c.$d.$e.$r.txt
						date
						echo densite=$a tillering_prob_Maxwell=$b LAIc_Maxwell=$c PARseuil=$d expe_related=$e rep=$r CARIBU_state=$CARIBU
						time ./WALTer_launcher-v1-16.py densite=$a tillering_prob_Maxwell=$b LAIc_Maxwell=$c PARseuil=$d expe_related=$e rep=$r CARIBU_state=$CARIBU >>out.$a.$b.$c.$d.$e.$r.txt 2>err.$a.$b.$c.$d.$e.$r.txt
						done
					done
				done
			done
		done
	done
date


#mpg123 /home/christophe/Musique/yoyo_rnb.mp3
#cd /home/christophe/Documents/Programmation/Modeles/Wheat-Mixture-Simulator/batch/sources/1-script_R
#Rscript Evaluation-LWheat_Maxwell_organdim.R

#cd /home/christophe/Documents/Evaluation-du-modele/evaluation-finale
#Rscript Evaluation-du-modele-avec-liste.R

#./L-Wheat_batch_launcher.sh >out.txt 2>err.txt
