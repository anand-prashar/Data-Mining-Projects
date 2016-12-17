'''
Created on Oct 04, 2016

@author: anand
'''

import sys
import random
import itertools

origSupportValue = 0
adjSupportValue = 0
fileName = ''
fullBasketList = []
sampledBasketList = []
negativeBorderItems={}


def readCommandLine():
    if len(sys.argv) != 3:
        print 'Invalid number of arguments passed'
        exit()
     
    global fileName, origSupportValue
    fileName = sys.argv[1]
    origSupportValue = int( sys.argv[2] )
   
   
def readFile():
    
    try:
        fHandle = open(fileName)
    except:
        print 'File cannot be opened:', fileName
        exit()

    for line in fHandle:
        listOfRow =  line.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        listOfRow.sort()
        fullBasketList.append(listOfRow )
    #fullBasketList.sort() 
    
 
# creates Sampled Basket List; and adjusts support value too
def adjustParametersForAlgo( samplingFraction ):
    
    global sampledBasketList, adjSupportValue
    
    # get random id to mark as 'random sample'
    totalPopulationSize =  len(fullBasketList)   
    randomBasketIdList = random.sample( range(totalPopulationSize) , int(totalPopulationSize* samplingFraction)  )    
 
    for randomBasketId in randomBasketIdList:
        sampledBasketList.append( fullBasketList[randomBasketId] )
    
    # intuitively, reduce the support even little lower - to minimize False Negatives
    adjSupportValue = int(origSupportValue * samplingFraction * 0.9)    
        
        
def setFrequentItemsets(itemSize, backupList = []):
    
    itemDictionary = {}
    frequentItemSets = []
    
    #look for frequent items in sample list
    for basket in sampledBasketList:
        for itemSet in itertools.combinations(basket,itemSize):
            itemDictionary.setdefault(itemSet,0)
            itemDictionary[itemSet] = itemDictionary[itemSet] + 1
    
    if itemSize == 1:
        for currentCandidate,value in itemDictionary.viewitems():
            if value>=adjSupportValue:
                frequentItemSets.append( list(currentCandidate) )
            else:
                negativeBorderItems.update({currentCandidate: value})
        frequentItemSets.sort(cmp=None, key=None, reverse=False)        
        return frequentItemSets   # exit        

    # for sizes > 1
    for currentCandidate,value in itemDictionary.viewitems():
        if value>=adjSupportValue:
            frequentItemSets.append( list(currentCandidate) )
        else: 
            allSubsetsAreFrequent = True   
            for subsetOfcurrentCandidate in itertools.combinations(currentCandidate, itemSize-1):
                if list(subsetOfcurrentCandidate) not in backupList:
                    allSubsetsAreFrequent = False
                    break
            
            if allSubsetsAreFrequent:
                negativeBorderItems.update({currentCandidate:value})       
    frequentItemSets.sort(cmp=None, key=None, reverse=False)              
    return frequentItemSets

def checkFalseNegativesAndPositives(negativeBorderItems, maxRunCount):
    
    # for false positive
    falsePositiveCheckDict = {}
    for freqSetsOfXSize in frequentItemSets:
        for freqSet in freqSetsOfXSize:
            falsePositiveCheckDict.setdefault(tuple(freqSet),0)
        
    # for false negative
    for key in negativeBorderItems.viewkeys():
        negativeBorderItems[key] = 0 #reset values
   
    for basket in fullBasketList:
        #while maxRunCount > 0:  
        for pickSize in range(1,maxRunCount):              
            for itemSet in itertools.combinations(basket, pickSize):
                # for false Negatives
                if itemSet in negativeBorderItems:
                    negativeBorderItems[itemSet]+=1
                    
                # for false Positives   
                if itemSet in falsePositiveCheckDict:
                    falsePositiveCheckDict[itemSet]+=1 
                 
            #maxRunCount = maxRunCount - 1
        
    # remove false positives from Frequent List
    for key,value in falsePositiveCheckDict.viewitems():
        if value <= origSupportValue:
            for listOfXSize in frequentItemSets:
                if list(key) in listOfXSize : 
                    listOfXSize.remove(list(key)); break    
        
    # If any of the item in negativeBorder has value >= Original threshold, send back- need to Rerun
    for key,value in negativeBorderItems.viewitems():
        if value >= origSupportValue:
            return True         
    return False
    
########################################### DRIVER PROGRAM ############################################
#######################################################################################################


# initial declaration-
samplingFraction = 0.4
maxAttemptsforLoop = 1
negativeBorderIncomplete  =True
iterationCount = 0
itemSize = 1
frequentItemSets = []
backupList = []


# Logic -  

readCommandLine()

readFile()  

while negativeBorderIncomplete and maxAttemptsforLoop <= 30 :

    adjustParametersForAlgo(samplingFraction)
 
    itemSize = 1
    while backupList!=[] or itemSize == 1:
        tempSet = setFrequentItemsets(itemSize, backupList)
        if tempSet!=[]: frequentItemSets.append( tempSet )
        backupList = tempSet[:] # make a copy for lookup for higher order later
        itemSize+=1
    
    negativeBorderIncomplete = checkFalseNegativesAndPositives(negativeBorderItems, itemSize-1)
    if negativeBorderIncomplete: 
        #print 'Re-sampling Attempt ', maxAttemptsforLoop, '/ 30'; print
        frequentItemSets=[]
        sampledBasketList=[]
        negativeBorderItems={}
    maxAttemptsforLoop+=1
    

# Output -

if maxAttemptsforLoop > 30:
    print 'All heuristics attempts failed on negative Border removal'
    exit()

# after getting outside of loop    
print maxAttemptsforLoop-1
print samplingFraction;

for itemSet in frequentItemSets:
    if itemSet != [] : print itemSet
