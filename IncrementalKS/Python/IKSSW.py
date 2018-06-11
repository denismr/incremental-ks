from IKS import IKS
from ForgettingBuffer import ForgettingBuffer as FB
from scipy.stats import ks_2samp as KSTest
from math import sqrt

class IKSSW:
  def __init__(self, values):
    self.sw = FB(values)
    self.iks = IKS()
    self.values = values
    self.increments = 0
    for val in values:
      self.iks.AddObservation(val, 1)
      self.iks.AddObservation(val, 2)

  def Increment(self, value):
    rem = self.sw(value)
    self.iks.RemoveObservation(rem, 2)
    self.iks.AddObservation(value, 2)
    self.increments += 1

  __call__ = Increment

  def Kuiper(self):
    return self.iks.Kuiper()

  def KS(self):
    if self.increments < len(self.values):
      return KSTest(self.values, self.sw.Values()).statistic
    else:
      return self.iks.KS()
  
  def Test(self, ca = 1.95):
    if self.increments < len(self.values):
      ks = KSTest(self.values, self.sw.Values()).statistic
      n = len(self.values)
      return ks > ca * sqrt(2.0 * n / (n * n))
    else:
      return self.iks.KS()

if __name__ == "__main__":
  from random import random as rnd
  v = [rnd() for x in range(10)]
  ikssw = IKSSW(v)
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())
  for i in range(10):
    ikssw(rnd())
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())