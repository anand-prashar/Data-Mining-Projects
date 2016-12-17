
import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

try:
    fHandle = open("input.txt")
except:
    print 'File cannot be opened:'
    exit()   

sum = 0    
for line in fHandle:
    listOfRow =  line.split(',')
    n = len(listOfRow)
    if n>=3:
        sum+=ncr(n, 3)
print sum    