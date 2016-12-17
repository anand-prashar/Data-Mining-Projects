from pyspark import SparkContext

sellType = 'laptop'
dontSellType = 'cell phone'

def keyGen(fileLine, fileSource):
    
    tempList = str(fileLine).split(',')   
    if fileSource == 'product':
        return (tempList[0], tempList[2])
    return (tempList[3], tempList[1])

def customFilter(productTypeSet, sellType, dontSellType):
    
    if (sellType in productTypeSet) and (dontSellType not in productTypeSet):
        return True
    return False
  
#############################################################################################

sc = SparkContext(appName='inf551_part_d')

# resulting map KeyValue: ( product, productType )
productRDD  = sc.textFile('product.txt').map( lambda  fileLine : keyGen(fileLine,'product'))

# resulting map KeyValue: ( product, seller )
purchaseRDD = sc.textFile('purchase.txt').map( lambda fileLine : keyGen(fileLine,'purchase')) 

#join on product : KeyValue ( product, (seller,productType) )
joinRDD = purchaseRDD.join(productRDD)

#extract (seller,productType) tuples, group in list all productTypes sold by Each Seller
sellerPtypeRDD = joinRDD.map(lambda tuple: (tuple[1][0],tuple[1][1])).groupByKey()

#find Unique product types for each seller
resultRDD = sellerPtypeRDD.map(lambda Seller_PTypeList: ( Seller_PTypeList[0], set(Seller_PTypeList[1]) ) )

#finally, filter : keep those sellers, who sell Laptop but not CellPhone
resultRDD = resultRDD.filter(lambda S_PSet: customFilter(S_PSet[1], sellType, dontSellType) ).sortByKey()

for i in resultRDD.collect():
    print i[0]
