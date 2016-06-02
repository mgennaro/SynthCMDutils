import matplotlib.pyplot as plt
import numpy as np
from numba import jit

class GeneralRandom:
  """This class enables us to generate random numbers with an arbitrary 
  distribution."""
  
  def __init__(self, x, p, Nrl):
    """Initialize the lookup table (with default values if necessary)
    Inputs:
    x = random number values
    p = probability density profile at that point
    Nrl = number of reverse look up values between 0 and 1"""  
    self.set_pdf(x, p, Nrl)
  @jit
  def set_pdf(self, x, p, Nrl):
    """Generate the lookup tables. 
    x is the value of the random variate
    pdf is its probability density
    cdf is the cumulative pdf
    inversecdf is the inverse look up table
    
    """
    
    self.x = x
    self.pdf = p/p.sum() #normalize it
    self.cdf = self.pdf.cumsum()
    self.inversecdfbins = Nrl
    self.Nrl = Nrl
    y = np.arange(Nrl)/float(Nrl)
    delta = 1.0/Nrl
    self.inversecdf = np.zeros(Nrl)    
    self.inversecdf[0] = self.x[0]
    cdf_idx = 0
    for n in range(1,self.inversecdfbins):
      while self.cdf[cdf_idx] < y[n] and cdf_idx < Nrl:
        cdf_idx += 1
      self.inversecdf[n] = self.x[cdf_idx-1] + (self.x[cdf_idx] - self.x[cdf_idx-1]) * (y[n] - self.cdf[cdf_idx-1])/(self.cdf[cdf_idx] - self.cdf[cdf_idx-1]) 
      if cdf_idx >= Nrl:
        break
    self.delta_inversecdf = np.concatenate((np.diff(self.inversecdf), [0]))

  @jit
  def random(self, N = 1):
    """Give us N random numbers with the requested distribution"""

    idx_f = np.random.uniform(size = N, high = self.Nrl-1)
    idx = np.array([idx_f],'i')
    y = self.inversecdf[idx] + (idx_f - idx)*self.delta_inversecdf[idx]

    return y.T
  
  def plot_pdf(self):
    plt.plot(self.x, self.pdf)
    
  def self_test(self, N = 1000):
    plt.figure()
    #The cdf
    plt.subplot(2,2,1)
    plt.plot(self.x, self.cdf)
    #The inverse cdf
    plt.subplot(2,2,2)
    y = np.arange(self.Nrl)/float(self.Nrl)
    plt.plot(y, self.inversecdf)
    
    #The actual generated numbers
    plt.subplot(2,2,3)
    y = self.random(N)
    plt.hist(y, bins = 50,
           range = (self.x.min(), self.x.max()), 
           normed = True)
      #    plt.plot(self.x, self.pdf/self.pdf.max())
    plt.plot(self.x-(0.5*(self.x[1]-self.x[0])), self.pdf/np.trapz(self.pdf,self.x))