
from gurobipy import *
from re import compile
import random 
import numpy as np
from collections import Counter
from itertools import chain
#from collections import Counter

images = []
labels = []
trainImageNames = []
level1Inputs = []
testImages = []
testLabels = [] 
testImageNames = []
weightThr = 6000
pixelThr = 0.25
deltaWeight = 0.01
totalN = 5
globalWeights = []
accuracies = []

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
        weightList.append( abs(random.randint(0,4)) )
        
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
constr_set = False
vars_set = False
iters = 0
choicearray = range(len(images))

img_cnt = Counter(labels)
while iters < 500 :
    print "\nEpoch ",iters+1
    imageruns = 0
    up_img = 0
    down_img = 0
    zero_labels = 0
    one_labels = 0
    vars_memory = []
    while imageruns < 50:
        k = np.random.choice(choicearray,replace = True)
        image = images[k]
        label = labels[k]
        if label == 1:
            one_labels +=1
        else:
            zero_labels +=1
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
                
            for i in range(pixelSize):
                vars_q[i] = image[i]
                sameImage = True
                 
            if not constr_set:
                patternindex = compile(r"^[0-9+]$") #
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
            
            vars_update = [y.varName for y in m.getVars() if y.x == 1]
            #print "vars",vars_update
            img_index = [i for i, x in enumerate(image) if x == 1]
            img_data = [var_names[i] for i in img_index]
            #print "image",img_data
            vars_union = list(set(vars_update).union(set(img_data)))
            #print "union",vars_union
            vars_memory.append(vars_union)
            #print "Vars in MWVC",len(m.getVars()),len(vars_update),len(img_data),len(vars_union)
            #print "Image",trainImageNames[k],"label",label
            #print "Weight",m.objVal
            if m.objVal <= weightThr and label == 1:
                down_img += 1
                #weights = (np.array(weights) * (1 + deltaWeight)).tolist()
            elif m.objVal > weightThr and label == 0:
                up_img += 1
                #weights = (np.array(weights) * (1 - deltaWeight)).tolist()
            imageruns+=1    
        except GurobiError as e:
            print('Error code ' + str(e.errno) + ": " + str(e))
        
        except AttributeError:
            print('Encountered an attribute error')
            
    globalWeights.append(weights)
    accuracy = (up_img + down_img) / 50.0
    accuracies.append(accuracy)
    print "total predicted right up, down", up_img, down_img,
    print "Accuracy", accuracy
    vars_repeated = list(chain.from_iterable(vars_memory))
    repeated_count = dict(Counter(vars_repeated))
    #print repeated_count
    if up_img / float(zero_labels) < down_img / float(one_labels):
        print "update for up"
        for p in repeated_count:
            #print p,type(repeated_count[p]),
            wIndex = var_names.index(p)
            weights[wIndex] += weights[wIndex] * int(repeated_count[p]) * deltaWeight
    else:
        print "update for down"
        for p in repeated_count:
            #print p,type(repeated_count[p]),
            wIndex = var_names.index(p)
            weights[wIndex] -= weights[wIndex] * int(repeated_count[p]) * deltaWeight
    
    iters+=1
        
print "\n\n\nprediction"
j = 0
down = 0
up = 0
#print "Highest accuracy", max(accuracies)
sortedAccuracies = list(accuracies)
sortedAccuracies.sort()
subset = np.array(sortedAccuracies)[np.array(sortedAccuracies) > 0.6]
print "accuracy chosen", subset[0]
weights = globalWeights[accuracies.index(subset[0])]
#weights = globalWeights[accuracies.index(max(accuracies))]
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
            
        sumv = quicksum(w * v2 for w, v2 in zip(weights, vars_q))
        m.setObjective(sumv, GRB.MINIMIZE)
        if not constr_set:
            patternindex = compile(r"^[0-9+]$") #
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
        if m.objVal < weightThr: 
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