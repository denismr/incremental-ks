from Treap import Treap
from math import log

class IKS:
  def __init__(self):
    self.treap = None
    self.n = [0, 0]

  @staticmethod
  def KSThresholdForPValue(pvalue, N):
    '''Threshold for KS Test given a p-value
    Args:
      pval (float): p-value.
      N (int): the size of the samples.

    Returns:
      Threshold t to compare groups 0 and 1. The null-hypothesis is discarded if KS() > t.
    '''
    ca = (-0.5 * log(pvalue)) ** 0.5
    return ca * (2.0 * N / N ** 2)

  @staticmethod
  def CAForPValue(pvalue):
    '''ca for KS Test given a p-value
    Args:
      pval (float): p-value.

    Returns:
      Threshold the "ca" that can be used to compute a threshold for KS().
    '''
    return (-0.5 * log(pvalue)) ** 0.5
  
  def KS(self):
    '''Kolmogorov-Smirnov statistic. Both groups must have the same number of observations.

    Returns:
      The KS statistic D.
    '''
    assert(self.n[0] == self.n[1])
    N = self.n[0]
    if N == 0:
      return 0
    return max(self.treap.max_value, -self.treap.min_value) / N
  
  def Kuiper(self):
    '''Kuiper statistic. Both groups must have the same number of observations.

    Returns:
      The Kuiper statistic.
    '''
    assert(self.n[0] == self.n[1])
    N = self.n[0]
    if N == 0:
      return 0
    return (self.treap.max_value - self.treap.min_value) / N
  
  def Add(self, obs, group):
    '''Insert new observation into one of the groups.

    Args:
      obs: the value of the obseration. Tip: a tuple (actual value, random value) is recommended when there is overlap between groups or if values are not guaranteed to be mostly unique.
      group (int): which group the observation belongs to. Must be either 0 or 1.
    '''
    group = 0 if group == 2 else group
    assert(group == 0 or group == 1)
    key = (obs, group)

    self.n[group] += 1
    left, left_g, right, val = None, None, None, None

    left, right = Treap.SplitKeepRight(self.treap, key)

    left, left_g = Treap.SplitGreatest(left)
    val = 0 if left_g is None else left_g.value
    left = Treap.Merge(left, left_g)

    right = Treap.Merge(Treap(key, val), right)

    Treap.SumAll(right, 1 if group == 0 else -1)

    self.treap = Treap.Merge(left, right)

  def Remove(self, obs, group):
    '''Remove observation from one of the groups.

    Args:
      obs: the value of the obseration. Must be identical to a previously inserted observation (including the random element of a tuple, if this was the case).
      group (int): which group the observation belongs to. Must be either 0 or 1.
    '''
    group = 0 if group == 2 else group
    assert(group == 0 or group == 1)
    key = (obs, group)

    self.n[group] -= 1

    left, right, right_l = None, None, None

    left, right = Treap.SplitKeepRight(self.treap, key)
    right_l, right = Treap.SplitSmallest(right)

    if right_l is not None and right_l.key == key:
      Treap.SumAll(right, -1 if group == 0 else 1)
    else:
      right = Treap.Merge(right_l, right)
    
    self.treap = Treap.Merge(left, right)
  
  def Test(self, ca = 1.95):
    '''Test whether the reference and sliding window follow the different probability distributions according to KS Test.

    Args:
      ca: ca is a parameter used to calculate the threshold for the Kolmogorov-Smirnov statistic. The default value corresponds to a p-value of 0.001. Use IKS.CAForPValue to obtain an appropriate ca.

    Returns:
      True if we **reject** the null-hypothesis that states that both windows have the same distribution. In other words, we can consider that the windows have now different distributions.
    '''
    ca = ca or 1.95
    n = self.n[0]
    return self.KS() > ca * (2 * n / n ** 2) ** 0.5

IKS.AddObservation = IKS.Add
IKS.RemoveObservation = IKS.Remove

