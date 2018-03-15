# -*- coding:utf-8 -*-  


import os,os.path,sys
from odbAccess import *

elementL = 14930     #单元编号
instanceL = 'PART-1-1'  #节点编号
times,stress = [],[]
o = openOdb(path='dui100-s.odb',readOnly=False)
inst = o.rootAssembly.instances[instanceL]
ele = inst.getElementFromLabel(label=elementL)
frames = o.steps['Step-7'].frames
for frame in frames:
	times.append(frame.frameValue)
	fopS = frame.fieldOutputs['S']
	fopSFromEle = fopS.getSubset(region=ele)
	stress.append(fopSFromEle.values[0].mises)
print(times,stress)
o.close()