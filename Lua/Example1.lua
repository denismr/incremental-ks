local IKS = require 'IncrementalKS'

-- Compute two pseudo-random normal variables
-- Default mean (mu) = 0
-- Deafult standard deviation (sigma) = 1
local function BoxMuller(mu, sigma)
  mu = mu or 0
  sigma = sigma or 1
  local x1, x2, w, y1, y2

  repeat
    x1 = 2.0 * math.random() - 1.0
    x2 = 2.0 * math.random() - 1.0
    w = x1 * x1 + x2 * x2
  until w < 1

  w = math.sqrt((-2.0 * math.log(w)) / w)
  y1 = x1 * w
  y2 = x2 * w

  return y1 * sigma + mu, y2 * sigma + mu
end

-- Creates one instance of the Incremental Kolmogorov Smirnov structure
local iks = IKS()

local minimum_number_of_observations = 100

-- Every run of this file will produce a different result
math.randomseed(os.time())

-- Inserts the minimum ammount of observations into each sample
for i = 1, minimum_number_of_observations do
  iks:AddElement(BoxMuller(), 1)
  iks:AddElement(BoxMuller(0.1), 2)
end

repeat
  iks:AddElement(BoxMuller(), 1)
  iks:AddElement(BoxMuller(0.1), 2)
until iks:Test()

print('# elements until difference is detected:', iks.n[1])
