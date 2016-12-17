'''
Created on Oct 7, 2016

@author: anand
'''

from pyspark import SparkConf, SparkContext
import re
#from _sqlite3 import Row

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

joinOnMovieRDD = movieDctorPair.join(movieActorPair)#.collect()

ADtupleCountRDD = joinOnMovieRDD.map(lambda x:createADPairs(x))
temp = ADtupleCountRDD.first()
#print temp

Support = 5
rawResultRDD = ADtupleCountRDD.reduceByKey( lambda x,y: x+y )  
rawResultRDD = rawResultRDD.filter(lambda x: x[1] >= Support )
rawResultRDD = rawResultRDD.map(lambda x: unicodeToUTF8(x) )
resultRDD = rawResultRDD.sortBy(lambda x: x[1])#.map(lambda revTpl : reverseXY( revTpl[0], revTpl[1]))

resultRDD =   resultRDD.repartition(1)  
resultRDD2 = resultRDD.filter( lambda x : 'Aaltonen' in x[0][1] )
for row in resultRDD2.collect():
    print row[0]
try:
    resultRDD.saveAsTextFile('anand_prashar_spark')   
    print 'Process completed successfully !'
except:
    print 'Process success. Please delete existing folder with same name to see output !'    