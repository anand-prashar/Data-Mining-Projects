from pyspark import SparkContext

# change parameters for other tests
city = 'los angeles'

def keyGen(fileLine):
    
    tempList = str(fileLine).split(',')   
    return (tempList[0], tempList[2])

#########################################################################################

sc = SparkContext(appName='inf551_part_a')

personRDD   = sc.textFile('person.txt').map(lambda fileLine : keyGen(fileLine) ).filter(lambda keyTuple: keyTuple[1]== city).sortByKey()

for itr in personRDD.collect():
    print itr[0]