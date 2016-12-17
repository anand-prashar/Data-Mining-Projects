'''
Created on Nov 4, 2016

@author: anand
'''

import random

    
def getGraph():
    
    level1 = []
    level2 = [] 
    level3 = []
    vertexList = []
    weightList = []
    edgeList = []
    
    l1vertexCount = 5
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
        
    return (vertexList, weightList, edgeList)  

print len(getGraph()[2])      
            
    