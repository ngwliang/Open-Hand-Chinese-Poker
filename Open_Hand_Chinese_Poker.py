
# coding: utf-8

# In[2]:
from selenium import webdriver
import xlsxwriter
import pandas as pd
import numpy as np
import time
import os
import itertools

## To record the game scores of Open Hand Chinese Poker ##

driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/Open-face_Chinese_poker")

# In[3]:

#formula Counting score for the 1st player#
def counting_score(player,round_scores):
    scoring_tup = (-6,-1,1,6)
    baseplayer = player[0]
    
    #getting the number of win, must be 0-4
    while True:
        print()
        print(player[0], "versus", player[1])
        baseplayer_win = get_int("enter number to suits " + baseplayer + " won: " )  #need to be an input
        if 0 <= baseplayer_win < len(scoring_tup) :
            break
        else:
            print("Invalid Value")
            continue
    
    win_score = scoring_tup[baseplayer_win]
   
    round_score = win_score + round_scores[player[0]] - round_scores[player[1]]
  
    return round_score


# In[4]:

# playing the game #
def play():
    global Totalscore_df
    # setting number of rounds #
    number_of_rounds = get_int("Input Number of rounds to be played: ")

    # Getting the round scores #
    for rounds in range(number_of_rounds):
        print ("round number " + str(rounds+1))
        for i in range(15):
            print("=", end='')
        print()

        #Getting Round Scores#
        RC_list = []
        for player in plyr_list:
            roundscore = get_int("Enter round score for " + player + ":" )
            RC_list.append(roundscore)

        RC_dict = dict(zip(plyr_list,RC_list))
        print()
        
        #Getting number of suits won#
        for matches in matchup:
            p1 = matches[0]
            p2 = matches[1]
        #Calculating scores#
            p1score = counting_score(matches,RC_dict)
            p2score = p1score * -1

        #storing scores
            Tscore_dict[p1] += p1score
            Tscore_dict[p2] += p2score

        Totalscore_df = Totalscore_df.append(Tscore_dict, ignore_index=True)

        print()
        print("round score:")
        print(Totalscore_df.iloc[-1])
        print()
        for i in range(15):
            print("=", end='')
        print()

    print("############")
    print()
    print("Final Score:")
    print(Totalscore_df)
    print()
    print("############")

        #writing scores to excel
    writer = pd.ExcelWriter("OHCPoker_Score.xlsx", engine = 'xlsxwriter')
    Totalscore_df.to_excel(writer, sheet_name = 'Sheet 1')
    writer.save()

def get_int(text):
    while True:
        try:
            tmp = int(input(text))
            break
        except(ValueError):
            continue
    return tmp

# Initializing lists and dict to record scores #
def init():
    plyr_list = []
    for i in range (1,4):
        plyr = input("Please input Player "+ str(i) + " initials:")
        plyr_list.append(plyr.upper())
        
    Tscore_dict = dict(zip(plyr_list,[0,0,0]))
    Totalscore_df = pd.DataFrame(columns = plyr_list)

    # setting the matchup order #
    matchup =list(itertools.combinations(plyr_list, 2))

    return plyr_list,Tscore_dict,Totalscore_df,matchup


# In[8]:
plyr_list,Tscore_dict,Totalscore_df,matchup = init()

Conti = True
while Conti:
    print("\n\n")
    user_input = input("'play' to start\n'reset' to reset scores and players\n'exit' to close\n")

    if user_input.lower() == "play":
        play()

    elif user_input.lower() == "reset":
        plyr_list,Tscore_dict,Totalscore_df,matchup = init()

    elif user_input.lower() == "exit":
        Conti = False

    else:
        print("\nOops... Wrong Command")

print()
input("Bye Bye")
