'''
Created on Nov 14, 2016

@author: anand
'''
import sys
import six
import community
import girvanNeuman
import networkx as nx
from matplotlib import colors
import matplotlib.pyplot as plt


def readFile():
    fHandle = open('input_test2.txt')#sys.argv[1])
    nodeList = set();edgeList = set()
    
    for fileRow in fHandle:
        node1,node2 = fileRow.split(' ')
        node1 = int(node1)                       
        node2 = int(node2.split('\n')[0])
        nodeList.add(node1)
        nodeList.add(node2)
        if node1<node2:   edgeList.add((node1,node2)) 
        else: edgeList.add((node2,node1)) 
    
    nodeList = sorted( list(nodeList))    
    edgeList = sorted( list(edgeList))
    return (nodeList,edgeList)    

def createGraph(nodeList,edgeList):
    
    G=nx.Graph()
    G.add_nodes_from(nodeList)
    G.add_edges_from(edgeList)
    G = G.to_undirected()

    #nx.draw_networkx(G, arrows=False, with_labels = True)
    #plt.axis('off')
    #plt.show()
    
    return G


def get_Partitions(nodeList, inputGraph):
    
    partitionNo = 1
    partitionDict = {}
    nodeListCp = nodeList[:]
    
    while nodeListCp != []:
        node = nodeListCp[0]
        propagte_and_removeEdge(node, nodeListCp, partitionDict, inputGraph, partitionNo)
        partitionNo +=1
        
    return partitionDict    

def propagte_and_removeEdge(node, nodeList, partitionDict, inputGraph, partitionNo):
    
    neighborsList = []
    try:
        nodeList.remove(node)
        partitionDict.setdefault(node,partitionNo)
        try:
            neighborsList = inputGraph.neighbors(node)
        except AttributeError: pass
        
        for neighbor in neighborsList:
            propagte_and_removeEdge(neighbor, nodeList, partitionDict, inputGraph, partitionNo)
            
    except ValueError: # Do nothing, if it was already removed
        return

def getBestCommunityGraph(inputGraph, nodeList):
    
    bestModularity = -1
    bestGraph = None
    originalG = inputGraph.copy()
    
    while inputGraph.edges()!=[]:
        
        partition = get_Partitions(nodeList, inputGraph) 
        try:
            currModularity = community.modularity( partition, originalG ) 
            print '\n\nModularity = ', currModularity
            print 'Partition = ', partition
        except ValueError: 
            continue
            #print 'Modularity = undefined'

        
        if bestModularity < currModularity:
            bestModularity = currModularity
            del bestGraph
            bestGraph = inputGraph.copy()
            
        #edgeBetweennessValues = nx.edge_betweenness(inputGraph)              # <------------------------------- existing library
        edgeBetweennessValues = girvanNeuman.edge_betweenness(inputGraph)     # <------------------------------- own implementation
        
        maxValue = -1
        for value in edgeBetweennessValues.itervalues():
            if maxValue < value:
                maxValue = value
            
        for breakEdge,value in edgeBetweennessValues.iteritems():
            if value == maxValue:
                inputGraph.remove_edge(breakEdge[0], breakEdge[1])
                #print '\nMax betweenness for: ',breakEdge,' .... Value=',maxValue  

    return bestGraph

def getColorList():
    sixColorList = list(six.iteritems(colors.cnames))
    
    for cName, rgb in six.iteritems(colors.ColorConverter.colors):
        rgbToHexVal = colors.rgb2hex(rgb)
        sixColorList.append((cName, rgbToHexVal))
    return sixColorList
    
         
######################################################################################################################
######################################################################################################################


(nodeList, edgeList) = readFile()
inputGraph = createGraph(nodeList, edgeList)
inputGraphBkp = inputGraph.copy()

bestGraph = getBestCommunityGraph(inputGraph, nodeList)

########### OUTPUT TO CONSOLE #############

partitions = get_Partitions(nodeList, bestGraph)
clusters=[] 
maxPartition= 0
for key,value in partitions.iteritems():   
    if maxPartition< value:
        maxPartition = value
for i in range(0,maxPartition):
    clusters.append([])
for key,value in partitions.iteritems():   
    clusters[value-1].append(key)
for cluster in clusters:
    print sorted(cluster)    

############## GUI OP ####################

pos = nx.spring_layout(inputGraphBkp)
count = 0

colors = getColorList() #['red','blue','green','yellow','cyan','magenta','grey','black','purple']
for com in set(partitions.values()):
    list_nodes = [nodes for nodes in partitions.keys() if partitions[nodes] == com]
    color = colors[count % len(colors)]
    
    nx.draw_networkx_nodes(inputGraphBkp, pos, list_nodes, node_size = 270, node_color= color, with_labels=True)
    count = count + 1

nx.draw_networkx_labels(inputGraphBkp, pos)    
nx.draw_networkx_edges(inputGraphBkp, pos, alpha=0.5)

plt.axis('off')
plt.savefig('op.png')#sys.argv[2])
#print '\nImage file saved as : ',sys.argv[2]
plt.show()  
    

