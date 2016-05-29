#include <cstdlib>
#include <algorithm>

template<class URNG>
IncrementalKS<URNG>::IncrementalKS(URNG* generator) {
  this->generator = generator;
  treap = nullptr;
  count_a = 0;
  count_b = 0;
}

template<class URNG>
IncrementalKS<URNG>::~IncrementalKS() {
  if (treap != nullptr) {
    delete treap;
  }
}

template<class URNG> double
IncrementalKS<URNG>::PValue() {
  if (count_a != count_b) {
    throw "Samples must have equal size!";
  }
  
  if (count_a == 0) return 0.0;
  
  return std::max(treap->MaxValue(), -treap->MinValue()) / (double) count_a;
}

template<class URNG> bool
IncrementalKS<URNG>::Test(double ca) {
  double n = (double) count_a;
  return PValue() > ca * sqrt(2.0 * n / (n * n));
}

template<class URNG> void
IncrementalKS<URNG>::AddObservation(double obs, SampleID sample) {
  if (sample == SampleA) {
    count_a++;
  } else {
    count_b++;
  }
  
  TreapDD *left, *left_g, *right;
  double val;
  
  TreapDD::SplitKeepRight(treap, obs, &left, &right);
  
  TreapDD::SplitGreatest(left, &left, &left_g);
  val = left_g != nullptr ? left_g->Value() : 0.0;
  left = TreapDD::Merge(left, left_g);
  
  right = TreapDD::Merge(new TreapDD(obs, val,
      distribution(*generator)), right);
    
  TreapDD::SumAll(right, sample == SampleA ? 1.0 : -1.0);
  
  treap = TreapDD::Merge(left, right);
}

template<class URNG> void
IncrementalKS<URNG>::RemoveObservation(double obs, SampleID sample) {
  TreapDD *left, *right, *right_l;
  
  TreapDD::SplitKeepRight(treap, obs, &left, &right);
  TreapDD::SplitSmallest(right, &right_l, &right);
  
  if (right_l != nullptr && right_l->Key() == obs) {
    if (sample == SampleA) {
      count_a--;
      TreapDD::SumAll(right, -1.0);
    } else {
      count_b--;
      TreapDD::SumAll(right, 1.0);
    }
    
    delete right_l;
    
  } else if(right_l != nullptr) {
    right = TreapDD::Merge(right_l, right);
  }
  
  treap = TreapDD::Merge(left, right);
}
