from random import random

class Treap:
  def __init__(self, key, value = 0):
    self.key = key
    self.value = value
    self.priority = random()
    self.size = 1
    self.height = 1
    self.lazy = 0
    self.max_value = value
    self.min_value = value
    self.left = None
    self.right = None

  @staticmethod
  def SumAll(node, value):
    if node is None:
      return
    node.value += value
    node.max_value += value
    node.min_value += value
    node.lazy += value
  
  @classmethod
  def Unlazy(cls, node):
    cls.SumAll(node.left, node.lazy)
    cls.SumAll(node.right, node.lazy)
    node.lazy = 0

  @classmethod
  def Update(cls, node):
    if node is None:
      return
    cls.Unlazy(node)
    node.size = 1
    node.height = 0
    node.max_value = node.value
    node.min_value = node.value

    if node.left is not None:
      node.size += node.left.size
      node.height = node.left.height
      node.max_value = max(node.max_value, node.left.max_value)
      node.min_value = min(node.min_value, node.left.min_value)
    
    if node.right is not None:
      node.size += node.right.size
      node.height = max(node.height, node.right.height)
      node.max_value = max(node.max_value, node.right.max_value)
      node.min_value = min(node.min_value, node.right.min_value)
    
    node.height += 1
  
  @classmethod
  def SplitKeepRight(cls, node, key):
    if node is None:
      return None, None

    left, right = None, None
    
    cls.Unlazy(node)

    if key <= node.key:
      left, node.left = cls.SplitKeepRight(node.left, key)
      right = node
    else:
      node.right, right = cls.SplitKeepRight(node.right, key)
      left = node
    
    cls.Update(left)
    cls.Update(right)

    return left, right

  @classmethod
  def Merge(cls, left, right):
    if left is None:
      return right
    if right is None:
      return left
    
    node = None

    if left.priority > right.priority:
      cls.Unlazy(left)
      left.right = cls.Merge(left.right, right)
      node = left
    else:
      cls.Unlazy(right)
      right.left = cls.Merge(left, right.left)
      node = right
    
    cls.Update(node)
    return node

  @classmethod
  def SplitSmallest(cls, node):
    if node is None:
      return None, None

    left, right = None, None
    
    cls.Unlazy(node)

    if node.left is not None:
      left, node.left = cls.SplitSmallest(node.left)
      right = node
    else:
      right = node.right
      node.right = None
      left = node
    
    cls.Update(left)
    cls.Update(right)

    return left, right

  @classmethod
  def SplitGreatest(cls, node):
    if node is None:
      return None, None
    
    cls.Unlazy(node)

    if node.right is not None:
      node.right, right = cls.SplitGreatest(node.right)
      left = node
    else:
      left = node.left
      node.left = None
      right = node
    
    cls.Update(left)
    cls.Update(right)

    return left, right

  @staticmethod
  def Size(node):
    return 0 if node is None else node.size
  
  @staticmethod
  def Height(node):
    return 0 if node is None else node.height

  @classmethod
  def _ToList(cls, node, extractor, _list = None):
    if _list is None:
      _list = []
    if node is None:
      return _list
    cls.Unlazy(node)
    cls._ToList(node.left, extractor, _list)
    _list.append(extractor(node))
    cls._ToList(node.right, extractor, _list)
    return _list
  
  @classmethod
  def KeysToList(cls, node, _list = None):
    extractor = lambda x: x.key
    return cls._ToList(node, extractor, _list)

  @classmethod
  def ValuesToList(cls, node, _list = None):
    extractor = lambda x: x.value
    return cls._ToList(node, extractor, _list)
