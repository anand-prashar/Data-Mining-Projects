'''
Created on Sep 28, 2016

@author: anand
'''

import gc
import sys
import itertools

supportValue = 0
bucketSize = 0
fname = ''
basketList = []


def readCommandLine():
    if len(sys.argv) != 4:
        print 'Invalid number of arguments passed'
        exit()
     
    global fname, supportValue, bucketSize
    fname = sys.argv[1]
    supportValue = int( sys.argv[2] )
    bucketSize   = int( sys.argv[3] )  
         
    
def readFile():
    
    try:
        fHandle = open(fname)
    except:
        print 'File cannot be opened:', fname
        exit()   
    
    global basketList
    for line in fHandle:
        listOfRow =  line.split(',')
        listOfRow[-1] = listOfRow[-1].split('\n')[0]
        listOfRow.sort()
        basketList.append(listOfRow)


def setHashTable1( itemSize):
    hashTable1Dict={}
    
    for basket in basketList:        
        for combination in itertools.combinations( basket, itemSize):
            key = 0
            for itemSet in combination:
                for item in itemSet:
                    key = key + ord(item)
                    
            key = key%bucketSize
            hashTable1Dict.setdefault(key,0)
            hashTable1Dict[ key ]+=1    

    return hashTable1Dict
    
def setHashTable2( itemSize):
    hashTable2Dict={}
    
    for basket in basketList:
        
        for combination in itertools.combinations( basket, itemSize):
            key = 0
            for itemSet in combination:
                #create hash using ASCII
                
                counter = 997
                for item in itemSet:
                    key = (ord(item)* counter)+key
                    counter=counter-1
                    
            key = key%bucketSize
            hashTable2Dict.setdefault(key,0)
            hashTable2Dict[key]+=1

    return hashTable2Dict


def setFreqItemsets(itemSize,  bitMap1=None, bitMap2=None, backupList=None):
    freqItemSet = []
    itemDictionary={}
    
    if itemSize == 1:
        for basket in basketList:
        
            for item in basket:
                if itemDictionary.get(item) is not None:
                    itemDictionary[item] = itemDictionary[item]+1
                else:
                    itemDictionary[item] = 1    
    else:
        
        for basket in basketList:
            
            #create current-size pairs, then check for its candidature among last-size frequent pairs
            for currentCandidate in itertools.combinations( basket, itemSize):

                allPossibleSubsets=[]
                commonItemset=[]
                for subsetOfcurrentCandidate in itertools.combinations(currentCandidate, itemSize-1):
                    #totalComb = totalComb+1
                    allPossibleSubsets.append(list(subsetOfcurrentCandidate) )

                
                commonItemset = filter(lambda item: item in allPossibleSubsets, backupList)
                    
                if(len(allPossibleSubsets) == len(commonItemset)):
                    # candidate exists in previous Frequent Set: now lookup in both bitmaps to confirm
                    if ( checkBitMap1(bitMap1, subsetOfcurrentCandidate) == True and checkBitMap2(bitMap2, subsetOfcurrentCandidate) == True ):
                        #add to dictionary 
                        itemDictionary.setdefault(currentCandidate, 0)    
                        itemDictionary[currentCandidate] = itemDictionary[currentCandidate] + 1
                    
    # filter        
    for key, count in itemDictionary.iteritems():
        if count>=supportValue:
            freqItemSet.append(list(key))
               
    freqItemSet.sort(cmp=None, key=None, reverse=False)                

    return freqItemSet        

    
def setBitMap(hashTable_any):
    global supportValue
    bitDictionary = {} 
    
    for htKey, value in hashTable_any.iteritems():
        if value >= supportValue:
            bitDictionary.setdefault(htKey, True)
        #don't need to add any False entry    
            
    return bitDictionary


def checkBitMap1(bitMap1, Candidate):
    genHash = 0
    
    for subsets in Candidate:
        genHash = ord(subsets) + genHash
        
    if genHash%bucketSize in bitMap1:
        return True
    else:
        return False      
        
def checkBitMap2(bitMap2, Candidate):
    genHash = 0
    counter = 997
    
    for subsets in Candidate:
        genHash = (ord(subsets)* counter)+genHash
        counter=counter+1
    
    if genHash%bucketSize in bitMap2:
        return True
    else:
        return False      
    
        
########################################### DRIVER PROGRAM ############################################
#######################################################################################################
   
     
readCommandLine()   
readFile() 

# set initial step
# Null-set is a subset of every set of size 1 - so just look if each set's support > S
freqItemSet  = setFreqItemsets(1)
print freqItemSet,'\n'


itemSize = 2    
while ( freqItemSet != []):
    
    
    
    # create hash tables
    hashTable1 = setHashTable1(itemSize)
    hashTable2 = setHashTable2(itemSize)
    
    # create bitmaps from hashtable
    bitMap1 = setBitMap(hashTable1)
    bitMap2 = setBitMap(hashTable2)
    
    
    backupList = freqItemSet[:] #make a copy for lookup later
    freqItemSet = setFreqItemsets(itemSize, bitMap1, bitMap2, backupList)
    itemSize = itemSize + 1
    
    if freqItemSet  != []:
        print hashTable1,'\n', hashTable2,'\n',freqItemSet,'\n'
    
    #force release memory of hashtable
    hashTable1 = None
    hashTable2 = None
    gc.collect()
    
    
