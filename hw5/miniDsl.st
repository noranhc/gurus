"Repeated pattern:
keep valid scores
reject suspicious scores
reduce what remains to one total"

Object subclass: ScoreTools [
    ScoreTools class >> totalOfCleanScores: scores [
        | passing cleaned |
        passing := scores select: [ :each | each >= 50 ].
        cleaned := passing reject: [ :each | each > 100 ].
        ^ cleaned inject: 0 into: [ :total :each | total + each ]
    ]
]

| scores cleanedTotal |

scores := #(20 55 70 101 85 49 100 200).
cleanedTotal := ScoreTools totalOfCleanScores: scores.

'cleaned total:' printNl.
cleanedTotal printNl.
