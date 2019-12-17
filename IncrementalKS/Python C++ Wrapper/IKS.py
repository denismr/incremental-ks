from cffi import FFI

ffi = FFI()

ffi.cdef("""

typedef struct {
  void * pointer;    
} IKS_WrappedPointer;

IKS_WrappedPointer IKS_NewGeneratorWithSeed(unsigned seed);
IKS_WrappedPointer IKS_NewGenerator(void);
void IKS_DeleteGenerator(IKS_WrappedPointer pointer);
IKS_WrappedPointer IKS_NewIKS(IKS_WrappedPointer generatorPointer);
void IKS_DeleteIKS(IKS_WrappedPointer pointer);
int IKS_Test(IKS_WrappedPointer pointer, double ca);
double IKS_KS(IKS_WrappedPointer pointer);
double IKS_Kuiper(IKS_WrappedPointer pointer);
void IKS_AddObservation(IKS_WrappedPointer pointer, double obs, int which_sample);
void IKS_RemoveObservation(IKS_WrappedPointer pointer, double obs, int which_sample);
void IKS_AddCompositeObservation(IKS_WrappedPointer pointer, double obs, double obs_p2, int which_sample);
void IKS_RemoveCompositeObservation(IKS_WrappedPointer pointer, double obs, double obs_p2, int which_sample);
double IKS_KSThresholdForPValue(double pvalue, int N);
double IKS_CAForPValue(double pvalue);
""")

clib = ffi.dlopen("iks.dll")

class Generator:
  def __init__(self, seed = None):
    if seed == None:
      self.wp = clib.IKS_NewGenerator()
    else:
      self.wp  = clib.IKS_NewGeneratorWithSeed(seed)

  def __del__(self):
    clib.IKS_DeleteGenerator(self.wp)

global_generator = Generator()

class IKS:
  def __init__(self, generator = global_generator):
    self.wp = clib.IKS_NewIKS(generator.wp)

  def __del__(self):
    clib.IKS_DeleteIKS(self.wp)
  
  def AddObservation(self, obs, sample):
    '''Insert new observation into one of the groups.

    Args:
      obs: the value of the obseration. Tip: a tuple (actual value, random value) is recommended when there is overlap between groups or if values are not guaranteed to be mostly unique.
      group (int): which group the observation belongs to. Must be either 0 or 1.
    '''
    if isinstance(obs, tuple):
      clib.IKS_AddCompositeObservation(self.wp, obs[0], obs[1], sample)
    else:
      clib.IKS_AddObservation(self.wp, obs, sample)
  
  def RemoveObservation(self, obs, sample):
    '''Remove observation from one of the groups.

    Args:
      obs: the value of the obseration. Must be identical to a previously inserted observation (including the random element of a tuple, if this was the case).
      group (int): which group the observation belongs to. Must be either 0 or 1.
    '''
    if isinstance(obs, tuple):
      clib.IKS_RemoveCompositeObservation(self.wp, obs[0], obs[1], sample)
    else:
      clib.IKS_RemoveObservation(self.wp, obs, sample)
  
  def KS(self):
    '''Kolmogorov-Smirnov statistic. Both groups must have the same number of observations.

    Returns:
      The KS statistic D.
    '''
    return clib.IKS_KS(self.wp)
  
  def Kuiper(self):
    '''Kuiper statistic. Both groups must have the same number of observations.

    Returns:
      The Kuiper statistic.
    '''
    return clib.IKS_Kuiper(self.wp)
  
  def Test(self, ca = 1.95):
    '''Test whether the reference and sliding window follow the different probability distributions according to KS Test.

    Args:
      ca: ca is a parameter used to calculate the threshold for the Kolmogorov-Smirnov statistic. The default value corresponds to a p-value of 0.001. Use IKS.CAForPValue to obtain an appropriate ca.

    Returns:
      True if we **reject** the null-hypothesis that states that both windows have the same distribution. In other words, we can consider that the windows have now different distributions.
    '''
    return clib.IKS_Test(self.wp, ca) == 1

  @staticmethod
  def KSThresholdForPValue(pvalue, N):
    '''Threshold for KS Test given a p-value
    Args:
      pval (float): p-value.
      N (int): the size of the samples.

    Returns:
      Threshold t to compare groups 0 and 1. The null-hypothesis is discarded if KS() > t.
    '''
    return clib.IKS_KSThresholdForPValue(pvalue, N)
  
  @staticmethod
  def CAForPValue(pvalue):
    '''ca for KS Test given a p-value
    Args:
      pval (float): p-value.

    Returns:
      Threshold the "ca" that can be used to compute a threshold for KS().
    '''
    return clib.IKS_CAForPValue()

IKS.Add = IKS.AddObservation
IKS.Remove = IKS.RemoveObservation

if __name__ == "__main__":
  import random

  iks = IKS()
  for i in range(0, 10):
    iks.AddObservation(i, 0)
    iks.AddObservation(i, 1)

  print(iks.KS())
  print(iks.Kuiper())
  print(iks.Test())

  iks = IKS()
  for i in range(0, 10):
    iks.AddObservation(random.random(), 0)
    iks.AddObservation(random.random(), 1)

  print(iks.KS())
  print(iks.Kuiper())
  print(iks.Test())
