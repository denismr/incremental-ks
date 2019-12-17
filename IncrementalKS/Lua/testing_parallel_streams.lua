local IKS = require 'IncrementalKS'
local RB = require 'RotatingBuffer'

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

initial_A = {}
initial_B = {}

stream_A = {}
stream_B = {}

for i = 1, 500 do
  table.insert(initial_A, (BoxMuller(0, 1)))
  table.insert(initial_B, (BoxMuller(1, 1)))
end

for i = 1, 5000 do
  table.insert(stream_A, (BoxMuller(0, 1)))
  table.insert(stream_B, (BoxMuller(1, 1)))
end

start = os.clock()

iks_statistics = {}
sliding_A = RB(initial_A)
sliding_B = RB(initial_B)
iks = IKS()

for i = 1, #initial_A do
  iks:Add(initial_A[i], 1)
  iks:Add(initial_B[i], 2)
end

for i = 1, #stream_A do
  iks:Remove(sliding_A:GetOldest(), 1)
  iks:Remove(sliding_B:GetOldest(), 2)
  iks:Add(stream_A[i], 1)
  iks:Add(stream_B[i], 2)
  sliding_A:Add(stream_A[i])
  sliding_B:Add(stream_B[i])
  table.insert(iks_statistics, iks:KS())
end

print(#iks_statistics)

finish = os.clock()

print(finish - start)

-- for i = 1, 100 do
--   print(iks_statistics[i])
-- end
