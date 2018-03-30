local ffi = require 'ffi'

ffi.cdef [[

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

]]

local clib = ffi.load 'iks'
local global_generator = ffi.gc(clib.IKS_NewGenerator(), clib.IKS_DeleteGenerator);

local meta = {
  __index = {
    AddObservation = function(self, obs, sample)
      clib.IKS_AddObservation(self.wp, obs, sample)
    end,
    RemoveObservation = function(self, obs, sample)
      clib.IKS_RemoveObservation(self.wp, obs, sample)
    end,
    KS = function(self)
      return clib.IKS_KS(self.wp)
    end,
    Kuiper = function(self)
      return clib.IKS_Kuiper(self.wp)
    end,
    Test = function(self, ca)
      return clib.IKS_Test(self.wp, ca or 1.95) == 1
    end,
  }
}

return function()
  return setmetatable({
    wp = ffi.gc(clib.IKS_NewIKS(global_generator), clib.IKS_DeleteIKS),
  }, meta)
end

