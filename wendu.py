#-*-coding:UTF-8-*-
from odbAccess import *
from abaqusConstants import *
myodb=openOdb(path='F:/zhuanli/pingban42.odb',readOnly=False)
mysteps=myodb.steps
#myodb=session.viewports[session.currentViewportName].displayedObject
#hazset=myodb.rootAssembly.nodeSets['SET-BASEMETAL-HAZ']
myinstance=myodb.rootAssembly.instances['PART-1-1']
#myfield=mysteps['Step-138'].frames[2].fieldOutputs['NT11']
subfieldvalues=mysteps['Step-3'].frames[1].fieldOutputs['NT11'].values

inode=len(subfieldvalues)

istep=len(myodb.steps)    #分析步(steps)的个数

iistep=istep//2

#maxtemp=myodb.steps['Step-36'].frames[9].fieldOutputs['NT11']
#newfield.addData(field=maxtemp)
nodelabel=[]
tempdata=[]
tempdata2=[]

#该循环对第一个增量步的所有节点取温度值
for n in range(inode):
    myvalue=subfieldvalues[n]
    nodelabel.append(myvalue.nodeLabel)
    tempdata.append(myvalue.data)

#该外层循环取了所有加热分析步(steps)的所有增量步(increments)
#每一步画一次图？
for s in range(1,iistep):
    ss=(s)*2+3           #这个地方有点问题
    sss='Step-'+str(ss)
    myframes=mysteps[sss].frames     #frames对象代表这一步的所有增量
    iframe=len(myframes)

    for f in range(iframe):
    	#取第f个增量步(increments)的所有节点的nt11值
        mysubfieldvalues=myframes[f].fieldOutputs['NT11'].values
        #遍历所有节点，如果某个节点的温度值比temp1更大，就更新tempdata
        for n in range(inode):
            temp1=tempdata[n]
            temp2=mysubfieldvalues[n].data
            if temp2<=temp1: continue
            else:
                tempdata[n]=temp2
        print sss,'frame-',f,' ended'
    print sss,'is ended'
    #取出该步的更新后的各节点温度(NT11)值
    for n in range(inode):
        ttemp=(tempdata[n],)
        tempdata2.append(ttemp)    #tempdata2包括所有分析步的更新后的节点值

#    print tempdata
    newstep=myodb.Step(name='Step-688',description='weldline',domain=TIME,timePeriod=1.0)
    newframe=newstep.Frame(incrementNumber=0,frameValue=0.1)
    newfield=newframe.FieldOutput(name='NT11',description='weldtemp',type=SCALAR)
    newfield.addData(position=NODAL,instance=myinstance,labels=nodelabel,data=tempdata2)
    myodb.save()
    myodb.close()
    print 'All is ended'