from sklearn.decomposition import PCA
#from numpy  import array
import numpy as np
from numpy.random import randint
from numpy import float

data = np.array([[ float(5.906262853951832), float(-7.729464584682111), float(9.144944874608196) ], 
                    [ float(-8.640323106971573), float(1.7242604350569888), float(-10.696805187953952)]] )
print data

pca = PCA(n_components=2)
pca.fit(data)
#results = PCA(data)
print'\n', (pca.explained_variance_ratio_) 
print '\n',pca.get_covariance()
#for it in results:
#    print it
#print results