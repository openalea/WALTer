#!/usr/bin/python

from openalea.lpy import *
from openalea.plantgl.all import *
import sys

params = dict(map(lambda x: x.split('='), sys.argv[1:]))
#params = map(lambda x: x.split('='), sys.argv[1:])

print params

for key, item in params.items():
    try :
        params[key] = float(item)
    except:
        pass

print params

lsys = Lsystem('WALTer_v1-16.4.lpy',params)

#lsys.nbj = 10
#lsys.derivationLength = lsys.nbj
#lsys.animate()
lsys.iterate()
#ipython --gui=qt4
#s=lsys.sceneInterpretation(lstring)
#Viewer.display(s)


