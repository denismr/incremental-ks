from IKS import IKS
from collections import deque
from random import random

class IKSSW:
  def __init__(self, values):
    '''Incremental Kolmogorov-Smirnov Sliding Window. This class assumes that one window is fixed (reference window) and another slides over a stream of data. The reference window can be updated to be the same as the current sliding window.

    Args:
      values: initial values for the reference and sliding windows.
    '''
    self.iks = IKS()
    self.sw = deque()
    self.reference = [(x, random()) for x in values]

    for val in self.reference:
      self.iks.AddObservation(val, 1)

    for val in values:
      wrnd = (val, random())
      self.sw.append(wrnd)
      self.iks.AddObservation(wrnd, 2)

  def Increment(self, value):
    '''Remove the oldest observation from the sliding window and replace it with a given value.
    
    Args:
      value: the new observation.
    '''
    self.iks.RemoveObservation(self.sw.popleft(), 2)
    wrnd = (value, random())
    self.iks.AddObservation(wrnd, 2)
    self.sw.append(wrnd)

  __call__ = Increment

  def Kuiper(self):
    '''Kuiper statistic. Both groups must have the same number of observations.

    Returns:
      The Kuiper statistic.
    '''
    return self.iks.Kuiper()

  def KS(self):
    '''Kolmogorov-Smirnov statistic. Both groups must have the same number of observations.

    Returns:
      The KS statistic D.
    '''
    return self.iks.KS()

  def Update(self):
    '''Updates the IKSSW. The reference window becomes the sliding window.
    '''
    for val in self.reference:
      self.iks.Remove(val, 1)

    self.reference.clear()
    for x in self.sw:
      self.reference.append((x[0], random()))

    for val in self.reference:
      self.iks.Add(val, 1)
  
  def Test(self, ca = 1.95):
    '''Test whether the reference and sliding window follow the different probability distributions according to KS Test.

    Args:
      ca: ca is a parameter used to calculate the threshold for the Kolmogorov-Smirnov statistic. The default value corresponds to a p-value of 0.001. Use IKS.CAForPValue to obtain an appropriate ca.

    Returns:
      True if we **reject** the null-hypothesis that states that both windows have the same distribution. In other words, we can consider that the windows have now different distributions.
    '''
    return self.iks.Test(ca)

if __name__ == "__main__":
  v = [random() for x in range(10)]
  ikssw = IKSSW(v)
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())
  for i in range(10):
    ikssw(random())
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())
  ikssw.Update()
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())
