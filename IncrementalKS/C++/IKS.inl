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
IncrementalKS<URNG>::KS() {
  if (count_a != count_b) {
    throw "Samples must have equal size!";
  }
  
  if (count_a == 0) return 0.0;
  
  return std::max(treap->MaxValue(), -treap->MinValue()) / (double) count_a;
}

template<class URNG> double
IncrementalKS<URNG>::Kuiper() {
  if (count_a != count_b) {
    throw "Samples must have equal size!";
  }
  
  if (count_a == 0) return 0.0;
  
  return (treap->MaxValue() - treap->MinValue()) / (double) count_a;
}

template<class URNG> bool
IncrementalKS<URNG>::Test(double ca) {
  double n = (double) count_a;
  return KS() > ca * sqrt(2.0 * n / (n * n));
}

template<class URNG> void
IncrementalKS<URNG>::AddObservation(double _obs, SampleID sample) {
  std::pair<double, double> obs = std::make_pair(_obs, sample == SampleA ? 0.0 : 1.0);
  if (sample == SampleA) {
    count_a++;
  } else {
    count_b++;
  }
  
  TreapPDDD *left, *left_g, *right;
  double val;
  
  TreapPDDD::SplitKeepRight(treap, obs, &left, &right);
  
  TreapPDDD::SplitGreatest(left, &left, &left_g);
  val = left_g != nullptr ? left_g->Value() : 0.0;
  left = TreapPDDD::Merge(left, left_g);
  
  right = TreapPDDD::Merge(new TreapPDDD(obs, val,
      distribution(*generator)), right);
    
  TreapPDDD::SumAll(right, sample == SampleA ? 1.0 : -1.0);
  
  treap = TreapPDDD::Merge(left, right);
}

template<class URNG> void
IncrementalKS<URNG>::RemoveObservation(double _obs, SampleID sample) {
  std::pair<double, double> obs = std::make_pair(_obs, sample == SampleA ? 0.0 : 1.0);
  TreapPDDD *left, *right, *right_l;
  
  TreapPDDD::SplitKeepRight(treap, obs, &left, &right);
  TreapPDDD::SplitSmallest(right, &right_l, &right);
  
  if (right_l != nullptr && right_l->Key() == obs) {
    if (sample == SampleA) {
      count_a--;
      TreapPDDD::SumAll(right, -1.0);
    } else {
      count_b--;
      TreapPDDD::SumAll(right, 1.0);
    }
    
    delete right_l;
    
  } else if(right_l != nullptr) {
    right = TreapPDDD::Merge(right_l, right);
  }
  
  treap = TreapPDDD::Merge(left, right);
}
