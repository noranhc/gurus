--[[
  Cleaned-up machine2.lua:
    Q0 – Four helper functions that eliminate clumsy idioms
    Q1 – Trace tool (built into fsm3.lua engine)
    Q2 – Linter (called before start)
    Q3 – Guard example (stamina-gated attack)
    Q4 – Wildcard transition demo
    Q5 – DOT export
]]--
local machine = require"fsm3"

-----------------------------------------------------------------
-- Q0  HELPER FUNCTIONS (four idiom fixes)
-----------------------------------------------------------------

-- Fix 1: say() — kills string-concatenation spam in actions
local function say(msg)
  return function(p)
    print(string.format("[%s] %s", p.name, msg:gsub("{hp}", p.hp))) end end

-- Fix 2: T() — shorthand transition builder (removes repeated `transitions = { ... }` boilerplate)
--   Before: transitions = { walk = "moving", attack = "attacking", hit = "staggered", die = "dead" }
--   After:  T{ walk="moving", attack="attacking", hit="staggered", die="dead" }
--   (Here it's a trivial identity, but it documents intent and lets us add
--    default entries like the wildcard in one place later.)
local function T(tbl) return tbl end

-- Fix 3: hit() — extracts the duplicated damage-processing logic into a reusable closure
--   Before: a 9-line anonymous function copy-pasted into the `staggered` action
--   After:  action = hit()
local function hit()
  return function(p)
    local dmg = table.remove(p.damage_queue, 1) or 0
    p.hp = p.hp - dmg
    print(string.format("   > BOOM! [%s] took %d damage! HP is now %d", p.name, dmg, p.hp))
    if p.hp <= 0 then
      print("   > SYSTEM: Fatal damage detected! Injecting 'die' event...")
      table.insert(p.queue, 1, "die")
    end
  end
end

-- Fix 4: player() — builds the payload table from named arguments
--   Before: a raw table literal with magic keys scattered across lines
--   After:  player{ name="Hero", hp=100, queue={...}, damage_queue={...} }
local function player(t)
  return {
    name         = t.name         or "Unknown",
    hp           = t.hp           or 100,
    stamina      = t.stamina      or 50,
    queue        = t.queue        or {},
    damage_queue = t.damage_queue or {},
    trace        = {}
  }
end

-----------------------------------------------------------------
-- 1. RULES  (now much cleaner thanks to Q0 helpers)
-----------------------------------------------------------------
local rpg_rules = {
  idle = {
    action      = say("\nis idling. HP: {hp}"),
    transitions = T{ walk="moving",
                     attack=function(p)
                       return p.stamina > 10 and "attacking" or "idle" end,
                     hit="staggered", die="dead",
                     ["*"]="error" }
  },

  moving = {
    action      = say("is walking forward."),
    transitions = T{ stop="idle", attack="attacking", hit="staggered", die="dead" }
  },

  attacking = {
    action      = say("swings their weapon!"),
    transitions = T{ recover="idle", hit="staggered", die="dead" }
  },

  staggered = {
    action      = hit(),
    transitions = T{ recover="idle", die="dead" }
  },

  dead = {
    action      = say("has collapsed to the ground."),
    transitions = T{ revive="idle" }
  },

  -- Q4 demo: a catch-all error state reached by wildcards
  error = {
    action      = say("encountered an unknown event!"),
    transitions = T{ recover="idle" }
  }
}

-----------------------------------------------------------------
-- Q2  LINT — first demo on a broken rule set to show warnings
-----------------------------------------------------------------
print("=== LINT REPORT (bad rules) ===")
machine.lint({
  idle      = { transitions = { walk="moving", fly="flying" } },
  moving    = { transitions = { stop="idle" } },
  orphaned  = { transitions = { go="idle" } },
  trapped   = { }
}, "idle")

print("\n=== LINT REPORT (rpg_rules) ===")
machine.lint(rpg_rules, "idle")

-----------------------------------------------------------------
-- 2. PAYLOAD  (Fix 4 in action)
-----------------------------------------------------------------
local my_payload = player{
  name         = "Hero",
  hp           = 100,
  stamina      = 50,
  queue        = {
    "walk", "attack", "recover",
    "hit", "recover",
    "walk", "attack",
    "hit", "walk"
  },
  damage_queue = { 15, 90 }
}

-----------------------------------------------------------------
-- 3. RUN
-----------------------------------------------------------------
print("\n=== STARTING TCO RPG BATTLE ===")
local final = machine.start(rpg_rules, "idle", my_payload)

print("\n=== PROCESSING COMPLETE ===")
print("Final Queue Size remaining: " .. #final.queue)
print("Final HP: " .. final.hp)

-----------------------------------------------------------------
-- Q1  TRACE
-----------------------------------------------------------------
machine.print_trace(final)

-----------------------------------------------------------------
-- Q5  DOT EXPORT
-----------------------------------------------------------------
print("\n=== DOT EXPORT ===")
print(machine.to_dot(rpg_rules))
