from pyspark import SparkContext

def keyGen(fileLine, fileSource):
    
    tempList = str(fileLine).split(',')
    if fileSource == 'product':
        return (tempList[3], tempList[0])
    return (tempList[0], tempList[2])

#########################################################################################

sc = SparkContext(appName='inf551_part_c')

productRDD = sc.textFile('product.txt').map( lambda line: keyGen(line, 'product' ))
companyRDD = sc.textFile('company.txt').map( lambda line: keyGen(line, 'company' ))

resultRDD  = companyRDD.join(productRDD).map( lambda mapTuple: (mapTuple[1][1], mapTuple[1][0]) ).sortByKey()


for OPtuple in resultRDD.collect():
    print OPtuple[0],', ',OPtuple[1]