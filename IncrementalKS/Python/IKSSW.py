from IKS import IKS
from ForgettingBuffer import ForgettingBuffer as FB

class IKSSW:
  def __init__(self, values):
    self.sw = FB(values)
    self.iks = IKS()
    for val in values:
      self.iks.AddObservation(val, 1)
      self.iks.AddObservation(val, 2)

  def Increment(self, value):
    rem = self.sw(value)
    self.iks.RemoveObservation(rem, 2)
    self.iks.AddObservation(value, 2)

  __call__ = Increment

  def Kuiper(self):
    return self.iks.Kuiper()

  def KS(self):
    return self.iks.KS()
  
  def Test(self, ca = 1.95):
    return self.iks.Test(ca)


if __name__ == "__main__":
  from random import random as rnd
  v = [rnd() for x in range(10)]
  ikssw = IKSSW(v)
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())
  for i in range(10):
    ikssw(rnd())
  print(ikssw.KS(), ikssw.Kuiper(), ikssw.Test())