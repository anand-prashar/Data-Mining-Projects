'''
Created on Oct 28, 2016

@author: anand
'''

import math
import sys


getWeight = [ {'low' : 0, 'med' : 1, 'high' : 2, 'vhigh' : 3},  #0 buyingDict
              {'low' : 0, 'med' : 1, 'high' : 2, 'vhigh' : 3},  #1 maintDict
              {'2' : 0, '3' : 1, '4' : 2, '5more' : 3},         #2 doorsDict
              {'2' : 0, '4': 1, 'more' : 2},                    #3 personsDict
              {'small': 0, 'med' : 1, 'big': 2},                #4 lug_bootDict
              {'low': 0, 'med' : 1, 'high': 2}]                 #5 safetyDict


def readFile():
    
    fileInput = open(sys.argv[1])
    
    input_carList = []
    for fileRow in fileInput:
        listOfRow =  fileRow.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        input_carList.append(listOfRow[:])
    fileInput.close()
    
    fileInput = open(sys.argv[2])
    
    initialPointsList = []
    for fileRow in fileInput:
        listOfRow =  fileRow.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        initialPointsList.append(listOfRow[:-1])
    fileInput.close()  
    
    K = int(sys.argv[3])
    if (K != len(initialPointsList)):
        print 'Invalid K'
        exit()
    
    iterations = int(sys.argv[4])
          
    return (input_carList, initialPointsList, K, iterations)
    

def getDistanceMeasure(centroid, dataPoint):
    
    distance = 0.0

    for index in range( len(centroid)):
        diff = centroid[index] - float(getWeight[index][ dataPoint[index] ])
        distance += diff * diff 
 
    distance = math.sqrt(distance)
    return distance


def adjustClusters( currClustersList, input_carList, K):
    
    newClustersList = []
    for centroid in currClustersList:
        newClustersList.append([centroid[0], []])  # reset datapoints in cluster
    
    
    for dataPoint in input_carList:
        
        clusterDistance = []   
        for Kindex in range(0,K):
            clusterDistance.append( getDistanceMeasure( newClustersList[Kindex][0], dataPoint))
            
        selectedClusterId = clusterDistance.index( min(clusterDistance) )
        newClustersList[selectedClusterId][1].append( dataPoint )
            
    return newClustersList


def getCentroid( pointsList ):
    
    meanVector = [] 
    for dimension in range( len(getWeight)):   # 6 dimensions
        meanVector.append(0)
        
    for point in pointsList:
        for dimension in range( len(point)-1): # 6 dimensions
            meanVector[dimension] += getWeight[dimension] [ point[dimension]]
    
            
    
    for index in range( len(meanVector)):
        if( len(pointsList) != 0):   # if no data points available, dont divide below
            meanVector[index] = float(meanVector[index]) / len(pointsList)                
    return meanVector

def K_meansClustering(initialPointsList, input_carList, K, iterations):
    
   
    currClustersList = []
    
    for centroid in initialPointsList:
        numericCentroid = []
        for index in range(0,len(centroid)):
            numericCentroid.append(float(getWeight[index][centroid[index] ])) 
                                   
        currClustersList.append( [ numericCentroid, [] ])    # each row is a cluster in currClustersList, has its centroid id and its list of points 
    
  
    for i in range(1, iterations+1): #while centroidsChanged( prevClustersList,currClustersList ): 

        currClustersList = adjustClusters(currClustersList, input_carList, K)
        for index in range(0, len(currClustersList)):
            currClustersList[index][0] = getCentroid( currClustersList[index][1] ) # send a list of cluster's data points to get its means
            
        print 'i=',i,'\n'            
        for c in currClustersList:
            print c[0],':: instances=', len(c[1])
        print '-----------------\n'
    
    return  currClustersList   
        

def writeToFile(currClustersList):            
    # save to op
    fileWriter = open('anand_prashar_clustering.txt','w')
    
    wrongAssignedCount = 0 
    for c in currClustersList:
        labelCountDict= {'unacc' :0, 'acc' : 0, 'good' : 0, 'vgood' : 0}
        
        #assign label
        for labelIter in c[1]:
            labelCountDict[labelIter[-1]] = labelCountDict[labelIter[-1]] + 1
        label = max(labelCountDict, key= labelCountDict.get)
        
        fileWriter.write('cluster: '+label+'\n')
        
        for labelIter in c[1]:
            if labelIter[6] != label:
                wrongAssignedCount+=1
            fileWriter.write(str(labelIter)+'\n')    
        fileWriter.write('\n\n')    
    fileWriter.write('Number of points wrongly assigned:\n'+ str(wrongAssignedCount) )
    fileWriter.close()
    
    print '\nWrong assignment to Clusters = ', wrongAssignedCount            
    print 'OUTOUT FILE : anand_prashar_clustering.txt'
    
    return currClustersList         

#####################################################################################################################

# TO DO, PASS NO OF ITERATIONS ALSO ! - to K means clustering

(input_carList, initialPointsList, K, iterations) = readFile()

currClustersList = K_meansClustering(initialPointsList, input_carList, K, iterations)  

writeToFile(currClustersList)

      
    
    
    