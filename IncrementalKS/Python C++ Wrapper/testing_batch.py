from scipy.stats import ks_2samp
from IKS import IKS
import numpy as np

group_A = np.random.normal(loc = 0, scale = 1, size = 100)
group_B = np.random.normal(loc = 1, scale = 1, size = 100)

iks = IKS()


for x, y in zip(group_A, group_B):
  iks.Add(x, 0)
  iks.Add(y, 1)

print(iks.KS())
print(ks_2samp(group_A, group_B).statistic)