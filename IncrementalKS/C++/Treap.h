#ifndef TREAP_H
#define TREAP_H

template <typename K, typename V> class Treap {
  private:
  K key;
  int priority;
  int size;
  int height;
  V value;
  V max_value;
  V min_value;
  V lazy;
  
  Treap* left;
  Treap* right;
  
  static void Unlazy(Treap* node);
  static void Update(Treap* node);
  
  public:
  
  Treap(K key, V value, int priority);
  static void SumAll(Treap* node, V value);
  
  static Treap* Merge(Treap* left, Treap* right);
  static void SplitKeepRight(Treap* node, K key, Treap** left, Treap** right);
  static void SplitSmallest(Treap* node, Treap** left, Treap** right);
  static void SplitGreatest(Treap* node, Treap** left, Treap** right);
  
  static int Size(const Treap* node);
  static int Height(const Treap* node);
  
  inline K Key();
  inline V Value();
  inline V MaxValue();
  inline V MinValue();
  
  virtual ~Treap();
};

#include "Treap.inl"

#endif
