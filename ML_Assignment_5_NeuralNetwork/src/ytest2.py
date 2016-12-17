'''
Created on Oct 29, 2016

@author: anand
'''

from snap import *


G1 = TNGraph.New()
G1.AddNode(1)
G1.AddNode(5)
G1.AddNode(32)
G1.AddEdge(1,5)
G1.AddEdge(5,1)
G1.AddEdge(5,32)


# generate a network using Forest Fire model
G3 = GenForestFire(1000, 0.35, 0.35) 
# save and load binary
FOut = TFOut("test.graph")
G3.Save(FOut)
FOut.Flush()
FIn = TFIn("test.graph")
G4 = TNGraph.Load(FIn)
# save and load from a text file
SaveEdgeList(G4, "test.txt", "Save as tab-separated list of edges")
G5 = LoadEdgeList(PNGraph, "test.txt", 0, 1)