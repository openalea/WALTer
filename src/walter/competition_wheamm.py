import math

def compute_Pci(density,kb,Sfi):
    Sd = 1 / density
    Pci = 1 - math.exp(-kb * Sfi / Sd)
    return(Pci)


def compute_Pioverj(hi, hj, K=0.5):
    Pioverj = 1 / (1 + math.exp(-K*(hi-hj)))
    return(Pioverj)


def compute_Probai(density,kb,Sfi,hi,hj,K=0.5):
    Pci = compute_Pci(density,kb,Sfi)
    Pioverj = compute_Pioverj(hi,hj,K)
    return(Pci, Pioverj)


def triple_intersection(neighbours, xi, yi, Spi):
    if len(neighbours) < 2:
        return(0)
    else:
        for j in neighbours:
            for k in neighbours:
                if k > j:
                    rspi = math.sqrt(Spi/math.pi)
                    rspj = math.sqrt(neighbours[j]["Sp"]/math.pi)
                    rspk = math.sqrt(neighbours[k]["Sp"]/math.pi)

                    dij = math.sqrt(pow((xi - neighbours[j]["x"]),2) + pow((yi - neighbours[j]["y"]),2))
                    dik = math.sqrt(pow((xi - neighbours[k]["x"]),2) + pow((yi - neighbours[k]["y"]),2))
                    djk = math.sqrt(pow((neighbours[j]["x"] - neighbours[k]["x"]),2) + pow((neighbours[j]["y"] - neighbours[k]["y"]),2))
                    if rspi+rspj > dij and rspi+rspk > dik and rspj+rspk > djk:
                        return(1)
        return(0)


def default_neighbours(density):
    neighbours = {}
    neighbours[2] = {}
    neighbours[3] = {}
    neighbours[2]["x"] = 0.0
    neighbours[3]["x"] = 0.05
    neighbours[2]["y"] = 0.0
    neighbours[3]["y"] = 0.05
    neighbours[2]["Sp"] = neighbours[3]["Sp"] = 1 / density
    neighbours[2]["height"] = neighbours[3]["height"] = 50.0
    neighbours[2]["Pc"] = neighbours[3]["Pc"] = 1.0
    return(neighbours)



def Get_Rho_List(t,i,Spi,xi,yi,neighbours):
    # rho1 and rho 2 for plant i
    dsqri = math.sqrt(Spi/math.pi - pow(t,2))
    rho1 = yi - dsqri
    rho2 = yi + dsqri
    Rho_List = [(i,rho1),(i,rho2)]

    for j in neighbours:
        dsqrj2 = neighbours[j]["Sp"]/math.pi - pow((t + xi - neighbours[j]["x"]),2)
        if dsqrj2 > 0:
            dsqrj = math.sqrt(dsqrj2)
            rho1_temp = neighbours[j]["y"] - dsqrj
            rho2_temp = neighbours[j]["y"] + dsqrj

            if rho1_temp < rho2 and rho1_temp > rho1:
                Rho_List.append((j,rho1_temp))
            if rho2_temp < rho2 and rho2_temp > rho1:
                Rho_List.append((j,rho2_temp))
    return(rho1, rho2, Rho_List)


def Get_Prob(i, Pci, hi, neighbours, li, lo,type):
    prob = 1.0
    if type == "homogeneous":
        for it1 in li:
            if it1 == i:
                prob *= Pci
            else:
                prob *= neighbours[it1]["Pc"]
        if len(lo) > 0:
            for it2 in lo:
                if it2 == i:
                    print("weird")
                    prob *= (1 - Pci)
                else:
                    prob *= (1 - neighbours[it2]["Pc"])
        prob /= len(li)
    else:
        prob_temp = 1.0
        norm = 0.0
        for it1 in li:
            if it1 == i:
                prob *= Pci
            else:
                Pij = compute_Pioverj(hi,neighbours[it1]["height"])
                prob *=  neighbours[it1]["Pc"] * Pij
        for it2 in lo:
            prob *= (1-neighbours[it2]["Pc"])
        for it3 in li:
            prob_temp = 1.0
            for it4 in li:
                if it3 != it4: # then Piover = 1 and focus plant is not in its own neighbour vector
                    if it3 == i:
                        Pij = compute_Pioverj(hi,neighbours[it4]["height"])
                    elif it4 == i:
                        Pij = compute_Pioverj(neighbours[it3]["height"],hi)
                    else:
                        Pij = compute_Pioverj(neighbours[it3]["height"],neighbours[it4]["height"])
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



def partitioning(i,Spi,Pci, neighbours,timestep,type):
    Sfu = 0.0
    deltat = math.sqrt(Spi/math.pi) # radius of spi
    dt = deltat / timestep
    beg = (-deltat + dt/2)
    trange = float_range(beg,deltat-dt,dt)
    for t in trange:
        print(t)
        rho1, rho2, Rho_List = Get_Rho_List(t,i,Spi,xi,yi,neighbours)
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
                    prob += Get_Prob(i, Pci, hi, neighbours,partition_IN[k], partition_OUT[k],type)
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

Pci=1.0
density = 160.0
kb = 1.95
Sfi = 2.0
hi = 50.0
neighbours = default_neighbours(density)
xi = 0.05
yi=0.0
Spi=1/density
test = partitioning(i,Spi,Pci,neighbours,50.0,"heterogeneous")


