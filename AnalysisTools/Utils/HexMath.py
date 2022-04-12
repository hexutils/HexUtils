import numpy as np
import scipy.stats as stats
import uncertainties

def weightedaverage(vals,err):
  # expected input is list of values and weights
  if not vals: raise IOError("Can't take the weighted average of an empty array")
  if all(x == 0 for x in err):
    return sum(vals) / len(vals) , 0
  return sum(vals[i] / err[i]**2 for i in range(len(vals))) / sum(1 / x**2 for x in err), sum(1 / x**2 for x in err) ** -0.5

def kspoissongaussian(mean, size=10000):
  np.random.seed(123456)  #make it deterministic
  return stats.ks_2samp(
    np.random.poisson(mean, size=size),
    np.random.normal(mean, mean**.5, size=size)
  ).statistic

