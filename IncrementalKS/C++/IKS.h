#ifndef IKS_H
#define IKS_H

#include <random>
#include "Treap.h"

enum SampleID { SampleA, SampleB };
typedef Treap<double, double> TreapDD;

template<class URNG>
class IncrementalKS {
  private:
  
  TreapDD* treap;
  int count_a;
  int count_b;
  std::uniform_int_distribution<> distribution;
  URNG* generator;
  
  public:
  
  IncrementalKS(URNG* generator); // does not keep ownership of URNG

  double PValue();
  
  // ca defines the significance level.
  // ca = 1.22 => alpha = 0.10
  // ca = 1.36 => alpha = 0.05
  // ca = 1.48 => alpha = 0.025
  // ca = 1.63 => alpha = 0.01
  // ca = 1.73 => alpha = 0.005
  // ca = 1.95 => alpha = 0.001 (default)
  bool Test(double ca = 1.95);
  
  void AddObservation(double obs, SampleID sample);
  void RemoveObservation(double obs, SampleID sample);
  
  virtual ~IncrementalKS();
};

#include "IKS.inl"

#endif
 