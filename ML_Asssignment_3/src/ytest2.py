'''
Created on Oct 5, 2016

@author: anand
'''

import re
s1 = '(\'Night of the Demons (2009)  (uncredited)\', \'\"Steff\", Stefanie Oxmann Mcgaha\')'
s2 = '(\'\"Supernatural\" (2005) {99 Problems (#5.17)}  (uncredited)\', \"\'67 Impala")'

print s1.split('\', \'')[0]
print s2.split('\', \"')[0]

result = re.split('\', [\"\']', s2)
print result[0]
result = re.split('\', [\"\']', s1)
print result[0]