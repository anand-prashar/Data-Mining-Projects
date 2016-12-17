'''
Created on Oct 14, 2016

@author: anand
'''

import random

theta = 0
learningRate = 0.01
maxNoOfIterations = 0
featureMatrix = []
testSet = []
provop2 = []
providedOP=[]
weights = []

def readFile():
    
    global featureMatrix, providedOP
    
    fileData = open ('classification.txt')
    count = 0
    for fileLine in fileData:
        coordinate = fileLine.split(',')
        if count <=600:
            featureMatrix.append( [ float(coordinate[0]), float(coordinate[1]), float(coordinate[2]) ] )
            providedOP.append(float(coordinate[3]))
        else:
            testSet.append( [ float(coordinate[0]), float(coordinate[1]), float(coordinate[2]) ] )
            provop2.append(float(coordinate[3]))    
#        else:
#            providedOP.append(float(0))    
        count+=1
#        if count == 50: break
            

def calculateHyperPlane():
    
    global featureMatrix, providedOP, weights, maxNoOfIterations
    
    # update random weights
    for i in range(0,3):
        weights.append( float(random.randint(0,1)))
    weights.append(float(1)) # = w0    
    
    globalError = 0
    localError = 0
    firstRun = True
    
    while( globalError!=0.0 or firstRun):
        firstRun = False
        globalError = 0
    
        for index in range( len(featureMatrix)):
            calculatedOP = calculateTrainingOP(theta, weights, featureMatrix[index] )
            localError = providedOP[index] - calculatedOP 
            
            for itr in range( len(weights)-1):
                weights[itr] += learningRate * localError * featureMatrix[index][itr]
            weights[len(weights)-1] += learningRate * localError # new W0
            globalError += localError*localError  
        #print weights
            
             
        maxNoOfIterations+=1
    print 'Iterations taken = ',maxNoOfIterations
        
        
def calculateTrainingOP(theta,weights, featureMatrixRow):
    
    #for( i in rang ):
    weightedSum = featureMatrixRow[0]*weights[0] + featureMatrixRow[1]*weights[1] + featureMatrixRow[2]*weights[2]
    if weightedSum >= theta:
        return 1
    else:
        return -1

def validate(): 
    global featureMatrix, weights, providedOP, theta, testSet, provop2
    
    itr = 0
    for featureMatrixRow in testSet:
        wsum = featureMatrixRow[0]*weights[0] + featureMatrixRow[1]*weights[1] + featureMatrixRow[2]*weights[2] + weights[3]
        if wsum >= theta:
            if 1.0 != provop2[itr]: print 'False'
            
            #print 'calc=',1.0,' givenOP=',providedOP[itr]
        else:
            if -1.0 != provop2[itr]: print 'False'
            #print 'calc=',-1.0,' givenOP=',providedOP[itr]
        itr+=1    
################################################################################################################################    

print 'We have used 1900 data points from file to TRAIN the perceptron.'
print 'We are using last 100 points to TEST the perceptron. Any \'false\' in o/p means wrong classification of some test point'
print 'Please change the value from 1800 -> 2000 in line 26 of code, if you want to use all points to train\n'

readFile()
calculateHyperPlane()

print "Equation of plane : ",weights[0],"x + ",weights[1],"y + ",weights[2],"z + ",weights[3]," = 0"
validate()
