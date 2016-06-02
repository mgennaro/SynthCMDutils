import numpy as np
import scipy.stats as ss
from . import ParlistException
from numba import jit

@jit
def getbinq(sampsize,distr_name,parlist):

    '''
       Extract a number "sampsize" of masses
       from a distribution selected among several available.
       When a certain "distr_name" is passed, the paramters
       for that distribution are passed in the list "parlist"
       
    '''

    #Uniform Distribution
    if (distr_name == 'uniform'):
        if (len(parlist) != 2): raise ParlistException.PE(
                "The uniform distribution parlist must have 2 parameters: min_range and max_range",parlist)
        if (parlist[1] <= parlist[0]): raise ParlistException.PE(
                "parlist[0] must be <= parlist[1]",parlist)
        return np.random.uniform(low=parlist[0],high=parlist[1],size=sampsize)

    elif (distr_name == 'Trunc_normal'):
        if (len(parlist) != 4): raise ParlistException.PE(
                "The Truncated normal distribution parlist must have 4 elements: min_range, max_range, mu and sigma",parlist)

        cdfh = ss.norm.cdf(parlist[1],loc=parlist[2],scale=parlist[3])
        cdfl = ss.norm.cdf(parlist[0],loc=parlist[2],scale=parlist[3])
        nrm  = cdfh - cdfl
        #sample using the inverse cdf
        yr = np.random.uniform(low=0,high=1.,size=sampsize)*(nrm)+cdfl
        return ss.norm.ppf(yr,loc=parlist[2],scale=parlist[3])

    else:
        raise ParlistException.PE("This distribution is not supported:",distr_name)  
        
