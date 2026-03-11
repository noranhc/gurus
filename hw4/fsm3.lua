local M = {}

-- Q1: Trace-aware run. Appends to p.trace before each transition.
-- Q3: Guards. If a transition value is a function, call it with p to get the target state.
-- Q4: Wildcards. Falls back to "*" key before defaulting to current state.
local function run(rules, s, p)
  if rules[s] and rules[s].action then rules[s].action(p) end
  local e = table.remove(p.queue, 1)
  if not e then return p end
  local trans = rules[s].transitions or {}
  local raw   = trans[e] or trans["*"] or s
  local next  = type(raw) == "function" and raw(p)
                or raw
  p.trace = p.trace or {}
  p.trace[#p.trace + 1] = string.format("[%s] %s -> %s", e, s, next)
  return run(rules, next, p)
end

-- Q1: Print the full trace after the FSM finishes
function M.print_trace(p)
  print("\n=== TRACE ===")
  for _, line in ipairs(p.trace or {}) do print(line) end
end

-- Q2: Static linter
function M.lint(rules, initial)
  local names = {}
  for name in pairs(rules) do names[name] = true end
  local targeted = {}
  for src, rule in pairs(rules) do
    if not rule.transitions or not next(rule.transitions) then
      print(string.format("WARN dead-end: '%s' has no transitions", src))
    end
    for event, tgt in pairs(rule.transitions or {}) do
      if type(tgt) == "string" then
        if not names[tgt] then
          print(string.format("WARN ghost state: '%s' --%s--> '%s' (not in rules)", src, event, tgt))
        end
        targeted[tgt] = true
      end
    end
  end

  for name in pairs(names) do
    if name ~= initial and not targeted[name] then
      print(string.format("WARN unreachable: '%s' is never a transition target", name))
    end
  end
end

-- Q5: DOT exporter
function M.to_dot(rules)
  local lines = { "digraph fsm {" }
  local sorted = {}
  for name in pairs(rules) do sorted[#sorted + 1] = name end
  table.sort(sorted)
  for _, src in ipairs(sorted) do
    local trans = rules[src].transitions or {}
    local events = {}
    for ev in pairs(trans) do events[#events + 1] = ev end
    table.sort(events)
    for _, ev in ipairs(events) do
      local tgt = trans[ev]
      if type(tgt) == "string" then
        lines[#lines + 1] = string.format('  %s -> %s [ label="%s" ]', src, tgt, ev)
      else
        lines[#lines + 1] = string.format('  %s -> ? [ label="%s (guard)" ]', src, ev)
      end
    end
  end
  lines[#lines + 1] = "}"
  return table.concat(lines, "\n")
end

function M.start(rules, s, p)
  p.trace = {}
  return run(rules, s, p)
end

return M
