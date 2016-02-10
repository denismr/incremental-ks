--[[
  Incremental Kolmogorov Smirnov Algorithm
  Implemented by Denis Moreira dos Reis
                 denismr at gmail dot com

    How to use:
    local IKS = require 'IncrementalKS'

    my_iks = IKS()

    my_iks:AddElement(OBSERVATION, SAMPLE_ID) -> void
    and
    my_iks:RemoveElement(OBSERVATION, SAMPLE_ID) -> void

    OBSERVATION is a real number and SAMPLE_ID is either 1 or 2.

    local RejectNullHypotheis = my_iks:Test() -> boolean

    This specific implementation assumes
      -> significance level of 0.05
      -> |A| = |B| = m = n

    These assumptions are in the Test() function, and therefore can be easily modified.
  ]]


-- Requirements
local Treap = require 'Treap'

-- Meta
local idx = {}
local mt = {__index = idx}

function idx:Test()
  assert(self.n[1] == self.n[2])
  local n = self.n[1]
  if n == 0 then return false end

  local supremum = math.max(self.treap.max_value, -self.treap.min_value) / n
  return supremum > 1.36 * math.sqrt(2 * n / n ^ 2)
end

function idx:AddElement(key, group)
  self.n[group] = self.n[group] + 1

  local left, left_g, right, val

  left, right = Treap.SplitKeepRight(self.treap, key)

  left, left_g = Treap.SplitGreatest(left)
  val = left_g and left_g.value or 0
  left = Treap.Merge(left, left_g)

  right = Treap.Merge(Treap.CreateNode(key, val), right)

  Treap.SumAll(right, group == 1 and 1 or -1)

  self.treap = Treap.Merge(left, right)
end

function idx:RemoveElement(key, group)
  self.n[group] = self.n[group] - 1
  local left, right, right_l

  left, right = Treap.SplitKeepRight(self.treap, key)
  right_l, right = Treap.SplitSmallest(right)

  if right_l and right_l.key == key then
    Treap.SumAll(right, group == 1 and -1 or 1)
  else
    right = Treap.Merge(right_l, right)
  end

  self.treap = Treap.Merge(left, right)
end

return function()
  return setmetatable({
      treap = nil,
      n = {0, 0},
    }, mt)
end