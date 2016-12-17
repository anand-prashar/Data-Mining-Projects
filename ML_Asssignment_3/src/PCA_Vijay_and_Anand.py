'''
Created on Oct 5, 2016

@author: anand
'''

import numpy as np
import numpy.linalg as LA # numpy's linear algebra package
from numpy import double



def readFile():
    
    try:
        fHandle = open('pca-data.txt')
    except:
        #print 'Data fetch error'
        exit()
    
    dataList = []    
    for line in fHandle:
        
        listOfRow =  line.split('\t')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        dataPoint = np.matrix( [ [ double( listOfRow[0])] , 
                                 [ double( listOfRow[1])] , 
                                 [ double( listOfRow[2])] ] )   # each point is 3X1 vector
        dataList.append( dataPoint )
        
    return dataList

    
def normalizeVectors(dataList):
     
    meanVector = np.matrix([ [0.0], 
                             [0.0], 
                             [0.0] ])  # need as Nx1 matrix
    #print 'shape:', meanVector.shape
    for dataVector in dataList:
        meanVector += dataVector
    meanVector =  meanVector/len(dataList)
    
    for dataVector in dataList:
        dataVector -= meanVector
    
    #print meanVector  
    return dataList 
    

def findCovariance(dataList):
    
    # each data point is a 3x1 matrix. Its transpose will be 1x3 matrix. So we need 3x3 matrix to hold product and coVariance
    transposeSum = np.matrix( [ [ double( 0.0) , double( 0.0) , double( 0.0) ],
                                [ double( 0.0) , double( 0.0) , double( 0.0) ],
                                [ double( 0.0) , double( 0.0) , double( 0.0) ]  
                            ] )
    
    for dataVector in dataList:
        transposeProduct = dataVector * (dataVector.getT()) # (matrix X matrix transpose)
        transposeSum+= transposeProduct
    
    #print transposeSum
    #print 'shape:', transposeSum.shape
    sigma = transposeSum / len(dataList)
    
    return sigma    
        
def calcEigenValuesNVectors(coVariance):
    eVal, eVect = LA.eig(coVariance)
    #print 'EIGEN VALUE AND VECTOR = \n',eVal
    #print '\n\n', eVect
    #u, s, v = LA.linalg.svd(coVariance, full_matrices = True)
    ##print '\n\nSVD: U S V-\n', u, '\n',s,'\n',v
    print 'Eigen Values = \n', eVal
    print '\nEigen Vector = \n',eVect
    return eVect

def calcDimensionRedction(eigenVector, dataList, K):
    
    
    # Need to clip 1st K columns-- to create zMatrix :
    # 1st, transpose the matrix.. so that we can easily clip from a array[:K] 
    # after clipping, re-transpose to place it back in order
    UReduceMatrix = eigenVector.getT()  
    UReduceMatrix = UReduceMatrix[:K]
    UReduceMatrix = UReduceMatrix.getT()
    print '\nDirections of 2 principal components: \n',UReduceMatrix
    
    
    
    writeToFile = open('PCA_Output_Anand_and_Vijay.txt', 'w')
    UReduceMatrix = UReduceMatrix.getT()  # no need to do transpose every time inside loop
    for dataPoint in dataList:
        strResultLine = UReduceMatrix*dataPoint
        strResultLine = str(strResultLine[0][0])[3:-2]+',\t'+str(strResultLine[1][0])[3:-2]+'\n'
        
        writeToFile.write(strResultLine)
    writeToFile.close()
    print '\n\nDimenionality of all points reduced to 2D.\nOutput file- PCA_Output_Anand_and_Vijay.txt'

        
dataList = readFile()
dataList = normalizeVectors(dataList )  
coVariance = findCovariance(dataList)
eigenVector = calcEigenValuesNVectors(coVariance)
result = calcDimensionRedction(eigenVector, dataList, K=2)
