| nums doubled evens kept sum |

nums := #(1 2 3 4 5 6).

"Task B1: do:"
'original collection:' printNl.
nums printNl.

'items one per line:' printNl.
nums do: [ :each | each printNl ].

"Task B2: collect:"
doubled := nums collect: [ :each | each * 2 ].
'result of collect:' printNl.
doubled printNl.

"Task B3: select:"
evens := nums select: [ :each | each even ].
'result of select:' printNl.
evens printNl.

"Task B4: reject:"
kept := nums reject: [ :each | each < 4 ].
'result of reject:' printNl.
kept printNl.

"Task B5: inject:into:"
sum := nums inject: 0 into: [ :total :each | total + each ].
'result of inject:into:' printNl.
sum printNl.
