import math
import os
import pandas as pd
import csv
import numpy as np
from scipy.spatial.distance import pdist


def condensed_index(i, j, n):
    assert i != j, "no diagonal elements in condensed matrix"
    if i < j:
        i, j = j, i
    return n*j - j*(j+1)//2 + i - 1 - j


def neighbours(surfaces, plant_map, option_radius):
    if option_radius == "density":
        radius = pd.DataFrame(surfaces[:,7], index = surfaces[:,0], columns=["radius"])
    elif option_radius == "equivalent_cylinder_projection":
        radius = pd.DataFrame(math.sqrt(surfaces[:,3]/matyh.pi), index = surfaces[:,0], columns=["radius"])
    elif option_radius == "bounding_cylinder_projection":
        radius = pd.DataFrame(surfaces[:,5], index = surfaces[:,0], columns=["radius"])
    else:
        print("Unknown radius option, Rd by default")
        radius = pd.DataFrame(surfaces[:,7], index = surfaces[:,0], columns=["radius"])
    df = pd.DataFrame(plant_map.values(), index = plant_map.keys())
    df = pd.concat([df, radius], axis=1)
    dm = pdist(df)
    n = len(df)
    nbrs = {}
    for i, pid in enumerate(df.index):
        drad = [(j, dm[condensed_index(i, j, n)], radius["radius"].iloc[j]) for j in range(n) if j != i]
        nbrs[int(pid)] = [df.index[j] for j, d, r in drad if radius["radius"][pid] + r > d]
    return(nbrs)


def make_dico(dirname, option_radius="density"):
    os.chdir(dirname)
    with open('plant_map.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        plant_map = dict((eval(rows[0]),eval(rows[1])) for rows in reader)

    for elt in plant_map:
        plant_map[elt]["x"] *= 1e-02
        plant_map[elt]["y"] *= 1e-02

    with open('crop_scheme.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        crop_scheme = dict((rows[0],eval(rows[1])) for rows in reader)


    file = open("test_caribu_surfaces.csv","rb")
    df=pd.read_csv(file,delimiter=',',index_col=False)
    file.close()
    surfaces = np.array(df)
    dict_info = {}
    for i in range(0,np.shape(surfaces)[0]):
        idx = surfaces[i,0]
        dict_info[idx]={}
        dict_info[idx]["S"] = surfaces[i,1]
        dict_info[idx]["Sp_within"] = surfaces[i,2]
        dict_info[idx]["Sp_isolated"] = surfaces[i,3]
        dict_info[idx]["Sp_selfsim"] = surfaces[i,4]
        dict_info[idx]["Ri"] = surfaces[i,5]
        dict_info[idx]["Hi"] = surfaces[i,6]
        dict_info[idx]["Rd"] = surfaces[i,7]
    nbrs = neighbours(surfaces,plant_map,option_radius)
    return(plant_map, crop_scheme, dict_info, nbrs)


def compute_Sp(i,dict_info,option_radius="density"):
    """ Test for i = 1 and i = 2 with 4 different options """
    if option_radius == "density":
        dict_info[i]["Rp"] = dict_info[i]["Rd"]
        dict_info[i]["Sp"] = math.pi * pow(dict_info[i]["Rd"],2)
    elif option_radius == "equivalent_cylinder_projection":
        dict_info[i]["Sp"] = dict_info[i]["Sp_isolated"]
        dict_info[i]["Rp"] = math.sqrt(dict_info[i]["Sp_isolated"]/math.pi)
    elif option_radius == "bounding_cylinder_projection":
        dict_info[i]["Rp"] = dict_info[i]["Ri"]
        dict_info[i]["Sp"] = math.pi * pow(dict_info[i]["Ri"],2)
    else:
        print("Warning, wrong surface option, computation of Sp with Rd radius")
        dict_info[i]["Rp"] = dict_info[i]["Rd"]
        dict_info[i]["Sp"] = math.pi * pow(dict_info[i]["Rd"],2)

def compute_Pc(kb,i,dict_info):
    dict_info[i]["Pc"] = 1 - math.exp(-kb * dict_info[i]["S"] / dict_info[i]["Sp"])

def compute_Pioverj(i, j, dict_info):
    hi = dict_info[i]["Hi"]
    hj = dict_info[j]["Hi"]
    beta = min(hi, hj)
    Pioverj = pow(beta,2)/(2*hi*hj) + (hi-beta) / hi
    return(Pioverj)

def triple_intersection(nbrs, plant_map, dict_info, i):
    if len(nbrs[i]) < 2:
        return(0)
    else:
        for j in nbrs[i]:
            for k in nbrs[i]:
                if k > j:

                    rspi = dict_info[i]["Rp"]
                    rspj = dict_info[j]["Rp"]
                    rspk = dict_info[k]["Rp"]


                    dij = math.sqrt(pow((plant_map[i]["x"] - plant_map[j]["x"]),2) + pow((plant_map[i]["y"] - plant_map[j]["y"]),2))
                    dik = math.sqrt(pow((plant_map[i]["x"] - plant_map[k]["x"]),2) + pow((plant_map[i]["y"] - plant_map[k]["y"]),2))
                    djk = math.sqrt(pow((plant_map[j]["x"] - plant_map[k]["x"]),2) + pow((plant_map[j]["y"] - plant_map[k]["y"]),2))
                    if rspi+rspj > dij and rspi+rspk > dik and rspj+rspk > djk:
                        return(1)
        return(0)

def double_partitioning_trigo(i, nbrs, dict_info,plant_map):
    Sfu = 0.0
    Sponlyi = dict_info[i]["Sp"]
    rspi = dict_info[i]["Rp"]
    for j in nbrs[i]:
        d = math.sqrt(pow((plant_map[i]["x"] - plant_map[j]["x"]),2) + pow((plant_map[i]["y"] - plant_map[j]["y"]),2))
        rspj = dict_info[j]["Rp"]
        test = rspi + rspj - d
        if test <= 0:
            Spij = 0
        else:
            # Spij = 2 * rspi * (acos(1-test/(2*rspi)) * sqrt(test/rspi - (test/rspi)^2)*(1-test/(2*rspi)) )
            di = (pow(rspi,2) + pow(d,2) -pow(rspj,2)) / (2*d)
            dj = d - di

            Spij = math.acos(di/rspi) * pow(rspi,2) - di*math.sqrt(pow(rspi,2)-pow(di,2)) + math.acos(dj/rspj) * pow(rspj,2) - dj*math.sqrt(pow(rspj,2)-pow(dj,2))

        Pioverj = compute_Pioverj(i, j, dict_info)
        Sfu += Spij * dict_info[i]["Pc"] *((1-dict_info[j]["Pc"]) + dict_info[j]["Pc"] * Pioverj)
        Sponlyi -= Spij

    Sfu += Sponlyi * dict_info[i]["Pc"]
    return(Sfu)

def computeSfu(i,nbrs,dict_info,plant_map, timestep):
    if len(nbrs[i]) == 0:
        Sfu = dict_info[i]["Sp"] * dict_info[i]["Pc"]
        print("No intersection")
    else:
        triple_check = triple_intersection(nbrs, plant_map, dict_info, i)
        if triple_check == 0:
            print("1 intersection")
            Sfu = double_partitioning_trigo(i, nbrs, dict_info,plant_map)
        else:
            print("> 1 intersection")
            Sfu = partitioning(i,nbrs, dict_info,timestep,type)
    return(Sfu)


def Get_Rho_List(t,i,nbrs, plant_map,dict_info):
    # rho1 and rho 2 for plant i
    Rp = dict_info[i]["Rp"]
    Sp = dict_info[i]["Sp"]

    dsqri = math.sqrt(pow(Rp,2) - pow(t,2))
    rho1 = plant_map[i]["y"] - dsqri
    rho2 = plant_map[i]["y"] + dsqri
    Rho_List = [(i,rho1),(i,rho2)]

    for j in nbrs[i]:
        dsqrj2 = Rp - pow((t + plant_map[i]["x"] - plant_map[j]["x"]),2)
        if dsqrj2 > 0:
            dsqrj = math.sqrt(dsqrj2)
            rho1_temp = plant_map[j]["y"] - dsqrj
            rho2_temp = plant_map[j]["y"] + dsqrj

            if rho1_temp < rho2 and rho1_temp > rho1:
                Rho_List.append((j,rho1_temp))
            if rho2_temp < rho2 and rho2_temp > rho1:
                Rho_List.append((j,rho2_temp))
    return(rho1, rho2, Rho_List)


def Get_Prob(i, dict_info, li, lo):
    prob = 1.0
    prob_temp = 1.0
    norm = 0.0
    for it1 in li:
        if it1 == i:
            prob *= dict_info[it1]["Pc"]
        else:
            Pij = compute_Pioverj(i, it1, dict_info)
            prob *=  dict_info[it1]["Pc"] * Pij
    for it2 in lo:
        prob *= (1-dict_info[it2]["Pc"])
    for it3 in li:
        prob_temp = 1.0
        for it4 in li:
            if it3 != it4: # then Piover = 1 and focus plant is not in its own neighbour vector
                if it3 == i:
                    Pij = compute_Pioverj(i,it4,dict_info)
                elif it4 == i:
                    Pij = compute_Pioverj(it3,i,dict_info)
                else:
                    Pij = compute_Pioverj(it3,it4,dict_info)
                prob_temp *= Pij
        norm += prob_temp
    prob /= norm
    return(prob)

def float_range(start, stop, step):
    l = [start]
    while start < stop:
        start += step
        l.append(start)
    return(l)



def partitioning(i,nbrs, dict_info,plant_map,timestep):
    Sfu = 0.0
    deltat = dict_info[i]["Rp"]
    dt = deltat / timestep
    beg = (-deltat + dt/2)
    trange = float_range(beg,deltat-dt,dt)
    for t in trange:
        print(t)
        rho1, rho2, Rho_List = Get_Rho_List(t,i,nbrs, plant_map,dict_info)
        Rho_List.sort(key=lambda tup: tup[1])
        rhog = rho1
        rhod = rho2
        idx_list = []

        for value in Rho_List:
            rho_idx = value[0]
            rhod = value[1]
            if rhod > rho1:
                dSint = (rhod - rhog) * dt

                prob = 0.0
                rank = len(idx_list)-1
                l_a = pow(2,(rank+1))
                partition_IN = [[] for r in range(0,l_a)]
                partition_OUT = [[] for r in range(0,l_a)]

                for idx in idx_list:
                    for k in range(0,l_a):
                        p2r = pow(2,rank)
                        if (k+1)//p2r == pow(((k+1)//p2r)//2,2):
                            partition_IN[k].append(idx)
                        else:
                            partition_OUT[k].append(idx)
                    rank -= 1

                for k in range(0,l_a):
                    partition_IN[k].append(i)
                    prob += Get_Prob(i, dict_info, partition_IN[k], partition_OUT[k])
                Sfu += dSint*prob
            test = 0
            for idx in idx_list:
                if idx == rho_idx:
                    test = 1

            if rho_idx != i:
                if test == 0:
                    idx_list.append(rho_idx)
                else:
                    idx_list.remove(rho_idx)
    return(Sfu)

# sfu11 = double_partitioning_trigo(1, nbrs, dict_info,plant_map)
# sfu12 = computeSfu(1,nbrs,dict_info,plant_map, 50.0)
# print(sfu11 == sfu12)
# sfu21 = double_partitioning_trigo(2, nbrs, dict_info,plant_map)
# sfu22 = computeSfu(2,nbrs,dict_info,plant_map, 50.0)
# print(sfu21 == sfu22)

def LightCompetition(kb, dict_info,plant_map, nbrs,timestep, option_radius = "density"):
    for i in plant_map:
        compute_Sp(i,dict_info)
        compute_Pc(kb,i,dict_info)
    for i in plant_map:
        print(i)
        dict_info[i]["Sfu"] = computeSfu(i,nbrs,dict_info,plant_map,timestep)


dirname = "/home/meije/Documents/test5"
plant_map, crop_scheme, dict_info, nbrs = make_dico(dirname, "density")
LightCompetition(0.95, dict_info, plant_map, nbrs,50.0, "density")