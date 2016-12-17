'''
Created on Oct 28, 2016

@author: anand
'''

import math

getWeight = [ {'low' : 0, 'med' : 1, 'high' : 2, 'vhigh' : 3},  #0 buyingDict
              {'low' : 0, 'med' : 1, 'high' : 2, 'vhigh' : 3},  #1 maintDict
              {'2' : 0, '3' : 1, '4' : 2, '5more' : 3},         #2 doorsDict
              {'2' : 0, '4': 1, 'more' : 2},                    #3 personsDict
              {'small': 0, 'med' : 1, 'big': 2},                #4 lug_bootDict
              {'low': 0, 'med' : 1, 'high': 2}]                 #5 safetyDict


#getWeight = [ {'low' : 1, 'med' : 2, 'high' : 3, 'vhigh' : 4},  #0 buyingDict
#              {'low' : 1, 'med' : 2, 'high' : 3, 'vhigh' : 4},  #1 maintDict
#              {'2' : 1, '3' : 2, '4' : 3, '5more' : 4},         #2 doorsDict
#              {'2' : 1, '4': 2, 'more' : 3},                    #3 personsDict
#              {'small': 1, 'med' : 2, 'big': 3},                #4 lug_bootDict
#              {'low': 1, 'med' : 2, 'high': 3}]                 #5 safetyDict


def readFile():
    
    fileInput = open('input_car')
    
    input_carList = []
    for fileRow in fileInput:
        listOfRow =  fileRow.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        input_carList.append(listOfRow[:])
    fileInput.close()
    
    fileInput = open('initialPoints')
    
    initialPointsList = []
    for fileRow in fileInput:
        listOfRow =  fileRow.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        initialPointsList.append(listOfRow[:-1])
    fileInput.close()    
    
    return (input_carList, initialPointsList)
    

def getDistanceMeasure(centroid, dataPoint):
    
    distance = 0.0

    for index in range( len(centroid)):
        try:
            diff = getWeight[index][ centroid[index] ] - getWeight[index][ dataPoint[index] ]
            normalizedDiff = float(diff) / len(getWeight[index])
            distance += normalizedDiff * normalizedDiff 
        except KeyError as e:
            print 'EXCEPTION', e
            exit()    
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
        #newClustersList[selectedClusterId][0] = newClustersList[selectedClusterId][0]
        newClustersList[selectedClusterId][1].append( dataPoint )
            
    return newClustersList

def getMeanVector( pointsList ):
    
    meanVector = [] 
    for dimension in range( len(getWeight)):   # 6 dimensions
        meanVector.append(0)
        
    for point in pointsList:
        for dimension in range( len(point)-1): # 6 dimensions
            meanVector[dimension] += getWeight[dimension] [ point[dimension]]
    
            
    
    for index in range( len(meanVector)):
        if( len(pointsList) != 0):   # if no data points available, dont divide below
            meanVector[index] = round( float(meanVector[index]) / len(pointsList) ) 
            for key,value in getWeight[index].iteritems():
                if (value == meanVector[index]):
                    meanVector[index] = key  # replace some number with values like 'low' 'med' etc
                    break
               
    return meanVector

def centroidsChanged(prevClustersList, currClustersList):
    
    if prevClustersList == []: return True
    matchCount = 0  
    
    for index in range( len(prevClustersList)):
#        for prevListCentroid in prevClustersList[index] :
#            if prevClustersList[0] == prevClustersList[index][0]
        if(prevClustersList[index][0] == currClustersList[index][0]):
            matchCount+=1
    if matchCount == len(currClustersList):
        return False
    else:
        return True

def K_meansClustering(initialPointsList, input_carList, K):
    
    #prevClustersList = []
    currClustersList = []
    
    for centroid in initialPointsList:
        currClustersList.append( [ centroid, [] ])    # each row is a cluster in currClustersList, it has its centroid id and its list of points 
    
    for i in range(0, 5): #while centroidsChanged( prevClustersList,currClustersList ): 
        
        for c in currClustersList:
            print c[0] ,'  ::', len(c[1])
        print '-----------------\n'
        
    #    prevClustersList = currClustersList
        currClustersList = adjustClusters(currClustersList, input_carList, K)
        
        # calculate new centroids
        for index in range(0, len(currClustersList)):
            currClustersList[index][0] = getMeanVector( currClustersList[index][1] ) # send a list of cluster's data points to get its means
            
    # save to op
    fileWriter = open('OutputSample.txt','w')
    
    wrongAssignedCount = 0 
    for c in currClustersList:
        labelCountDict= {'unacc' :0, 'acc' : 0, 'good' : 0, 'vgood' : 0}
    
        for labelIter in c[1]:
            labelCountDict[labelIter[6]] = labelCountDict[labelIter[6]] + 1
        label = max(labelCountDict, key= labelCountDict.get)
        
        fileWriter.write('cluster: '+label+'\n')
        
        for labelIter in c[1]:
            if labelIter[6] != label:
                wrongAssignedCount+=1
            fileWriter.write(str(labelIter)+'\n')    
        fileWriter.write('\n\n')    
    fileWriter.write('Number of points wrongly assigned:\n'+ str(wrongAssignedCount) )
    fileWriter.close()
    
    print '\nWrong assigned = ', wrongAssignedCount            
    
    return currClustersList        
            
                
#####################################################################################################################

# TO DO, PASS NO OF ITERATIONS ALSO ! - to K means clustering

(input_carList, initialPointsList) = readFile()
finalClusters = K_meansClustering(initialPointsList, input_carList, 4)  

print'---------------------------TESTING------------------------------------'
centroid1 = finalClusters[0][0]
centroid2 = finalClusters[1][0]
centroid3 = finalClusters[2][0]
centroid4 = finalClusters[3][0]

commonDistance = 0
for dataPoint in finalClusters[3][1]:
    c1=  getDistanceMeasure(centroid1, dataPoint)
    c2 = getDistanceMeasure(centroid2, dataPoint)
    c3 = getDistanceMeasure(centroid3, dataPoint)
    c4 = getDistanceMeasure(centroid4, dataPoint)
    
    #if (c1>c2 or c1>c3 or c1>c4):
    if (c2>c1 or c2>c3 or c2>c4):
    #if (c3>c1 or c3>c2 or c3>c4):
    #if (c4>c1 or c4>c2 or c4>c3):
        commonDistance+=1
    #print dataPoint,'-',c1,'-',c2,'-',c3,'-',c4

#print commonDistance        
    
    
    