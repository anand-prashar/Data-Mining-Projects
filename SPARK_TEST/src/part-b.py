from pyspark import SparkContext

# change parameters for other tests
city = 'los angeles'
seller = 'john'

def keyGen(fileLine, fileSource):
    
    tempList = str(fileLine).split(',')   
    if fileSource == 'person':
        return (tempList[0], tempList[2])
    return (tempList[0], tempList[1])

#########################################################################################

sc = SparkContext(appName='inf551_part_b')

personRDD   = sc.textFile('person.txt').map(lambda fileLine : keyGen(fileLine, 'person')).filter(lambda keyTuple: keyTuple[1]== city)
    
purchaseRDD = sc.textFile('purchase.txt').map(lambda fileLine : keyGen(fileLine, 'purchase')).filter(lambda x: x[1]==seller)

resultList = personRDD.join(purchaseRDD).distinct().sortByKey().collect()

for line in resultList:
    print line[0]