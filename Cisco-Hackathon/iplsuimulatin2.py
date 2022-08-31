# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 06:40:38 2018

@author: Amogh
"""

import pandas as pd
import random

df = pd.read_csv("schedule.csv")
final = df[56:60][:]
league = df[0:56][:]

def init():
    "Function to read all the files before hand and prepare appropriate data structures"
    pass

# Function to print initial commentry before match for debugging purpose.
def welcome_comments(match):
    print("Welcome to the Game " +str(i+1) +" which is played between " + match["Team 1"] +
          " and " + match["Team 2"] + " at "+match["Venue"] + " on "+ match["Date"] +" " + match["Day"] + "!")
    
# Function to simulate Coin Toss
def simulate_coin_toss(team1, team2):
    participants = (team1, team2)
    # Randomly choose one from tuple
    randindex = random.randint(0,100)
    # Winner get choice
    winner = randindex%2
    loser = 0 if winner == 1 else 1
    choice = ("Batting", "Bowling")
    randindex = random.randint(0,100)
    if randindex%2 == 0:
        return (participants[winner], participants[loser])
    return (participants[loser], participants[winner])
# Uncomment to test the function
# print(simulate_coin_toss("MI","CSK"))

# Function to simulate the innings
def simulate_innings(batteam, bowlteam, match, o_cap, p_cap, over = 20):
    # decide number of balls
    num_ball = over*6
    for i in range(0, num_ball):
        # Simulate that delivery
        pass
    pass

# Function to simulate the match
def simulate_match(match, rep = 1):
    winner = loser = ""
    # Simulate the coin toss
    batteam, bowlteam = simulate_coin_toss(match["Team 1"], match["Team 2"])
    # First Innings
    target = simulate_innings(batteam, bowlteam, match, o_cap, p_cap)
    # Second Innings
    final_score = simulate_innings(batteam, bowlteam, match, o_cap, p_cap)
    # Decide the winner and loser
    if(final_score > target):
        winner = bowlteam
        loser = batteam
    elif final_score < target:
        winner = batteam
        loser = bowlteam
    else:
        # Toss for Super over
        batteam, bowlteam = simulate_coin_toss(match["Team 1"], match["Team 2"])
        # First Innings
        target = simulate_innings(batteam, bowlteam, match, o_cap, p_cap, 1)
        # Second Innings
        final_score = simulate_innings(batteam, bowlteam, match, o_cap, p_cap, 1)
        # Decision of match
        if(final_score > target):
            winner = bowlteam
            loser = batteam
        elif final_score < target:
            winner = batteam
            loser = bowlteam
        else:
            winner = None
            loser = None
    # Update Points Table
    update_points_table(winner, loser, match["Team 1"], match["Team 2"])
    # Update Purple Cap Contenders
    update_purple_cap(p_cap)
    # Update orange Cap Contenders
    update_orange_cap(o_cap)
    return (winner, loser)
    pass

# Simulation Begins
for i in range(0,56):
    # Interest is each row
    match = dict(league.loc[i])
    welcome_comments(match)
    # Call to match simulate for simulating the match
    winner, loser = simulate_match(match)
    print("Winner of match "+str(match["Sl no"]) + " is", winner)
# Open the points table file and select top 4 teams to decide the last 4 matches
pointstable = pd.read_csv("../pointstable.csv")
# Qualifier 1
match = final.loc[56]
match["Team 1"] = pointstable.loc[0]["Team"]
match["Team 2"] = pointstable.loc[1]["Team"]
welcome_comments(match)
winner, loser = simulate_match(match)
final.loc[58]["Team 1"] = loser
final.loc[59]["Team 1"] = winner
# Eliminator
match = final.loc[57]
match["Team 1"] = pointstable.loc[2]["Team"]
match["Team 2"] = pointstable.loc[3]["Team"]
match["Venue"] = "Bangalore"
welcome_comments(match)
winner, loser = simulate_match(match)
final.loc[58]["Team 2"] = winner
# Qualifier 2
match = final.loc[58]
welcome_comments(match)
winner, loser = simulate_match(match)
final.loc[59]["Team 2"] = winner
# Final
match = final.loc[59]
welcome_comments(match)
winner, loser = simulate_match(match, rep=3)
print("The winner of the IPL 2018 season 11 is", winner)
print("The orange cap winner is", get_orange_cap())
print("The purple cap winner is", get_purple_cap())

# Display points table for midseason
midseason = pd.read_csv("../midseason.csv")
print(midseason)
# Display points table for full season
print(pointstable)

