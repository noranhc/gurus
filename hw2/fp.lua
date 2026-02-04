-- C3: reject() returns a new table containing only elements where f returns false
-- t is the input table, f is a predicate function that takes an element and returns a boolean
function reject(t, f)
  local out = {}
  for _, v in ipairs(t) do
    if not f(v) then
      out[#out + 1] = v
    end
  end
  return out
end

-- C4: inject() folds a table from left to right, accumulating a single result value
-- t is the input table, acc is the initial accumulator value,
-- f is a function that takes (accumulator, element) and returns the new accumulator
function inject(t, acc, f)
  for _, v in ipairs(t) do
    acc = f(acc, v)
  end
  return acc
end

-- Tests
-- C3: Test reject()
print("reject test: filter out even numbers from {1,2,3,4,5}")
local result = reject({1,2,3,4,5}, function(x) return x%2==0 end)
print("{" .. table.concat(result, ",") .. "}") --> {1,3,5}

-- C4: Test inject()
print("\ninject test: sum of {1,2,3,4}")
print(inject({1,2,3,4}, 0, function(a,x) return a+x end))  --> 10

print("\ninject test: product of {1,2,3,4}")
print(inject({1,2,3,4}, 1, function(a,x) return a*x end))  --> 24
