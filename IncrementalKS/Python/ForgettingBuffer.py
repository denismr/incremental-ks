class Node:
  def __init__(self, value):
    self.value = value
    self.next = None

class ForgettingBuffer:
  def __init__(self, values):
    self.first = None
    self.last = None

    for val in values:
      if self.first == None:
        self.first = Node(val)
        self.last = self.first
      else:
        self.last.next = Node(val)
        self.last = self.last.next

  def __iter__(self):
    cur = self.first
    while cur != None:
      yield cur.value
      cur = cur.next

  def Increment(self, value):
    first_value = self.first.value
    self.first = self.first.next
    self.last.next = Node(value)
    self.last = self.last.next
    return first_value

  Add = Increment
  __call__ = Increment

  def Values(self):
    return list(self)
  
if __name__ == "__main__":
  fb = ForgettingBuffer([1, 2, 3, 4, 5])
  for val in fb:
    print(val)
  fb(10)
  fb(11)
  fb(12)
  print(list(fb))
  print(fb.Values())
