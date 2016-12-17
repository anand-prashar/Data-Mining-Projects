
from gurobipy import *
import re
import random 
import numpy as np
#from collections import Counter

images = []
labels = []
trainImageNames = []
level1Inputs = []
testImages = []
testLabels = [] 
testImageNames = []
weightThr = 7000
pixelThr = 0.265
deltaWeight = 0.04
totalN = 5

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
            if a >= pixelThr:
                a = 1    
            else:
                a = 0
            im.append(a)
        image = im      
    #ct = Counter(image)
    #print ct  
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

def readTestImages():
    global testImages, testLabels, testImageNames
    #print "Testing begins"
    with open('downgesture_test.list') as f:
        for test_image in f.readlines():
            test_image = test_image.strip()
            testImageNames.append(test_image)
            testImages.append(load_pgm_image(test_image))
            if 'down' in test_image:
                testLabels.append(1)
            else:
                testLabels.append(0)
                
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
        
    for i in range(0, l1vertexCount*totalN):
        
        vertex = 'v'+str(i)
        vertexList.append(vertex)
        weightList.append( abs(random.randint(0,5)) )
        
        if i<l1vertexCount:
            level1.append(vertex)
        else: 
            if i<l1vertexCount*(totalN - 1):
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
readTestImages()
results = getGraph()

var_names = results[0]
weights = results[1]
edges = results[2]
constraints = []
cnames = []
vars_p = []
k = 0
constr_set = False
vars_set = False

for image,label in zip(images,labels):
    iters = 0
    sameImage = False
    while iters < 50 :
        try:
            if not vars_set:
                # Create a new model
            
                m = Model("mip1")
                exp = []
                i = 0
                node_name = 'n'
                
                for v, w in zip(var_names, weights):
                    vars_p.append(m.addVar(vtype = GRB.BINARY, name = v))
                    cnames.append('c' + v)
                m.update()
                vars_set = True
                vars_q = list(vars_p)
                
            if not sameImage:    
                for i in range(pixelSize):
                    vars_q[i] = image[i]
                    sameImage = True
                 
            if not constr_set:
                patternindex = re.compile(r"^[0-9+]$") #
                for e in edges:
                    v1 = [x for x in e[0] if patternindex.match(x)]
                    v1 = int(''.join(v1))
                    if v1 < pixelSize:
                        v1 = vars_q[v1]
                    else:
                        v1 = vars_p[v1]
                    if v1 ==1:
                        y = 0
                    v2 = [x for x in e[1] if patternindex.match(x)]
                    v2 = int(''.join(v2))
                    if v2 < pixelSize:
                        v2 = vars_q[v2]
                    else:
                        v2 = vars_p[v2]
                    temp = [v1, v2]
                    constraints.append(quicksum(x for x in temp))
                
                for ceq, c in zip(constraints, cnames):
                    m.addConstr(ceq >= 1, c)    
                constr_set = True
            
            sumv = quicksum(w * v2 for w, v2 in zip(weights, vars_q))
            m.setObjective(sumv, GRB.MINIMIZE)    
            m.setParam("OutputFlag",False)
            m.optimize()
            
            print "Weight",m.objVal
            if m.objVal <= weightThr and label == 1:
                weights = (np.array(weights) * (1 + deltaWeight)).tolist()
            elif m.objVal > weightThr and label == 0:
                weights = (np.array(weights) * (1 - deltaWeight)).tolist()
            else:
                print "Image trained",trainImageNames[k],"label",label,"\n"
                break 
            iters+=1
            
        except GurobiError as e:
            print('Error code ' + str(e.errno) + ": " + str(e))
        
        except AttributeError:
            print('Encountered an attribute error')
    k+=1

print "\n\n\nprediction"
j = 0
down = 0
up = 0
for imagetest,labeltest in zip(testImages,testLabels):
    try:
        if not vars_set:
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
            vars_q = list(vars_p)
            m.update()
        
        prev_vars = list(vars_q)
        prev_image = imagetest    
        for i in range(pixelSize):
            vars_q[i] = imagetest[i]
        if prev_vars == vars_q:
            print "Same"
            
        sumv = quicksum(w * v2 for w, v2 in zip(weights, vars_q))
        m.setObjective(sumv, GRB.MINIMIZE)
        if not constr_set:
            patternindex = re.compile(r"^[0-9+]$") #
            for e in edges:
                v1 = [x for x in e[0] if patternindex.match(x)]
                v1 = int(''.join(v1))
                if v1 < pixelSize:
                    v1 = vars_q[v1]
                else:
                    v1 = vars_p[v1]
                if v1 ==1:
                    y = 0
                v2 = [x for x in e[1] if patternindex.match(x)]
                v2 = int(''.join(v2))
                if v2 < pixelSize:
                    v2 = vars_q[v2]
                else:
                    v2 = vars_p[v2]
                temp = [v1, v2]
                constraints.append(quicksum(x for x in temp))
            
            for ceq, c in zip(constraints, cnames):
                m.addConstr(ceq >= 1, c)    
            constr_set = True
            
        m.setParam("OutputFlag",False)
        m.optimize()
        
        print "Weight",m.objVal,
        print testImageNames[j],
        if m.objVal > weightThr: 
            print "Predicted down"
            if labeltest ==1:
                down+=1
        else:
            print "Predicted not down"
            if labeltest ==0:
                up+=1
        j+=1
            
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))
        
    except AttributeError:
        print('Encountered an attribute error')


print
print "Total down predicted right",down
print "Total up predicted right",up
print "Accuracy", (down + up) / float(len(testImages))