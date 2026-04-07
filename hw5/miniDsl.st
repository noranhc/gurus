"First idiom:
keep valid scores
reject suspicious scores
reduce what remains to one total

Second example paragraph:
In our report cleanup, we first keep only non-empty entries.
Then we drop any test placeholders.
Then we return the cleaned list for reuse.

Second idiom:
keep usable entries
reject fake entries
return clean data"

Object subclass: ScoreTools [
    ScoreTools class >> cleanScores: scores [
        | passing |
        passing := scores select: [ :each | each >= 50 ].
        ^ passing reject: [ :each | each > 100 ]
    ]

    ScoreTools class >> totalOfCleanScores: scores [
        | cleaned |
        cleaned := self cleanScores: scores.
        ^ cleaned inject: 0 into: [ :total :each | total + each ]
    ]
]

| scores cleaned cleanedTotal |

scores := #(20 55 70 101 85 49 100 200).
cleaned := ScoreTools cleanScores: scores.
cleanedTotal := ScoreTools totalOfCleanScores: scores.

'clean scores:' printNl.
cleaned printNl.
'cleaned total:' printNl.
cleanedTotal printNl.
