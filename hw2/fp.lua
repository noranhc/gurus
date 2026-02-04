-- C1: collect(t, f) — return a new table with f applied to each element.
function collect(t, f) 
    local result = {}
    for i, v in ipairs(t) do
        result[#result + 1] = f(v)
    end
    return result
end

-- C2: select(t, f) — return elements where f returns true.
function select(t, f)
    local result = {}
    for i, v in ipairs(t) do
        if f(v) then
            result[#result + 1] = v
        end
    end
    return result
end

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
