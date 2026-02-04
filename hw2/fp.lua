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
