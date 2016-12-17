from pyspark import SparkContext

def keyGen(fileLine):
    
    tempList = str(fileLine).split(',')
    return (tempList[3], tempList[1])

def getSumAndCount(tuple1, tuple2):
    return (float(tuple1[0])+ float(tuple2[0]), tuple1[1]+tuple2[1]) #(price+price, count+1 )

#########################################################################################

sc = SparkContext(appName='inf551_part_e')

productRDD = sc.textFile('product.txt').map( lambda fileLine : keyGen(fileLine))

sum_count_RDD = productRDD.mapValues(lambda price: (price, 1)).reduceByKey(lambda tuple1,tuple2: getSumAndCount(tuple1, tuple2) )

averageRDD = sum_count_RDD.mapValues(lambda priceCountTuple: float(priceCountTuple[0]) / priceCountTuple[1]) 
averageRDD = averageRDD.sortByKey()

for result in averageRDD.collect():
    print result[0],', ',result[1]