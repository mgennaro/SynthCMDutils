import numpy as np
import scipy.stats as ss
from . import ParlistException
from numba import jit

@jit
def getage(sampsize,distr_name,parlist):

    '''
       Extract a number "sampsize" of ages
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

    #Truncated exponential
    elif(distr_name == 'Trunc_exp'):
        if (len(parlist) != 3): raise ParlistException.PE(
                "The Trunc_exp distribution parlist must have 3 parameters: min_range, max_range, lambda",parlist)
        if (parlist[2] >= 0):
            rnd_cdf = np.random.uniform(ss.expon.cdf(x=parlist[0], scale=parlist[2]),
                                        ss.expon.cdf(x=parlist[1], scale=parlist[2]),size=sampsize)
            return ss.expon.ppf(q=rnd_cdf, scale=parlist[2])
        else:
            rnd_cdf = np.random.uniform(ss.expon.cdf(x=parlist[0], scale=-1.*parlist[2]),
                                        ss.expon.cdf(x=parlist[1], scale=-1.*parlist[2]),size=sampsize)
            
            draws = ss.expon.ppf(q=rnd_cdf, scale=-1.*parlist[2])
            return -1.*draws+parlist[0]+parlist[1]

    #Bursts
    elif(distr_name == 'Bursts'):
        pk = []
        for idx,burst in enumerate(parlist):
          if (len(burst) != 3): raise ParlistException.PE(
                  "Each burst in the Bursts distribution must have 3 parameters: min_range, max_range, intensity ",[idx,burst])
          else:
              pk.append(burst[2])

        xk = np.arange(len(pk))
        pkv = np.asarray(pk)
        pkv = pkv/np.sum(pkv)
        custm = ss.rv_discrete(name='custm', values=(xk, pkv))
        rndm_idx = custm.rvs(size=sampsize)
        return parlist[rndm_idx][0]+(parlist[rndm_idx][1]-parlist[rndm_idx][0])*np.random.uniform(low=0., high=1.,size=sampsize)

    else:
        raise ParlistException.PE("This distribution is not supported:",distr_name)  
   
