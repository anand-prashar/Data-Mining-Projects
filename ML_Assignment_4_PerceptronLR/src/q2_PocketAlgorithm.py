'''
Created on Oct 16, 2016

@author: anand
'''
import random
import matplotlib.pyplot as plt

theta = 5
learningRate = 0.01
maxNoOfIterations = 7000
featureMatrix = []
providedOP=[]
weights = []
XAxisIterations = []
YAxisMisClassed = []
ZWeightMemory = []

def readFile():
    
    global featureMatrix, providedOP
    
    fileData = open ('classification.txt')
    for fileLine in fileData:
        coordinate = fileLine.split(',')
        featureMatrix.append( [ float(coordinate[0]), float(coordinate[1]), float(coordinate[2]) ] )
        providedOP.append(float(coordinate[4]))

            

def calculateHyperPlane():
    
    global featureMatrix, providedOP, weights, maxNoOfIterations
    
    # update random weights
    for i in range(0,3):
        weights.append( float(random.randint(0,1)))
    weights.append(float(1)) # = w0    
    
    globalError = 0
    localError = 0
    pocketIteration = 1
    firstRun = True
    
    while( (globalError!=0.0 and maxNoOfIterations>=pocketIteration) or firstRun):
        firstRun = False
        globalError = 0
    
        for index in range( len(featureMatrix)):
            calculatedOP = calculateTrainingOP(theta,weights, featureMatrix[index] )
            localError = providedOP[index] - calculatedOP 
            
            for itr in range( len(weights)-1):
                weights[itr] += learningRate * localError * featureMatrix[index][itr]
            weights[len(weights)-1] += learningRate * localError # new W0
            globalError += localError*localError  
        
        validate(pocketIteration)   
        pocketIteration+=1
    
    #print '| global error=',globalError,' . Iteration=',maxNoOfIterations
        
        
def calculateTrainingOP(theta,weights, featureMatrixRow):
    
    #for( i in rang ):
    weightedSum = featureMatrixRow[0]*weights[0] + featureMatrixRow[1]*weights[1] + featureMatrixRow[2]*weights[2] + weights[3]    
    if weightedSum >= theta:
        return 1
    else:
        return -1

def validate(pocketIteration): 
    global featureMatrix, weights, providedOP, theta, XAxisIterations, YAxisMisClassed, ZWeightMemory
    
    misClassifiedPCount = 0
    itr = 0
    for featureMatrixRow in featureMatrix:
        
        wsum = featureMatrixRow[0]*weights[0] + featureMatrixRow[1]*weights[1] + featureMatrixRow[2]*weights[2] + weights[3]
        if wsum >= theta:
            if 1.0 != providedOP[itr]: misClassifiedPCount+=1
        else:
            if -1.0 != providedOP[itr]: misClassifiedPCount+=1
        itr+=1 
    
    #store info in list - plot later
    XAxisIterations.append(pocketIteration)
    YAxisMisClassed.append(misClassifiedPCount)
    ZWeightMemory.append(weights[:])   

def showResults():
    
    global XAxisIterations, YAxisMisClassed, ZWeightMemory
    
    minValue = min(YAxisMisClassed)
    minIndex = YAxisMisClassed.index( minValue )
    
    print "Equation of plane with most classifications ( ", minValue,'/ 2000 ) :'
    print ZWeightMemory[minIndex][0],"x + ",ZWeightMemory[minIndex][1],"y + ",ZWeightMemory[minIndex][2],"z + ",ZWeightMemory[minIndex][3]," = 0" 
    
    plt.plot( XAxisIterations, YAxisMisClassed,'ro')  
    plt.xlabel('No of Iterations')
    plt.ylabel('No of misclassified points')
    plt.show()    

################################################################################################################################    

print 'Pocket Algorithm:'
readFile()
calculateHyperPlane()
showResults()


#validate()