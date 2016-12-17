
from bitarray import bitarray
bitMap = bitarray([False,False,True,False,True])
#bitMap.setAll(False)
#bitMap[2:2] = True
print bitMap
print bitMap[4]

class userDictTuple:
    __key = None
    __value  = False
    def __init__(self, key ):
        self.__key = key
    def _updateValue(self, newBitValue):
        self.value = newBitValue    
    def __str__(self):
        return '['+ str(self.__hashIndex)+' : '+ str(self.__bitValue)+']'  

    
class userBitDictionary:
    
    _userBitDictionary = []
    
    def append(self,key):
        
        if key in self._userBitDictionary:
            raise KeyError('Key already exists')
       # else:
            

#obj = userBitPair(10)
#print obj
#print obj._bitValue

uDict = {}
uDict.setdefault(49,True)
uDict.setdefault(12,False)
#print uDict   

###############################################################################################

myDict = {}
a = ['a','b']
myDict.setdefault(a,11)

print myDict.get('k')
