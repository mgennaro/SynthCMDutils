import numpy as np
import scipy.stats as ss
from . import ParlistException
from numba import jit

@jit
def getmass(sampsize,distr_name,parlist):

    '''
       Extract a number "sampsize" of masses
       from a distribution selected among several available.
       When a certain "distr_name" is passed, the paramters
       for that distribution are passed in the list "parlist"
       
    '''

    #Uniform Distribution
    if (distr_name == 'uniform'):
        if (len(parlist) != 2): raise ParlistException.PE("The uniform distribution parlist must have 2 parameters: min_range and max_range",parlist)
        if (parlist[1] <= parlist[0]): raise ParlistException.PE("parlist[0] must be <= parlist[1]",parlist)
        return np.random.uniform(low=parlist[0],high=parlist[1],size=sampsize)

    #Single power law
    if (distr_name == 'SPL'):
        if (len(parlist) != 3): raise ParlistException.PE("The SPL distribution parlist must have 3 parameters: min_range, max_range and slope",parlist) 

        #Convert limits from M to logM
        log_x_Min = np.log(parlist[0])
        log_x_Max = np.log(parlist[1])
        max_p = np.power(parlist[0], 1.0 + parlist[2])

        # Prepare output array
        Y = np.zeros(sampsize)
        i = 0    
        # Fill in array.
        while (i < sampsize):
            # Draw candidate from logM interval.
            logx = np.random.uniform(low=log_x_Min,high=log_x_Max,size=1)
            x    = np.exp(logx)
            # Compute likelihood of candidate from Salpeter SMF.
            likelihood = np.power(x, 1.0 + parlist[2])
            # Accept randomly.
            u = np.random.uniform(low=0.0,high=max_p,size=1)
            if (u < likelihood):
                Y[i] = x
                i+=1
            return Y
    else:
        raise ParlistException.PE("This distribution is not supported:",distr_name)  
        
