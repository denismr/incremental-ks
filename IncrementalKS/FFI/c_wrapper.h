// cl /O2 /LD c_wrapper.cpp /Feiks.dll /EHsc

#ifndef CWRAPPER_H
#define CWRAPPER_H

extern "C" {

  typedef struct {
    void * pointer;    
  } IKS_WrappedPointer;
  
  __declspec(dllexport)
  IKS_WrappedPointer IKS_NewGeneratorWithSeed(unsigned seed);

  __declspec(dllexport)
  IKS_WrappedPointer IKS_NewGenerator(void);

  __declspec(dllexport)
  void IKS_DeleteGenerator(IKS_WrappedPointer pointer);

  __declspec(dllexport)
  IKS_WrappedPointer IKS_NewIKS(IKS_WrappedPointer generatorPointer);

  __declspec(dllexport)
  void IKS_DeleteIKS(IKS_WrappedPointer pointer);

  __declspec(dllexport)
  int IKS_Test(IKS_WrappedPointer pointer, double ca);

  __declspec(dllexport)
  double IKS_KS(IKS_WrappedPointer pointer);

  __declspec(dllexport)
  double IKS_Kuiper(IKS_WrappedPointer pointer);

  __declspec(dllexport)
  void IKS_AddObservation(IKS_WrappedPointer pointer, double obs, int which_sample);

  __declspec(dllexport)
  void IKS_RemoveObservation(IKS_WrappedPointer pointer, double obs, int which_sample);
}

#endif