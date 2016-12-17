'''
Created on Oct 14, 2016

@author: anand
'''

import sys
import math
import pandas as pd

userIndex = []
movieIndex = []
utilityMatrix = []
cmdlineUser=''; cmdlineMovie=''; cmdlineK=0
    
def readCommandLine():
    
    global cmdlineUser, cmdlineMovie, cmdlineK
    
    try:
        fHandle = open('ratings-dataset.tsv')     #sys.argv[1]) #
    except:
        print 'File cannot be opened:'
        exit()   
    
    inputDataList = []
    for line in fHandle:
        listOfRow =  line.split('\t')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        inputDataList.append(listOfRow)
    
    cmdlineUser  = 'Kluver'       # sys.argv[2]
    cmdlineMovie = 'The Fugitive' # sys.argv[3]
    try:
        cmdlineK = 10 #int(sys.argv[4])
    except:
        print 'Invalid value of K provided'; exit()    
        
    return inputDataList

def createUtilityMatrix(inputDataList):
    
    global userIndex, movieIndex, utilityMatrix, cmdlineUser, cmdlineMovie, cmdlineK
    
    # iterate through input data 1st to know the dimension of matrix that we will create
    for fileDataRow in inputDataList:
        userIndex.append(fileDataRow[0])
        movieIndex.append(fileDataRow[2])
    
    userIndex  = sorted( list(set(userIndex)))
    movieIndex = sorted( list(set(movieIndex)))
    
    #basic validation before creation
    if (cmdlineUser not in userIndex):
        print 'Command line User does not exist in File'; exit()
    if (cmdlineMovie not in movieIndex):
        print 'Command line Movie does not exist in File'; exit()
    if (cmdlineK> len(userIndex) or cmdlineK<=0):
        print 'Invalid value of K provided'; exit()       
    
    # Create Matrix
    utilityMatrix = pd.DataFrame( index=userIndex, columns=movieIndex)
    #utilityMatrix.to_excel('utilityMatrix.xlsx','sheet1')
    
    for fileDataRow in inputDataList:
        utilityMatrix.at[fileDataRow[0],fileDataRow[2]] = float( fileDataRow[1] )
    
    return utilityMatrix

    
def pearson_correlation(user1, user2, item) :
    
    global movieIndex, utilityMatrix
    
    avgUser1Rating=0 
    avgUser2Rating=0
    countCoRated = 0
    hasNeighborRatedItem = True
       
    for movieName in movieIndex:
        u1Rating = utilityMatrix.at[user1, movieName]
        u2Rating = utilityMatrix.at[user2, movieName]
        
        #if ( not (pd.isnull(u1Rating) or pd.isnull(u2Rating) )): 
        if (pd.isnull(u2Rating)): 
            if (movieName == item):
                # set flag, if this neighbor rated 'Item' passed to this method
                hasNeighborRatedItem = False
        else: 
            # for average ratings, use co-rated items from user1,user2
            if (not pd.isnull(u1Rating)):
                avgUser1Rating+=u1Rating  
                avgUser2Rating+=u2Rating
                countCoRated+=1  
           
    avgUser1Rating = avgUser1Rating/countCoRated
    avgUser2Rating = avgUser2Rating/countCoRated
        
    user1DenoSquareSum = 0
    user2DenoSquareSum = 0
    user1user2DotProduct = 0
 
    # formula
    for movieName in movieIndex:
        
        u1Rating = utilityMatrix.at[user1, movieName]
        u2Rating = utilityMatrix.at[user2, movieName]
        
        if ( not pd.isnull(u1Rating)  and not pd.isnull(u2Rating) ):    # summation only over co-related items    
            user1user2DotProduct += (u1Rating - avgUser1Rating) * (u2Rating - avgUser2Rating) # = dot product
            user1DenoSquareSum   += (u1Rating - avgUser1Rating) * (u1Rating - avgUser1Rating) # = square in deno
            user2DenoSquareSum   += (u2Rating - avgUser2Rating) * (u2Rating - avgUser2Rating) # = square in deno
                    
    pearsonCoefficient = user1user2DotProduct/ ( math.sqrt( user1DenoSquareSum) * math.sqrt( user2DenoSquareSum) )        
        
    return ( pearsonCoefficient,hasNeighborRatedItem   )
    

def K_nearest_neighbors(user1, k, item) :
    
    global userIndex
    nearestKNeighbours = []
    
    for otherUser in userIndex:
        if otherUser != user1:
            (pearsonCoff, neighborRatedTheItem )=  pearson_correlation(user1,otherUser, item )
            if (neighborRatedTheItem):
                nearestKNeighbours.append( [otherUser, pearsonCoff ] ) # call method
            
    nearestKNeighbours = sorted(nearestKNeighbours, key = lambda x : (x[0]) ,reverse = False)  
    nearestKNeighbours = sorted(nearestKNeighbours, key = lambda x : (x[1]) ,reverse = True )
    
    if len(nearestKNeighbours) > k: nearestKNeighbours = nearestKNeighbours[:k]  
    
    for row in nearestKNeighbours:
        print row[0],' ',row[1]
    return nearestKNeighbours
    
def Predict(user1, item, k_nearest_neighbors) :
    
    
    avgRatingUser1 = 0
    countRatingUser1 = 0
    avgRatingNeighbors = {}
    
    for movieName in movieIndex:
        # For average, do not use any rating from the movie column that we are about to calculate ratings for
        if (movieName != item ): 
        
            #get sum of ratings for user1 (active user) : Ra uses ALL
            if ( not pd.isnull(utilityMatrix.at[ user1, movieName])):
                avgRatingUser1 += utilityMatrix.at[ user1, movieName]
                countRatingUser1 += 1
                
            # get sum of ratings for K other neighbors  : Ru uses co-rated    
            for neighborTuple in k_nearest_neighbors:
                
                avgRatingNeighbors.setdefault(neighborTuple[0], [0,0] ) # { userName, [sumofRatings, countofRatings] }
                Ra = utilityMatrix.at[user1, movieName]
                Ru = utilityMatrix.at[neighborTuple[0], movieName]
                if ( not pd.isnull(Ra) and not pd.isnull(Ru) ):
                    sumRating   = avgRatingNeighbors[neighborTuple[0]] [0] + Ru
                    countRating = avgRatingNeighbors[neighborTuple[0]] [1] + 1
                    avgRatingNeighbors[neighborTuple[0]] = [sumRating, countRating]
                    
    
    #calculate average ratings
    if (countRatingUser1!=0):avgRatingUser1 /= countRatingUser1  
    for key, valueTuple in avgRatingNeighbors.iteritems():
        avgRatingNeighbors[key] = valueTuple[0]/valueTuple[1]  #{ userName, averageRatings }
                      
    
    # proceed on using equation                    
    predictionNum = 0
    predictionDen = 0            
    for neighborTuple in k_nearest_neighbors:  # [neighbor, PearsonCoff ]
        neighborRating = utilityMatrix.at[ neighborTuple[0], item]
        #if ( not pd.isnull(neighborRating)):
        predictionNum += ( neighborRating - avgRatingNeighbors[neighborTuple[0]] ) * neighborTuple[1]  
        predictionDen += abs( neighborTuple[1] ) 
    
    if (predictionDen!=0): utilityMatrix.at[user1,item] = avgRatingUser1 + (predictionNum / predictionDen )     
    print utilityMatrix.at[user1,item]
    
    
########################################################################################################

inputDataList = readCommandLine()
utilityMatrix = createUtilityMatrix(inputDataList)
k_nearest_neighbors = K_nearest_neighbors(cmdlineUser,cmdlineK, cmdlineMovie )
Predict(cmdlineUser, cmdlineMovie, k_nearest_neighbors)

    