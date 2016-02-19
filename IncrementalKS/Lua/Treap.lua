--[[
  Treap with Lazy Propagation

  O(1) operations:
    -> Adds a constant value to all elements
    -> Computes the maximum value of the treap
    -> Computes the minimum value of the treap
    -> Computes the height of the treap
]]

local function SumAll(node, value)
  if node then
    node.value = node.value + value
    node.max_value = node.max_value + value
    node.min_value = node.min_value + value
    node.lazy = node.lazy + value
  end
end

local function Unlazy(node)
  if node then
    SumAll(node.left, node.lazy)
    SumAll(node.right, node.lazy)
    node.lazy = 0
  end
end

local function CreateNode(key, value)
  return {
    key = key,
    priority = math.random(),
    size = 1,

    value = value or 0,
    lazy = 0,
    max_value = value or 0,
    min_value = value or 0,
    height = 1,
  }
end

local function Update(node)
  if not node then return end
  Unlazy(node)
  node.size = 1
  node.height = 0
  node.max_value = node.value
  node.min_value = node.value

  if node.left then
    node.size = node.size + node.left.size
    node.height = node.left.height
    node.max_value = math.max(node.max_value, node.left.max_value)
    node.min_value = math.min(node.min_value, node.left.min_value)
  end

  if node.right then
    node.size = node.size + node.right.size
    node.height = math.max(node.height, node.right.height)
    node.max_value = math.max(node.max_value, node.right.max_value)
    node.min_value = math.min(node.min_value, node.right.min_value)
  end

  node.height = node.height + 1
end

local function SplitKeepRight(node, key)
  local left, right

  if not node then
    return nil, nil
  end

  Unlazy(node)

  if key <= node.key then
    left, node.left = SplitKeepRight(node.left, key)
    right = node
  else
    node.right, right = SplitKeepRight(node.right, key)
    left = node
  end

  Update(left)
  Update(right)

  return left, right
end

local function Merge(left, right)
  if not left then return right end
  if not right then return left end
  local node

  if left.priority > right.priority then
    Unlazy(left)
    left.right = Merge(left.right, right)
    node = left
  else
    Unlazy(right)
    right.left = Merge(left, right.left)
    node = right
  end

  Update(node)
  return node
end

local function SplitSmallest(node)
  local left, right
  if not node then
    return nil, nil
  end

  Unlazy(node)

  if node.left then
    left, node.left = SplitSmallest(node.left)
    right = node
  else
    right = node.right
    node.right = nil
    left = node
  end
  Update(left)
  Update(right)
  return left, right
end

local function SplitGreatest(node)
  local left, right
  if not node then
    return nil, nil
  end

  Unlazy(node)

  if node.right then
    node.right, right = SplitGreatest(node.right)
    left = node
  else
    left = node.left
    node.left = nil
    right = node
  end
  Update(left)
  Update(right)
  return left, right
end

local function Size(node)
  if not node then return 0 end
  return node.size
end

local function Height(node)
  if not node then
    return 0
  else
    return node.height
  end
end

return {
  CreateNode = CreateNode,
  Height = Height,
  Merge = Merge,
  Size = Size,
  SplitKeepRight = SplitKeepRight,
  SplitSmallest = SplitSmallest,
  SplitGreatest = SplitGreatest,
  Update = Update,
  SumAll = SumAll,
}
