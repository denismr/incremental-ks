local idx = {}
local mt = {__index = idx}

function idx:Reset()
  self.v = {}
  self.nex = 1
  return self
end

function idx:GetCurrentSize()
  return #self.v
end

function idx:GetInOrderValues()
  local t = {}
  for i = self.nex, #self.v do
    t[#t + 1] = self.v[i]
  end
  for i = 1, self.nex - 1 do
    t[#t + 1] = self.v[i]
  end
  return t
end

function idx:GetValues()
  if self.wfcl then
    return #self.v == self.size and self.nex == 1 and self.v
  end
  return #self.v == self.size and self.v
end

function idx:ForceGetValues()
  return self.v
end

function idx:Add(value)
  self.v[self.nex] = value
  self.nex = self.nex + 1
  if self.nex > self.size then
    self.nex = 1
  end
end

function idx:GetNex()
  return self.v[self.nex]
end

function idx:GetOldest()
  return self.v[self.nex]
end

idx.GetNext = idx.GetNex

return function(size, wait_for_complete_loop)
  if type(size) == 'table' then
    local r = setmetatable({size = #size,
        wfcl = wait_for_complete_loop}, mt):Reset()
    for i, v in ipairs(size) do
      r:Add(v)
    end
    return r
  else
    return setmetatable({size = size,
        wfcl = wait_for_complete_loop}, mt):Reset()
  end
end
