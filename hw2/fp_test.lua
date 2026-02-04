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

-- Helper function for scalar test results
local function print_scalar_test(name, result, expected)
    print("Test " .. name)
    print("Result: " .. result)
    print("Expected: " .. expected)
    print(result == expected and "PASS" or "FAIL")
    print("")
end

-- Test C3: reject - should filter out even numbers
local result3 = reject({1,2,3,4,5}, function(x) return x%2==0 end)
print_test("C3: reject({1,2,3,4,5}, function(x) return x%2==0 end)", result3, "{1,3,5}")

-- Test C4: inject - should sum elements
local result4a = inject({1,2,3,4}, 0, function(a,x) return a+x end)
print_scalar_test("C4: inject({1,2,3,4}, 0, function(a,x) return a+x end)", result4a, 10)

-- Test C4: inject - should multiply elements
local result4b = inject({1,2,3,4}, 1, function(a,x) return a*x end)
print_scalar_test("C4: inject({1,2,3,4}, 1, function(a,x) return a*x end)", result4b, 24)
