'''
Created on Nov 4, 2016

@author: anand
'''

import random

def graph1():
    
    level1 = []
    level2 = [] 
    level3 = []
    graph = []
    graph.append(level1)
    graph.append(level2)
    graph.append(level3)
    
    partitionSize = 5
    
    for i in range(0, partitionSize):
        # build and label vertices
        level1.append([i])
        level2.append([i])
        level3.append([i])
        
    for i in range(0, partitionSize):    
        #build mapping   
        level12Index = None
        while( level12Index==None or len(level2[level12Index])!=1 ):
            level12Index = abs(random.randint(0, partitionSize) % partitionSize)
        level13Index = None
        while( level13Index==None or len(level3[level13Index])!=1 ):
            level13Index = abs(random.randint(0, partitionSize) % partitionSize)  
        
        #level1 connection with level 2 and 3  ==>    [l1_nodeI, [ (l2_connection, l2_weight),(l3_connection, l3_weight)] ]
        connProbability = float(random.randint(0, 10)) / 10 
        level1[i].append([(level2[level12Index][0], connProbability  ), 
                                  (level3[level13Index][0], float("{0:.2f}".format(1-connProbability)) )  ])
        
        level2[level12Index].append( [ ( level1[i][0], connProbability  )]  )
        level3[level13Index].append( [ ( level1[i][0], float("{0:.2f}".format(1-connProbability)) )] )

    
    for i in range(0, partitionSize):        
  
        #level2 connection with level3 and 1
        level23Index = random.randint(0, partitionSize)
        
        level23Index = None
        while( level23Index==None or len(level3[level23Index][1])!=1 ):
            level23Index = abs(random.randint(0, partitionSize) % partitionSize) 
 
        prob = level2[i][1][0][1]
        level2[i][1].append( (level3[level23Index][0], float("{0:.2f}".format(1-prob))) )
        
        level3[level23Index][1].append( (level2[i][0], float("{0:.2f}".format(1-prob))) )
    
    return graph    
        

tripartiteGraph = graph1()
for level in tripartiteGraph:
    print 'LEVEL:', tripartiteGraph.index(level)
    for vertex in level:
        print 'Node ',vertex[0],':', vertex[1]
    
    print '\n\n'    

    