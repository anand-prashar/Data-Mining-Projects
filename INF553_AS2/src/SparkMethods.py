'''
Created on Oct 7, 2016

@author: anand
'''

from pyspark import SparkConf, SparkContext
import re

def splitFn(rddStringRow):
    splitList = re.split('[\"\'], [\"\']', rddStringRow )
    rowTuple = (splitList[0].strip()[2:],splitList[1].strip()[:-2])
    return rowTuple

def createADPairs(threeLayerTuple):
    actorDirectorTupleCount = ((threeLayerTuple[1][1],threeLayerTuple[1][0]),1)
    return actorDirectorTupleCount

def unicodeToUTF8(tupleKV):
    actress  = tupleKV[0][0].encode('utf8')
    director = tupleKV[0][1].encode('utf8')
    
    return ((actress,director), tupleKV[1] )

#get spark configuration, set context here, and give it a name
SparkConf = SparkConf().setAppName('Self Test').setMaster('local[1]')
sc = SparkContext(conf = SparkConf)

#readTextFile
actorFileRDD = sc.textFile('actress') # , minPartitions
dctorFileRDD = sc.textFile('director') # , minPartitions

movieActorPair = actorFileRDD.map(lambda x: splitFn(x), True)
movieDctorPair = dctorFileRDD.map(lambda x: splitFn(x), True)


#for rowTuple in movieDctorPair.keys().collect():
#    print rowTuple
#print '\n\n-------------------------------------------------------------------------\n'
#for rowTuple in movieDctorPair.keys().collect():
#    print rowTuple

joinOnMovieRDD = movieDctorPair.join(movieActorPair)#.collect()
ADtupleCountRDD = joinOnMovieRDD.map(lambda x:createADPairs(x))

#for r in ADtupleCountRDD.collect():
#    print r[0] ,'---------',r[1]

Support = 3
rawResultRDD = ADtupleCountRDD.reduceByKey( lambda x,y: x+y )  
#rawResultRDD = rawResultRDD.map( lambda tpl : reverseXY(tpl[0],tpl[1] ) )
rawResultRDD = rawResultRDD.filter(lambda x: x[1] >= Support )
rawResultRDD = rawResultRDD.map(lambda x: unicodeToUTF8(x) )
resultRDD = rawResultRDD.sortBy(lambda x: x[1])#.map(lambda revTpl : reverseXY( revTpl[0], revTpl[1]))

resultRDD =   resultRDD.repartition(1)
#resultRDD = rawResultRDD.sortByKey().map(lambda revTpl : reverseXY( revTpl[0], revTpl[1]))


#finalResultRDD = rawResultRDD.filter(lambda x: x[1]>4)


print '--------------------------------------'
for r in resultRDD.collect():
    print r[0] ,'---------',r[1]
try:
    resultRDD.saveAsTextFile('AP_Spark_output')   
    print 'Process completed successfully !'
except:
    print 'Process success. Please delete existing folder with same name to see output !'      
    
#actorDirectorPairRDD = joinOnMovieRDD.map( lambda x : createADPairs(x)) 
    
#joinOnMovieRDD = actorFileRDD.join( dctorFileRDD )
#movieActorPair3 = joinOnMovieRDD.values() #keyBy(f) 
#for result in movieActorPair3.collect():
#    print 'VALUE =', result

#print 'RDD=',joinOnMovieRDD

#movieActorPair2 = movieActorPair.keys() #keyBy(f) 
#for result in movieActorPair2.collect():
#    print 'KEY =', result
#movieActorPair3 = movieActorPair.values() #keyBy(f) 
#for result in movieActorPair3.collect():
#    print 'VALUE =', result
    
#x = sc.parallelize([("a", 1), ("b", 4)])
#y = sc.parallelize([("a", 2), ("a", 3)])
#another = sorted(x.join(y).collect()) 

#for t in another:
#    print t 
    
#print textFileRDD.count()
#print fileRDD.getNumPartitions()
#print fileRDD.
