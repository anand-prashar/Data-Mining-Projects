import math
import numpy as np
import networkx as nx
import community
import matplotlib.pyplot as plt
import sys

# Read the input file into a graph
G=nx.Graph()
dataFileName = 'input_test1.txt'#sys.argv[1]
f = open(dataFileName)
for i in f:
    i = i.strip()
    i = i.split(' ')
    for j in i:
        G.add_node(int(j))
    if i[0] != i[1]:
        G.add_edge(int(i[0]),int(i[1]))
G_original = G.copy()


# construct a bfs tree from one source node and return the bfs tree as directed graph in networkx
def bfs_tree(graph,source_node):
    par_chi_dic = {}
    par_chi_dic[source_node] = []
    wait_list = []
    visited = []
    wait_list.append(source_node)
    level = {}
    level[source_node] = 0
    while len(wait_list)>0:
        par_chi_dic[wait_list[0]]=[]
        for i in list(graph.edges(wait_list[0])):
            if i[0] in level and i[1] not in level:
                level[i[1]] = level[i[0]]+1
            if i[1] in level and i[0] not in level:
                level[i[0]] = level[i[1]]+1
            if level[i[0]] == level[i[1]]+1:
                if i[0] !=wait_list[0]:
                    par_chi_dic[wait_list[0]].append(i[0])
                if i[0] not in wait_list:
                    wait_list.append(i[0])
            if level[i[1]] == level[i[0]]+1:
                if i[1] != wait_list[0]:
                    par_chi_dic[wait_list[0]].append(i[1])
                if i[1] not in wait_list:
                    wait_list.append(i[1])
        temp = wait_list.pop(0)
        if temp not in visited:
            visited.append(temp)
    my_bfs_tree = nx.DiGraph()
    for node,edges in par_chi_dic.items():
        my_bfs_tree.add_node(node)
        for edge in edges:
            my_bfs_tree.add_edge(node,edge)
    return my_bfs_tree


# use bfs_tree to construct bfs tree from source node, and calculate shortest path number for each node from source node, and then using girvan newman algorithm to calculate betweenness from source ndoe
def betweenness_1node(graph,source_node):
    my_bfs_tree = bfs_tree(graph,source_node)
    shorttest_path_num_dic = {}
    shorttest_path_num_dic[source_node]=1
    wait_list2 = []
    wait_list2.append(source_node)
    visited2 = []
    while len(wait_list2)>0:
        temp = wait_list2.pop(0)
        visited2.append(temp)
        for i in list(my_bfs_tree.edges(temp)):
            for j in i:
                if j not in visited2:
                    shorttest_path_num_dic[j] = shorttest_path_num_dic.get(j,0)+1
                    wait_list2.append(j)
    leaves = [x for x in my_bfs_tree.nodes_iter() if my_bfs_tree.out_degree(x)==0]
    # print leaves
    between_node = {}
    between_edge = {}
    for i in leaves:
        between_node[i] = 1
    wait_list = [i for i in leaves]
    while len(wait_list)>0:
        paren = my_bfs_tree.predecessors(wait_list[0])
        for p in paren:
            if p not in between_node:
                wait_list.append(p)
                flag = 1
                for c in my_bfs_tree.successors(p):
                    if c not in between_node:
                        flag = 0
                if flag ==1:
                    for c in my_bfs_tree.successors(p):
                        between_edge[(p,c)] = float(between_node[c])/shorttest_path_num_dic[c]*shorttest_path_num_dic[p]
                        between_node[p] = between_node.get(p,1)+float(between_node[c])/shorttest_path_num_dic[c]*shorttest_path_num_dic[p]

        wait_list.pop(0)
    return between_edge

# calculate betweenness from each node using betweenness_1node function, sum them up, and then divide by 2
def betweenness(graph):
    edges_betweenness = {}
    for node in list(graph.nodes()):
        bet_1node = betweenness_1node(graph,node)
        for k,v in bet_1node.items():
            k = ((k[0],k[1]) if k[0]<k[1] else (k[1],k[0]))
            edges_betweenness[k] = edges_betweenness.get(k,0) + v

    for k,v in edges_betweenness.items():
        edges_betweenness[k] = v/2
    return edges_betweenness
betweenness(G)


# a simple function to get all reachable node from source node using bfs
def bfs_node(graph,node):
    bfs_node = []
    bfs_node.append(node)
    waited_node = []
    waited_node.append(node)
    while len(waited_node) != 0:
        for i in graph.edges(waited_node[0]):
            if i[1] not in bfs_node:
                waited_node.append(i[1])
                bfs_node.append(i[1])
            if i[0] not in bfs_node:
                waited_node.append(i[0])
                bfs_node.append(i[0])
        waited_node.pop(0)
    return bfs_node


# according betweenness, cut the edges with the highest betweenness
def partition(G):
    flag = 1
    while flag == 1:
        flag = 0
        edge_betweenness = betweenness(G)
        sort_edge_between = sorted([(value,key) for (key,value) in edge_betweenness.items()])
        cut_edges = []
        for k,v in sort_edge_between:
            if k == sort_edge_between[-1][0]:
                cut_edges.append(v)
        for i in cut_edges:
            G.remove_edge(i[0],i[1])
        unvisited_nodes = list(G.nodes())
        part_diction = {}
        label = 0
        while len(unvisited_nodes)>0:
            bfs0 = bfs_node(G, unvisited_nodes[0])
            for i in list(bfs0):
                part_diction[i] = label
                unvisited_nodes.remove(i)
            label +=1
    return G, part_diction

unvisited_nodes = list(G.nodes())
part_dic = {}
label = 0
while len(unvisited_nodes)>0:
    bfs0 = bfs_node(G, unvisited_nodes[0])
    for i in list(bfs0):
        part_dic[i] = label
        unvisited_nodes.remove(i)
    label +=1

mod_G_list = []
if len(list(G.edges())) == 0:
    mod = None
else:
    mod = community.modularity(part_dic,G)
    print '\n\nModularity=', mod
    print part_dic    
    print 'Edges=',sorted( G.edges())
    
mod_G_list.append((mod,part_dic.items()))

while len(list(G.edges())) > 0:
    label = 1
    G, part_dic = partition(G)

    if len(list(G.edges()))==0:
        mod = None
    else:
        mod = community.modularity(part_dic,G_original)
        
        print '\n\nModularity=', mod
        print part_dic
        print 'Edges=',sorted( G.edges())
        
    mod_G_list.append((mod,part_dic.items()))

# get the partion with the highest modularity
lar_mod = sorted(mod_G_list,reverse=True)[0][0]
partition = sorted(mod_G_list,reverse=True)[0][1]
partition_dic = {}
for i in partition:
    if i[1] not in partition_dic:
        partition_dic[i[1]] = []
    partition_dic[i[1]].append(i[0])

partition_output = []
for k,v in partition_dic.items():
    partition_output.append(v)
partition_output.sort()
for i in partition_output:
    print i

# plot best partion
partition = dict(partition)
values = [partition.get(node) for node in G_original.nodes()]
nx.draw_spring(G_original, cmap = plt.get_cmap('jet'), node_color = values,  with_labels=True)
#plt.savefig(sys.argv[2]) # save as png
plt.show() # display