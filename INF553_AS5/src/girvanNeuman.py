'''
Created on Nov 23, 2016

@author: anand
NOTE : edge_betweenness method [Line 100] is called from other Python module files...
rest all methods just support the logic in this file
'''
import networkx as nx

class TreeNode:
    
    def __init__(self, name, parents = None, children = None ):
        self.nodeName = name
        if parents == None: self.parents = []
        else: self.parents = [parents]
        if children == None: self.children = []
        else: self.children = [children]
        
        self.nodeWeight = 1.0


class Tree:
    
    def __init__(self,nodeName = None):
        tempNode = TreeNode(nodeName)
        self.treeStr = []
        self.treeStr.append( [tempNode] ) #root    
            
    def searchNode(self, searchNodeName):    
        levelId = 0  
        for level in self.treeStr:
            for node in level:
                if node.nodeName == searchNodeName:
                    return (node ,levelId)
            levelId+=1    
        return None    
    
    def addNode(self, nodeName = None, parent = None):    
        if nodeName == None or parent == None: return False
        
        searchResponseP = self.searchNode(parent)
        if searchResponseP == None: return False
        (searchedParent,parentLevel) = (searchResponseP[0],searchResponseP[1])
        
        searchResponse = self.searchNode(nodeName)
        if searchResponse == None: currentNode = TreeNode(nodeName, searchedParent.nodeName) # new node + uplink from child
        else: 
            (currentNode,currLevel) = (searchResponse[0],searchResponse[1])
            if parentLevel == currLevel: return False
            if searchedParent.nodeName in currentNode.parents: return False   # Edge already exists
            currentNode.parents.append(searchedParent.nodeName) # add parent to existing node
        
 
        searchedParent.children.append(currentNode.nodeName) # create downlink from parent
        
        if searchResponse ==None:
            if len(self.treeStr) == parentLevel+1:
                self.treeStr.append([])
            self.treeStr[parentLevel+1].append(currentNode)
        return True
    
    def printTree(self):
        
        levelId = 0  
        for level in self.treeStr:
            print '\n\nLEVEL-',str(levelId)
            for node in level:
                print node.nodeName,' : Parent=', node.parents,' Children=' ,node.children 
            levelId+=1  
    
    def edgeWeightUpdate(self,edgeWeightDict):
        
        #if edgeWeightDict == {}: return self.edgeDictionary
         
        maxLevel = len(self.treeStr)-1
        
        while maxLevel >0:
            for node in self.treeStr[maxLevel]:
                for passToParent in node.parents:
                    
                    weightFraction = node.nodeWeight / len(node.parents)
                    dictKey = tuple(sorted([node.nodeName, passToParent]) )

                    if dictKey in edgeWeightDict:
                        edgeWeightDict[dictKey] += weightFraction
                    else:    
                        edgeWeightDict.setdefault( dictKey, weightFraction ) 
                   
                    for upParent in self.treeStr[maxLevel-1]:
                        if upParent.nodeName == passToParent:
                            upParent.nodeWeight += weightFraction                    
                            
            maxLevel-=1
             
        return edgeWeightDict  
            

####-------------------------- OWN IMPLEMENTATION OF BETWEENNESS FN------------------------------

def edge_betweenness(inputGraph):
        
    currVertexList = list( inputGraph.nodes_iter() )
    edgeWeightDict = {}
    
    for sourceVertex in currVertexList:
        
        tree = Tree(sourceVertex)
    
        traverseNodes = currVertexList[:]
        traverseNodes.remove(sourceVertex)
        
        for targetVertex in traverseNodes:
            try:
                # use shortest path information to build BFS Tree, for each node in sourceVertex
                allShortestPaths_X_to_Y =  list(nx.all_shortest_paths(inputGraph, sourceVertex, targetVertex))
                for path in allShortestPaths_X_to_Y:
                    while len(path)> 1:
                        parent = path[0]
                        child = path[1]
                        tree.addNode(child, parent)
                        del path[0]
            except nx.exception.NetworkXNoPath: pass
           

        tree.edgeWeightUpdate(edgeWeightDict)    
        del tree.treeStr 
    
    #if self loop exists
    edgeList = inputGraph.edges()
    for edgeTuple in edgeList:
        if edgeTuple[0]==edgeTuple[1]: 
            edgeWeightDict.setdefault( tuple(edgeTuple),0.0)
    
    #now, divide all edge weights by 2
    for key in edgeWeightDict.iterkeys(): 
        edgeWeightDict[key]/=2        

    return edgeWeightDict                 
