#Minimize
#  +2 v1 +3 v2 +1 v3 +2 v4
#Subject to
#  v1 + v2 >= 1
#  v1 + v3 >= 1
#  v2 + v3 >= 1
# v3 + v4 >= 1
#Binary
# v1 v2 v3 v4
#End


from gurobipy import *
import re
import random 
import numpy as np

images = []
labels = []
trainImageNames = []
level1Inputs = []

def load_pgm_image(pgm):
    global xdim, ydim
    with open(pgm, 'rb') as f:
        f.readline()   # skip P5
        f.readline()   # skip the comment line
        f.readline().split()  # size of the image
        max_scale = int(f.readline().strip())
        endian = '>'
        image = np.fromfile(f, dtype = 'u1' if max_scale < 256 else endian+'u2')
        image = [int(str(x)) / float(max_scale) for x in image.tolist()]
        im = []
        for im1 in image:
            a = im1
            if a >= 0.001:
                a = 1    
            else:
                a = 0
            im.append(a)
        image = im        
    return image

def readTrainingImages():
    global images, labels, pixelSize, trainImageNames

    with open('downgesture_train.list') as f:
        for training_image in f.readlines():
            training_image = training_image.strip()
            trainImageNames.append(training_image)
            images.append(load_pgm_image(training_image))
            if 'down' in training_image:
                labels.append(1)
            else:
                labels.append(0)
    
    pixelSize = len(images[0])
    
def getGraph():
    global level1Inputs
    level1 = []
    level2 = [] 
    level3 = []
    vertexList = []
    weightList = []
    edgeList = []
    
    l1vertexCount = pixelSize
    thresholdProb = 0.6
        
    for i in range(0, l1vertexCount*7):
        
        vertex = 'v'+str(i)
        vertexList.append(vertex)
        weightList.append( abs(random.randint(0,10)) )
        
        if i<l1vertexCount:
            level1.append(vertex)
        else: 
            if i<l1vertexCount*6:
                level2.append(vertex)
            else:  level3.append(vertex) 
  
    # L1 connects to L2 AND L3          
    for v1l1 in level1:
        
        for v2l2 in level2:
            connProb= random.random()
            if connProb< thresholdProb: continue
            edgeList.append((v1l1,v2l2))
        
        for v3l3 in level3:
            connProb= random.random()
            if connProb< thresholdProb: continue
            edgeList.append((v1l1,v3l3))  
            
    # L2 connects to L3          
    for v2l2 in level2:
        
        for v3l3 in level3:
            connProb= random.random()
            if connProb< thresholdProb: continue
            edgeList.append((v2l2,v3l3))               
    
    level1Inputs = list(level1)
    return (vertexList, weightList, edgeList)

readTrainingImages()
results = getGraph()

var_names = results[0]#['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7']
weights = results[1]#[5, 2, 1, 1, 3, 8, 4]
edges = results[2]#[('v1', 'v4'), ('v1', 'v3'), ('v2','v6'),('v4', 'v7'), ('v2', 'v5')]

try:
    constraints = []
    cnames = []
    vars_p = []
    # Create a new model

    m = Model("mip1")
    exp = []
    i = 0
    node_name = 'n'
    
    for v, w in zip(var_names, weights):
        vars_p.append(m.addVar(vtype = GRB.BINARY, name = v))
        cnames.append('c' + v)
        ver_name = v
        #if i < pixelSize:
        #    ver_name = images[0][i]
        #    exp.append(str(w) + '*' + str(ver_name)  + '+')
        #    continue
        
        if i == len(weights) - 1:
            exp.append(str(w) + '*' + ver_name)  
            break
        else:
        #v = m.addVar(vtype = GRB.BINARY, name = v)
            exp.append(str(w) + '*' + ver_name  + '+')
            
        i+=1
    
    vars_q = list(vars_p)
    for i in range(pixelSize):
        vars_q[i] = images[5][i]
        
    #print vars
    m.update()
    st =''.join(exp)
    sumv = quicksum(w * v2 for w, v2 in zip(weights, vars_q))
    #print "quicksum", sumv
    m.setObjective(sumv, GRB.MINIMIZE)
    #m.setObjective(st.strip("'")[1], GRB.MINIMIZE)
    patternindex = re.compile(r"^[0-9+]$") #
    for e in edges:
        v1 = [x for x in e[0] if patternindex.match(x)]
        v1 = int(''.join(v1))
        if v1 < pixelSize:
            v1 = vars_q[v1]
        else:
            v1 = vars_p[v1]
        v2 = [x for x in e[1] if patternindex.match(x)] # concat the digits returned in the list
        v2 = int(''.join(v2))
        #print v1, v2
        if v2 < pixelSize:
            v2 = vars_q[v2]
        else:
            v2 = vars_p[v2]
        temp = [v1, v2]
        constraints.append(quicksum(x for x in temp))
    
    for ceq, c in zip(constraints, cnames):
        #print ceq
        m.addConstr(ceq >= 1, c)    
    
    print "calling optimizer"
    m.optimize()
    
    i = 0
    k = 0
    for v in m.getVars():
        if v.x ==1 or k ==1000: 
            #if k < pixelSize:
            print('%s %g' % (v.varName, v.x)),
            print "w", weights[var_names.index(v.varName)]
            #print "pixel", images[0][k]
            k+=1
            i+=1
    print('Obj: %g' % m.objVal)
    print "Total",i

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
    