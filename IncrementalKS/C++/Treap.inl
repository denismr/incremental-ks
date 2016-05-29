template <typename K, typename V>
Treap<K, V>::Treap(K key, V value, int priority) {
  this->key = key;
  this->value = value;
  this->priority = priority;
  
  size = 1;
  height = 1;
  
  lazy = 0;
  max_value = value;
  min_value = value;
  
  left = nullptr;
  right = nullptr;
}

template<typename K, typename V>
Treap<K, V>::~Treap() {
  if (left != nullptr) delete left;
  if (right != nullptr) delete right;
}

template<typename K, typename V> void
Treap<K, V>::SumAll(Treap* node, V value) {
  if (node != nullptr) {
    node->value = node->value + value;
    node->max_value = node->max_value + value;
    node->min_value = node->min_value + value;
    node->lazy = node->lazy + value;
  }
}

template<typename K, typename V> void
Treap<K, V>::Unlazy(Treap* node) {
  if (node != nullptr) {
    SumAll(node->left, node->lazy);
    SumAll(node->right, node->lazy);
    node->lazy = 0;
  }
}

template<typename K, typename V> void
Treap<K, V>::Update(Treap* node) {
  if (node == nullptr) return;
  Unlazy(node);
  node->size = 1;
  node->height = 0;
  node->max_value = node->value;
  node->min_value = node->value;
  
  if (node->left != nullptr) {
    node->size = node->size + node->left->size;
    node->height = node->left->height;
    if (node->left->max_value > node->max_value) {
      node->max_value = node->left->max_value;
    }
    if (node->left->min_value < node->min_value) {
      node->min_value = node->left->min_value;
    }
  }
  
  if (node->right != nullptr) {
    node->size = node->size + node->right->size;
    node->height = node->right->height;
    if (node->right->max_value > node->max_value) {
      node->max_value = node->right->max_value;
    }
    if (node->right->min_value < node->min_value) {
      node->min_value = node->right->min_value;
    }
  }
  
  node->height = node->height + 1;
}

template<typename K, typename V> Treap<K, V>*
Treap<K, V>::Merge(Treap* left, Treap* right) {
  if (left == nullptr) return right;
  if (right == nullptr) return left;
  Treap* node;
  
  if (left->priority > right->priority) {
    Unlazy(left);
    left->right = Merge(left->right, right);
    node = left;
  } else {
    Unlazy(right);
    right->left = Merge(left, right->left);
    node = right;
  }
  
  Update(node);
  return node;
}

template<typename K, typename V> void
Treap<K, V>::SplitKeepRight(Treap* node, K key, Treap** left, Treap** right) {
  *left = nullptr;
  *right = nullptr;
  
  if (node == nullptr) return;
  
  Unlazy(node);
  
  if (key <= node->key) {
    SplitKeepRight(node->left, key, left, &node->left);
    *right = node;
  } else {
    SplitKeepRight(node->right, key, &node->right, right);
    *left = node;
  }
  
  Update(*left);
  Update(*right);
}

template<typename K, typename V> void
Treap<K, V>::SplitSmallest(Treap* node, Treap** left, Treap** right) {
  *left = nullptr;
  *right = nullptr;
  
  if (node == nullptr) return;
  
  Unlazy(node);
  
  if (node->left) {
    SplitSmallest(node->left, left, &node->left);
    *right = node;
  } else {
    *right = node->right;
    node->right = nullptr;
    *left = node;
  }
  
  Update(*left);
  Update(*right);
}

template<typename K, typename V> void
Treap<K, V>::SplitGreatest(Treap* node, Treap** left, Treap** right) {
  *left = nullptr;
  *right = nullptr;
  
  if (node == nullptr) return;
  
  Unlazy(node);
  
  if (node->right) {
    SplitGreatest(node->right, &node->right, right);
    *left = node;
  } else {
    *left = node->left;
    node->left = nullptr;
    *right = node;
  }
  
  Update(*left);
  Update(*right);
}

template<typename K, typename V> int
Treap<K, V>::Size(const Treap* node) {
  return node == nullptr ? 0 : node->size;
}

template<typename K, typename V> int
Treap<K, V>::Height(const Treap* node) {
  return node == nullptr ? 0 : node->height;
}

template<typename K, typename V> V
Treap<K, V>::Value() {
  return value;
}

template<typename K, typename V> V
Treap<K, V>::MaxValue() {
  return max_value;
}

template<typename K, typename V> V
Treap<K, V>::MinValue() {
  return min_value;
}

template<typename K, typename V> K
Treap<K, V>::Key() {
  return key;
}

