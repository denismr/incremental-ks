#include "IKS.h"
#include <iostream>
#include <chrono>

typedef Treap<double, double> TreapDD;

int main() {
  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  std::default_random_engine generator (seed);
  
  IncrementalKS<std::default_random_engine> iks(&generator);
  
  int n;
  
  std::cin >> n;
  std::cout << "Inserting\n\n";
  for (int i = 0; i < n; i++) {
    double a, b;
    std::cin >> a >> b;
    iks.AddObservation(a, SampleA);
    iks.AddObservation(b, SampleB);
    std::cout << iks.KS() << std::endl;
  }
  
  std::cout << "\nRemoving\n\n";
  for (int i = 0; i < n; i++) {
    double a, b;
    std:: cin >> a >> b;
    iks.RemoveObservation(a, SampleA);
    iks.RemoveObservation(b, SampleB);
    std::cout << iks.KS() << std::endl;
  }
  
  return 0;
}