-- Test file for fp.lua
dofile("fp.lua")

-- Helper function to print test results
local function print_test(name, result, expected)
    print("Test " .. name)
    local result_str = "{" .. table.concat(result, ",") .. "}"
    print("Result: " .. result_str)
    print("Expected: " .. expected)
    print(table.concat(result, ",") == expected:sub(2, -2) and "PASS" or "FAIL")
    print("")
end

-- Test C1: collect - should transform each element
local result1 = collect({1,2,3}, function(x) return x*x end)
print_test("C1: collect({1,2,3}, function(x) return x*x end)", result1, "{1,4,9}")

-- Test C2: select - should filter even numbers
local result2 = select({1,2,3,4,5}, function(x) return x%2==0 end)
print_test("C2: select({1,2,3,4,5}, function(x) return x%2==0 end)", result2, "{2,4}")
