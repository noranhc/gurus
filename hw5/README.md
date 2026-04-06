### Nora Cam & Aditya Shah

## How to run each file

From the `gurus/hw5/` folder, run each Smalltalk file with GNU Smalltalk using the following commands:
-  `gst hello.st`
-  `gst collections.st`
-  `gst miniDsl.st`

Each command prints program results to the terminal.

## What felt easy

What felt easy was using collection messages such as `do:`, `collect:`, `select:`, and `reject:` because they have simple behavior and formats. It also felt easy to wrap the cleanup logic in small helper functions with descriptive names, since the function style is similar to other programming languages I've seen before.

## What felt odd or surprising

The most odd or surprising part was the Smalltalk syntax, which uses a different order of operation (or execution?) than I'm used to. 

## Raw Steps vs. Tiny DSL

Raw steps show the mechanism: filter, reject, and total each part by hand.
A tiny DSL names the intent instead, such as `cleanScores:` or `totalOfCleanScores:`.
The raw version is useful for learning, because you can see every operation directly.
The DSL version is better for reuse or actual application. because the cleanup rule lives in one place.
