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
    clib.IKS_AddObservation(self.wp, obs, sample)
  
  def RemoveObservation(self, obs, sample):
    clib.IKS_RemoveObservation(self.wp, obs, sample)
  
  def KS(self):
    return clib.IKS_KS(self.wp)
  
  def Kuiper(self):
    return clib.IKS_Kuiper(self.wp)
  
  def Test(self, ca = 1.95):
    return clib.IKS_Test(self.wp, ca) == 1

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
