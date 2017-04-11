#Ce script permet d'extraire dans R les sorties issues des simulations de WALTer V1.17.
#
#Le script prend en entree :
#   path : le chemin absolu vers les fichiers "combi_param.txt" et "which_output_files.csv"
#   set : le nom du dossier dans lequel se trouvent les dossiers de sortie de WALter
#
#En remplissant le tableau "which_output_files.csv" on peut decider quels fichiers seront
#extraits apres les simulations (0 : le fichier n'est pas extrait (et pas genere par le modele
#non plus d'ailleurs)) ; 1 : le fichier est extrait
#
#Le script retourne :
#   combi_param : un data.frame donnant l'identifiant des differentes simulations et les valeurs
#de parametres associes
#   output_scheme : un data.frame rappelant quels fichiers sont extraits et lesquels ne le sont pas
#   nb_simul : le nb de simulation etudiees
#   Pour les fichier a extraire : une liste par type de fichier.Chaque liste comprend un data.frame
#par simulation

set = "output/"

path = "/home/emmanuelle/Documents/WALTer1.17/"

root = paste(path, set, sep = "")

combi_param = read.table(paste(path,"combi_param.txt",sep = ""), header = T, sep = "\t")
output_scheme = read.csv(paste(path,"which_output_files.csv",sep = ""),sep = "\t" ,header = T)

nb_simul = dim(combi_param)[1]


##################################################################################################################################################
############################## CREATION DE FONCTIONS POUR LECTURE DES FICHIERS #################################################
#############################################################################################################################################


#Fonction pour lire le fichier Apex_Sirius_prop
Lecture_Apex_Sirius <- function(id)
{
  print("Lecture Apex_sirius...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Apex_Sirius_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Apex_Sirius_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
}



#Fonction pour lire le fichier Apex_prop
Lecture_Apex <- function(id)
{
  print("Lecture Apex...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Apex_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Apex_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
}



#Fonction pour lire le fichier Apex_R_prop
Lecture_Apex_R <- function(id)
{
  print("Lecture Apex_R...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Apex_R_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Apex_R_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Bud_prop
Lecture_Bud <- function(id)
{
  print("Lecture Bud...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Bud_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Bud_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Blade_prop
Lecture_Blade <- function(id)
{
  print("Lecture Blade...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Blade_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Blade_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Internode_prop
Lecture_Internode <- function(id)
{
  print("Lecture Internode...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Internode_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Internode_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Sheat_prop
Lecture_Sheath <- function(id)
{
  print("Lecture Sheat...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Sheath_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Sheath_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Ear_prop
Lecture_Ear <- function(id)
{
  print("Lecture Ear...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Ear_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Ear_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Peduncle_prop
Lecture_Peduncle <- function(id)
{
  print("Lecture Peduncle...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Peduncle_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Peduncle_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier GAI_prox
Lecture_GAIp <- function(id)
{
  print("Lecture GAIp...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' *GAI_prox.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("GAI_prox.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Peraxes_prop
Lecture_Peraxes <- function(id)
{
  print("Lecture Peraxes...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Peraxes_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Peraxes_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier Proba_prop
Lecture_Proba <- function(id)
{
  print("Lecture Proba...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' Proba_prop.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("Proba_prop.txt", header=TRUE, na.strings = "NA", sep="\t")
  
}



#Fonction pour lire le fichier parcelle
LectureParcelle <-  function(id)
{
  print("Lecture Parcelle...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  
  read.table("parcelle.txt", header=TRUE, na.strings = "NA", sep="\t")
}



#Fonction pour lire le fichier parameters
LectureParam <-  function(id)
{
  print("Lecture Parameters...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  
  read.table("parameters.txt", header=TRUE, na.strings = "NA", sep="\t")
}



#Fonction pour lire le fichier individual_heterogeneity
LectureIndHet <- function(id)
{
  print("Lecture Individual_heterogeneity...")
  folder_name = paste(id)
  setwd(paste(root,folder_name, sep=""))
  system("sed -i 's/ //g' individual_heterogeneity.txt") #Modification du fichier en #bash pour enlever tout espace
  
  read.table("individual_heterogeneity.txt", na.strings = "NA", sep="\t")
}


##################################################################################################################################################
########################################## LECTURE DES FICHIERS #################################################
#############################################################################################################################################

#On note le temps pour savoir a la fin combien de temps ca a pris
registered_time = proc.time()


#Pour chaque type de fichier, on range dans une liste les data.frame de toutes les simulations

print("WAIT FILES ARE LOADING ...")

if (output_scheme$Apex_sirius == 1){
ListApex_Sirius <- lapply(1:nb_simul,function(x) Lecture_Apex_Sirius(combi_param$ID[x]))
print("List_Apex_Sirius : OK")
}

if (output_scheme$Apex == 1){
ListApex <- lapply(1:nb_simul,function(x) Lecture_Apex(combi_param$ID[x]))
print("ListApex : OK")
}

if (output_scheme$Apex_R == 1){
ListApexR <- lapply(1:nb_simul,function(x) Lecture_Apex_R(combi_param$ID[x]))
print("ListApexR : OK")
}

if (output_scheme$Bud == 1){
ListBud <- lapply(1:nb_simul,function(x) Lecture_Bud(combi_param$ID[x]))
print("ListBud : OK")
}

if (output_scheme$Blade == 1){
ListBlade <- lapply(1:nb_simul,function(x) Lecture_Blade(combi_param$ID[x]))
print("ListBlade : OK")
}

if (output_scheme$Sheat == 1){
ListSheath <- lapply(1:nb_simul,function(x) Lecture_Sheath(combi_param$ID[x]))
print("ListSheat : OK")
}

if (output_scheme$Internode == 1){
ListInternode <- lapply(1:nb_simul,function(x) Lecture_Internode(combi_param$ID[x]))
print("ListInternode : OK")
}

if (output_scheme$Ear== 1){
ListEar <- lapply(1:nb_simul,function(x) Lecture_Ear(combi_param$ID[x]))
print("ListEar : OK")
}

if (output_scheme$Peduncle == 1){
ListPeduncle <- lapply(1:nb_simul,function(x) Lecture_Peduncle(combi_param$ID[x]))
print("ListPeduncule : OK")
}

if (output_scheme$Peraxes == 1){
ListPeraxes <- lapply(1:nb_simul,function(x) Lecture_Peraxes(combi_param$ID[x]))
print("ListPeraxes : OK")
}

if (output_scheme$GAIp == 1){
ListGAIp <- lapply(1:nb_simul,function(x) Lecture_GAIp(combi_param$ID[x]))
print("ListGAIp : OK")
}

if (output_scheme$Proba == 1){
List_Proba <- lapply(1:nb_simul,function(x) Lecture_Proba(combi_param$ID[x]))
print("ListProba : OK")
}

if (output_scheme$Parcelle == 1){
List_Parcelle <- lapply(1:nb_simul,function(x) LectureParcelle(combi_param$ID[x]))
print("List_Parcelle : OK")
}

if (output_scheme$Parameters == 1){
List_Param <- lapply(1:nb_simul,function(x) LectureParam(combi_param$ID[x]))
print("List_Param : OK")
}

if (output_scheme$Indiv_hete == 1){
List_Ind <- lapply(1:nb_simul,function(x) LectureIndHet(combi_param$ID[x]))
print("List_Ind : OK")
}

print("100% COMPLETED")

#On affiche le temps que ca a pris de charger les fichiers dans R
print(proc.time()-registered_time)



