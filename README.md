# Playoff_Draft
Custom Draft for NHL Playoffs

This application is to run/manage a custom playoff draft set-up which is detailed below.

It runs on a Flask Framework to generate a localhost (or if you wanted to port to website).


## Rules For Covid Cup -- How the draft works

### Play In Round

Pick the winner from each series and the games, and the games you think it will take (3, 4, or 5)

If you pick the correct team to win, you will have 3 points for that match up, but will lose 1 points from that 5 for every game you are off from the final result.

example) Vancouver vs Minnesota
pick: Vancouver in 5
result: Vancouver in 3
final points: 1

3 points for correct pick - 2 points (2 games x 1 points) = 1

total points available = 24

### Round Robin

Select the standings when round robin is completed (1st, 2nd, 3rd, and 4th for each conference)

Picking correct team in correct place - 1 point

Total points available = 8

### Round 1 - 3

Same Rules as Play In, pick the winner and the number of games it will take

Round 1: Winning Team + games = 7 points (-1 point for each game off final result)
Round 2: Winning Team + games = 14 points (-2 point for each game off final result)
Round 3: Winning Team + games = 21 points (-3 point for each game off final result)

Total points available = (Round 1: 56), (Round 2: 56), (Round 3: 42)

### Stanley Cup Final

Choose the winner of each game in the 7 game series

Picking the winner of each game = 5 points

Even if you think its a sweep, you can still fill in games 5 - 7 with winner

Total points available = 35 points

### Player Totals

Pick 2 players before start of playoffs

Add their point total to your final prediction total for final tally.

Goals are worth 1 point
Assists are worth 1 point
