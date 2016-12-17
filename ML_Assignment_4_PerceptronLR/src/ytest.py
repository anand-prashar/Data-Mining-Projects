'''
Created on Oct 13, 2016

@author: vijay
'''
import numpy as np
data_points = []
data_outcome = []

def readData():
    global data_outcome, data_points
    data_point = []
    with open("./linear-regression.txt") as fileReader:
        data_file = fileReader.read().splitlines()
    for d in data_file:
        data_point = d.split(",") 
        data_points.append([float(1),float(data_point[0]),float(data_point[1])]) # X[0] will be 1
        data_outcome.append(float(data_point[2]))
    
def findNewDelta():

    pointsMatrix= np.matrix(data_points).T
    pointsMatrixT = pointsMatrix.T
    #print "Matrix, Matrix Transpose",pointsMatrix.shape, pointsMatrixT.shape
    matrixProductInv = np.matmul(pointsMatrix,pointsMatrixT).I
    #print "Inv", matrixProductInv.shape
    outcomeMatrix = np.matrix(data_outcome).T
    #print "outcome", outcomeMatrix.shape
    allProduct = np.matmul(matrixProductInv,np.matmul(pointsMatrix,outcomeMatrix))
    print "Weight vector for current data points\n[W0            W1                W2]\n", allProduct.T

readData()
findNewDelta()