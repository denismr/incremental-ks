#include "c_wrapper.h"
#include "IKS.h"
#include <chrono>

IKS_WrappedPointer IKS_NewGeneratorWithSeed(unsigned seed) {
  IKS_WrappedPointer wp;
  auto * generator = new std::default_random_engine(seed);
  wp.pointer = reinterpret_cast<void*>(generator);
  return wp;
}

IKS_WrappedPointer IKS_NewGenerator(void) {
  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  return IKS_NewGeneratorWithSeed(seed);
}

void IKS_DeleteGenerator(IKS_WrappedPointer wp) {
  auto * generator = reinterpret_cast<std::default_random_engine*>(wp.pointer);
  delete generator;
}

IKS_WrappedPointer IKS_NewIKS(IKS_WrappedPointer gen_wp) {
  IKS_WrappedPointer wp;
  auto * generator = reinterpret_cast<std::default_random_engine*>(gen_wp.pointer);
  auto * iks = new IncrementalKS<std::default_random_engine>(generator);
  wp.pointer = reinterpret_cast<void*>(iks);
  return wp;
}

void IKS_DeleteIKS(IKS_WrappedPointer wp) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  delete iks;
}

int IKS_Test(IKS_WrappedPointer wp, double ca) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  return iks->Test() ? 1 : 0;
}

double IKS_KS(IKS_WrappedPointer wp) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  return iks->KS();
}

double IKS_Kuiper(IKS_WrappedPointer wp) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  return iks->Kuiper();
}

void IKS_AddObservation(IKS_WrappedPointer wp, double obs, int which_sample) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  return iks->AddObservation(obs, which_sample == 1 ? SampleA : SampleB);
}

void IKS_RemoveObservation(IKS_WrappedPointer wp, double obs, int which_sample) {
  auto * iks = reinterpret_cast<IncrementalKS<std::default_random_engine>*>(wp.pointer);
  return iks->RemoveObservation(obs, which_sample == 1 ? SampleA : SampleB);
}
