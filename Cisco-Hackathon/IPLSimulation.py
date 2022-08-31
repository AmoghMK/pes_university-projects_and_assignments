
import pandas as pd
import random
import json
import math

df = pd.read_csv("schedule.csv")

final = df[56:60][:]
# print(final)
league = df[0:56][:]

def load_data_set(path):
    with open(path, "r") as fp:
        data = fp.read()
    try:
        l = json.loads(data)
        pvsp = {}
        for i in l:
            # print(type(i))
            pvsp[tuple(i["key"])] = i["value"]
    except ValueError:
        pvsp = {}
    return pvsp

def init():
    "Function to read all the files before hand and prepare appropriate data structures"
    clusterpvsp = load_data_set("clusteredplayervsplayer2k18.json")
    players = pd.read_csv("players.csv")
    venuebias = pd.read_csv("venbias.csv")
    rain_factor = pd.read_csv("rainbias.csv")
    batsman = pd.read_csv("batsmanonly.csv")
    bowler = pd.read_csv("bowlers.csv")
    return (clusterpvsp, players, venuebias, rain_factor, batsman, bowler)

# Function to print initial commentry before match for debugging purpose.
def welcome_comments(match):
    print("Welcome to the Game " +str(match["Sl no"]) +" which is played between " +str(match["Team 1"]) +
          " and " +str(match["Team 2"]) + " at "+str(match["Venue"]) + " on "+ str(match["Date"]) +" " + str(match["Day"]) + "!")

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

def pick(l, prob_list):
    cuml_prob = [0]
    for i in range(0, len(prob_list)):
        cuml_prob.append(cuml_prob[i]+prob_list[i])
    # print(cuml_prob)
    r = random.random()
    upper_bound = max(cuml_prob)
    while r > upper_bound:
        r = random.random()
    lower_bound = min(cuml_prob)
    # print("r:",r)
    for i in cuml_prob:
        if r < i:
            upper_bound = min(i, upper_bound)
        if r > i:
            lower_bound = max(i, lower_bound)
    lower_index = cuml_prob.index(lower_bound)
    upper_index = cuml_prob.index(upper_bound)
    # print(lower_index,upper_index)
    return l[lower_index]

#debug for testing
pick([0,1,2,3,6],[0.5,0.3,0.05,0.1,0.05])

def simulate_wicket(name, prob):
    if(prob[name] < 0.5):
        return 1
    return 0

def simulate_extras(key):
    global cprob
    r = random.random()
    if r < cprob[key]["extras"]:
        return 1
    return 0

def simulate_run(key,current_pair, mode = 1):
    global cprob
    if mode == -1:
        # Run out simulation
        prob_list = [cprob[key]["zeroes"], cprob[key]["ones"], cprob[key]["twos"], cprob[key]["threes"]]
        run = pick([0,1,2,3], prob_list)
        run -= 1
        if run == -1:
            run = 0
        if run == 1:
            current_pair[0], current_pair[1] = current_pair[1], current_pair[0]
    elif mode == 0:
        # Leg Bye simulation
        prob_list = [cprob[key]["zeroes"], cprob[key]["ones"], cprob[key]["fours"]]
        run = pick([0,1,4], prob_list)
        if run == 1:
            current_pair[0], current_pair[1] = current_pair[1], current_pair[0]
    else:
        # Normal Simulation
        prob_list = [cprob[key]["zeroes"], cprob[key]["ones"], cprob[key]["twos"], cprob[key]["threes"], 
                     cprob[key]["fours"], cprob[key]["sixes"]]
        run = pick([0,1,2,3,4,6], prob_list)
        if run%2 == 1:
            current_pair[0], current_pair[1] = current_pair[1], current_pair[0]
    return (run, current_pair)

def simulate_ball(batsman_name, bowler_name, current_pair, prob):
    batcluster = int(batsman[batsman["Player"] == batsman_name]["cluster"])
    bowlcluster = int(bowler[bowler["Player"] == bowler_name]["cluster"])
    key = (batcluster, bowlcluster)
    taken = simulate_wicket(batsman_name, prob)
    extras = simulate_extras(key)
    if(taken == 1 and extras == 0):
        run = 0
        ran = random.randint(0,3)
        if(ran == 0):
            # Run out Simulate run also but with mode runout
            run, current_pair = simulate_run(key,current_pair,-1)
        return (run, taken, 0, current_pair)
    elif(extras > 0):
        taken = 0
        run, current_pair = simulate_run(key,current_pair, 0)
        if run == 1 or run == 4:
            t = random.random()
            if(t < 0.5):
                # Legbye
                extras = run
            else:
                # Wide
                extras += run
        return(run, taken, extras, current_pair)
    run, current_pair = simulate_run(key,current_pair)
    return (run, taken, extras, current_pair)

def get_batsman_name(runs, batlist,  wicket_taken, current_pair, ball, bat_pos, batsman_prob):
    if(wicket_taken == 1):
        bat_pos += 1
        # print("bat_pos", bat_pos)
        current_pair[0] = batlist[bat_pos] 
    if(runs == 6 or runs == 4):
        batsman_prob[current_pair[0]] += 0.025
    if(ball % 6 == 0):
        current_pair[0], current_pair[1] = current_pair[1], current_pair[0]
    return (current_pair[0],bat_pos)

def get_bowler_name(ball, bowllist, current_bowler, bowler_stat):
    if ball % 6 == 0:
        r = random.randint(0,4)
        if bowllist[r] in bowler_stat:
            if bowler_stat[bowllist[r]]["over"] == 4:
                t = random.randint(0,4)
                while(t == r):
                    t = random.randint(0,4)
                r = t
            return bowllist[r]  
    return current_bowler
        
def update_probability(batsman_name, bowler_name, batsman_prob):
    global cprob
    global batsman
    global bowler
    # Find to which cluster the batsman and bowler belongs
    bat_cluster = int(batsman[batsman["Player"] == batsman_name]["cluster"])
    # print(batsman_name, bat_cluster)
    ball_cluster = int(bowler[bowler["Player"] == bowler_name]["cluster"])
    # print(bowler_name, ball_cluster)
    key = (bat_cluster,ball_cluster)
    batsman_prob[batsman_name] *= (1-cprob[key]["dissmissals"])

def initialize(batteam, bowlteam):
    dic1 = {}
    dic2 = {}
    dic3 = {}
    global players
    global bowler
    batting_order = list(players[players["Team"]==util[batteam]]["Player"])
    bowllist = list(bowler[bowler["Team"]==util[bowlteam]]["Player"])
    for i in batting_order:
        dic1[i] = {"runs":0}
        dic3[i] = 1
    for i in bowllist:
        dic2[i] = {"runs":0,"extras":0,"wickets":0, "over":0}
    return (dic3,dic1,dic2, batting_order, bowllist)

def update_batsman_details(batscore, name, statlist):
    run = sum([i[0] for i in statlist])
    batscore[name]["runs"] += run
    
def update_bowler_details(bowlerstat, name, over, statlist):
    run = sum([i[0] for i in statlist])
    extras = sum([i[2] for i in statlist])
    wicket = sum([i[1] for i in statlist])
    bowlerstat[name]["runs"] += run
    bowlerstat[name]["extras"] += extras
    bowlerstat[name]["wickets"] += wicket
    bowlerstat[name]["over"] += over

# Function to simulate the innings
def simulate_innings(batteam, bowlteam, match, over = 20, target_ach = 0):
    # decide number of balls
    batsman_prob , batsman_score, bowler_stat, batlist, bowllist = initialize(batteam, bowlteam)
    print(batlist)
    num_ball = over*6
    current_over = 0
    current_ball = 0
    total_score = 0
    runs = 0
    current_pair = [batlist[0], batlist[1]]
    bat_pos = 1
    current_bowler = bowllist[random.randint(0,4)]
    wicket = 0
    l = []
    runs = 0
    wicket_taken = 0
    while(current_over != over):
        # Simulate that delivery
        #print("Current Over:", current_over)
        #print("Current Ball:", current_ball)
        batsman_name, bat_pos = get_batsman_name(runs, batlist, wicket_taken, current_pair, current_ball, bat_pos, batsman_prob)
        bowler_name = get_bowler_name(current_ball, bowllist, current_bowler, bowler_stat)
        runs, wicket_taken, extras, current_pair = simulate_ball(batsman_name, bowler_name, current_pair, batsman_prob)
        l.append([runs, wicket_taken, extras])
        if(extras > 0):
            current_ball -= 1
        update_probability(batsman_name, bowler_name, batsman_prob)
        total_score += runs
        wicket += wicket_taken
        # print("wicket:",wicket)
        if(current_ball > 0 and current_ball % 6 == 0 ):
            current_over += 1
            current_ball = 0
            update_bowler_details(bowler_stat, bowler_name,1, l)
            update_batsman_details(batsman_score, batsman_name, l)
            l = []
        else:
            current_ball += 1
        if(wicket == 10):
            # Finish innings
            if current_ball == 6:
                over = 1
            else:
                over = current_ball/10
            update_bowler_details(bowler_stat, bowler_name,over, l)
            update_batsman_details(batsman_score, batsman_name, l)
            break
        if(target_ach > 0):
            if(total_score > target_ach):
                if current_ball == 6:
                    over = 1
                else:
                    over = current_ball/10
                update_bowler_details(bowler_stat, bowler_name,over, l)
                update_batsman_details(batsman_score, batsman_name, l)
                break
        # print(total_score)
            # Update scorecard
    # write the details for orange and purple cap
    print(bowler_stat)
    print(batsman_score)
    global o_cap
    global p_cap
    for i in batsman_score:
        if i in o_cap:
            o_cap[i] += batsman_score[i]["runs"]
        else:
            o_cap[i] = batsman_score[i]["runs"]
    for i in bowler_stat:
        if i in p_cap:
            p_cap[i] += bowler_stat[i]["wickets"]
        else:
            p_cap[i] = bowler_stat[i]["wickets"]
    return total_score

def update_points_table(winner, loser, team1, team2):
    global pointstabledf
    if winner == None and loser == None:
        pointstabledf[util[team1]]["Tie"] += 1
        pointstabledf[util[team2]]["Tie"] += 1
        pointstabledf[util[team1]]["Points"] += 1
        pointstabledf[util[team2]]["Points"] += 1
    else:
        pointstabledf[util[winner]]["Wins"] += 1
        pointstabledf[util[winner]]["Points"] += 2
        pointstabledf[util[loser]]["Loss"] += 1
    print("Points Table updated")

# Function to simulate the match
def simulate_match(match, venbias, rainaffected, rep = 1):
    global d_net_rr
    if rainaffected:
        update_points_table(None, None, match["Team 1"], match["Team 2"])
        return(None,None)
    winner = loser = ""
    # Simulate the coin toss
    batteam, bowlteam = simulate_coin_toss(match["Team 1"], match["Team 2"])
    # First Innings
    target = simulate_innings(batteam, bowlteam, match)
    target += venbias*target
    target = math.floor(target)
    if(not rainaffected):
        d_net_rr[batteam]["Runs_scored"] += target
        d_net_rr[bowlteam]["Runs_given"] += target
        d_net_rr[bowlteam]["match"] += 1
    # Second Innings
    final_score = simulate_innings(bowlteam, batteam, match, target_ach = target)
    if(not rainaffected):
        d_net_rr[bowlteam]["Runs_scored"] += final_score
        d_net_rr[batteam]["Runs_given"] += final_score
        d_net_rr[batteam]["match"] += 1
    print("Target Score:", target)    
    print("Final_score:",final_score)
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
        target = simulate_innings(batteam, bowlteam, match, 1)
        # Second Innings
        final_score = simulate_innings(batteam, bowlteam, match, 1)
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
    return (winner, loser)

# Simulation Begins
clusteredpvsp, players, venuebias, rain_factor, batsman, bowler = init()
cprob = {}
for i in clusteredpvsp:
    cprob[i] = {"zeroes":clusteredpvsp[i]["zeroes"]/clusteredpvsp[i]["balls"], 
                "ones":clusteredpvsp[i]["ones"]/clusteredpvsp[i]["balls"],
               "twos":clusteredpvsp[i]["twos"]/clusteredpvsp[i]["balls"],
               "threes":clusteredpvsp[i]["threes"]/clusteredpvsp[i]["balls"],
               "fours":clusteredpvsp[i]["fours"]/clusteredpvsp[i]["balls"],
               "sixes":clusteredpvsp[i]["sixes"]/clusteredpvsp[i]["balls"],
               "extras":clusteredpvsp[i]["extras"]/clusteredpvsp[i]["balls"],
               "dissmissals":clusteredpvsp[i]["dissmissals"]/clusteredpvsp[i]["balls"],
               }

d_net_rr = {"CSK": {"Runs_given":0, "Runs_scored":0, "match":0},
            "MI": {"Runs_given":0, "Runs_scored":0, "match":0},
            "RCB": {"Runs_given":0, "Runs_scored":0, "match":0},
            "DD": {"Runs_given":0, "Runs_scored":0, "match":0},
            "SRH": {"Runs_given":0, "Runs_scored":0, "match":0},
            "KKR": {"Runs_given":0, "Runs_scored":0, "match":0},
            "KXP": {"Runs_given":0, "Runs_scored":0, "match":0},
            "RR": {"Runs_given":0, "Runs_scored":0, "match":0}}


util = {}
util["MI"] = "Mumbai Indians"
util["CSK"] = "Chennai Super Kings"
util["RR"] = "Rajasthan Royals"
util["RCB"] = "Royal Challengers Bangalore"
util["DD"] = "Delhi Daredevils"
util["SRH"] = "Sunrisers Hyderabad"
util["KXP"] = "Kings XI Punjab"
util["KKR"] = "Kolkata Knight Riders"
pointstabledf = {}
for i in list(util.values()):
    pointstabledf[i] = {"Wins":0, "Loss":0,"Tie":0, "Points":0, "Net_run_rate":0}
p_cap = {}
o_cap = {}
for i in range(0,56):
    # Interest is each row
    match = dict(league.loc[i])
    welcome_comments(match)
    r = random.random()
    print(r)
    rainaffected=  False
    # print(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"])
    if r < float(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"]): 
        rainaffected = True
    # Call to match simulate for simulating the match
    winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], rainaffected)
    print("Winner of match "+str(match["Sl no"]) + " is", winner)
    print(d_net_rr)
    '''
    if i == 27:
        for i in d_net_rr:
            pointstabledf[util[i]]["Net_run_rate"] = (d_net_rr[i]["Runs_scored"] - d_net_rr[i]["Runs_given"])/(d_net_rr[i]["match"]*20)
        df = pd.DataFrame.from_dict(pointstabledf, orient='index')
        df.reset_index(level=[], inplace=True)
        df.columns = ['Team', 'Wins','Loss','Tie','Points','Net_Run_Rate']
        for i in range(0,8):
            if df.loc[i]["Team"] == "Delhi Daredevils":
                df.at[i, "Team Code"] = "DD"
            elif df.loc[i]["Team"] == "Mumbai Indians":
                df.at[i, "Team Code"] = "MI"
            elif df.loc[i]["Team"] == "Chennai Super Kings":
                df.at[i, "Team Code"] = "CSK"
            elif df.loc[i]["Team"] == "Kolkata Knight Riders":
                df.at[i, "Team Code"] = "KKR"
            elif df.loc[i]["Team"] == "Rajasthan Royals":
                df.at[i, "Team Code"] = "RR"
            elif df.loc[i]["Team"] == "Sunrisers Hyderabad":
                df.at[i, "Team Code"] = "SRH"
            elif df.loc[i]["Team"] == "Royal Challengers Bangalore":
                df.at[i, "Team Code"] = "RCB"
            elif df.loc[i]["Team"] == "Kings XI Punjab":
                df.at[i, "Team Code"] = "KXP"
        df.sort_values(by = ['Points', 'Net_Run_Rate'],axis = 0,ascending=[False, False], inplace = True)
        df = df.reset_index(drop=True)
        df.to_csv("midseasonpointstable.csv")
    # break
for i in d_net_rr:
    pointstabledf[util[i]]["Net_run_rate"] = (d_net_rr[i]["Runs_scored"] - d_net_rr[i]["Runs_given"])/(d_net_rr[i]["match"]*20)
print(pointstabledf)

df = pd.DataFrame.from_dict(pointstabledf, orient='index')
df.reset_index(level=0, inplace=True)
df.columns = ['Team', 'Wins','Loss','Tie','Points','Net_Run_Rate']
# df["Team Code"] = "NA"
for i in range(0,8):
    if df.loc[i]["Team"] == "Delhi Daredevils":
        df.at[i, "Team Code"] = "DD"
    elif df.loc[i]["Team"] == "Mumbai Indians":
        df.at[i, "Team Code"] = "MI"
    elif df.loc[i]["Team"] == "Chennai Super Kings":
        df.at[i, "Team Code"] = "CSK"
    elif df.loc[i]["Team"] == "Kolkata Knight Riders":
        df.at[i, "Team Code"] = "KKR"
    elif df.loc[i]["Team"] == "Rajasthan Royals":
        df.at[i, "Team Code"] = "RR"
    elif df.loc[i]["Team"] == "Sunrisers Hyderabad":
        df.at[i, "Team Code"] = "SRH"
    elif df.loc[i]["Team"] == "Royal Challengers Bangalore":
        df.at[i, "Team Code"] = "RCB"
    elif df.loc[i]["Team"] == "Kings XI Punjab":
        df.at[i, "Team Code"] = "KXP"
df.sort_values(by = ['Points', 'Net_Run_Rate'],axis = 0,ascending=[False, False], inplace = True)
df = df.reset_index(drop=True)
df.to_csv("pointstable.csv")
# Open the points table file and select top 4 teams to decide the last 4 matches
pointstable = pd.read_csv("pointstable.csv")
pointstable.sort_values(by = ['Points'],axis = 0,ascending=False, inplace = True)
pointstable = pointstable.reset_index(drop=True)
print(pointstable)
'''
# # Qualifier 1
final.at[56, 'Team 1'] = pointstable.loc[0]["Team Code"]
final.at[56, 'Team 2'] = pointstable.loc[1]["Team Code"]
match = final.loc[56]
welcome_comments(match)
r = random.random()
print(r)
rainaffected=  False
# print(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"])
if r/10 < float(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"]): 
    rainaffected = True
# Call to match simulate for simulating the match
winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], rainaffected)
print("Winner of match "+str(match["Sl no"]) + " is", winner)
final.at[58, "Team 1"] = loser
final.at[59, "Team 1"] = winner
# Eliminator
final.at[57, 'Team 1'] = pointstable.loc[2]["Team Code"]
final.at[57, 'Team 2'] = pointstable.loc[3]["Team Code"]
final.at[57, "Venue"] = "Bengaluru"
match = final.loc[57]
welcome_comments(match)
r = random.random()
print(r)
rainaffected=  False
# print(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"])
if r/10 < float(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"]): 
    rainaffected = False
# Call to match simulate for simulating the match
winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], rainaffected)
print("Winner of match "+str(match["Sl no"]) + " is", winner)
final.at[58, "Team 2"] = winner
# Qualifier 2
final.at[58, "Venue"] = "Chennai"
match = final.loc[58]
welcome_comments(match)
r = random.random()
print(r)
rainaffected=  False
# print(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"])
if r/10 < float(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"]): 
    rainaffected = True
# Call to match simulate for simulating the match
winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], rainaffected)
print("Winner of match "+str(match["Sl no"]) + " is", winner)
final.at[59, "Team 2"] = winner
# Final
match = final.loc[59]
welcome_comments(match)
r = random.random()
print(r)
rainaffected=  False
# print(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"])
if r/10 < float(rain_factor[rain_factor["Place"] == match["Venue"]]["rain_prob"]): 
    rainaffected = True
# Call to match simulate for simulating the match
winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], rainaffected)
print("Winner of match "+str(match["Sl no"]) + " is", winner)
print("The winner of the IPL 2018 season 11 is", winner)
odf = pd.DataFrame.from_dict(o_cap, orient='index')
odf.reset_index(level=0, inplace=True, col_fill='Team')
odf.columns = ['Player','Runs']
odf.sort_values(by=["Runs"], ascending=False, inplace=True)
odf = odf.reset_index(drop=True)
odf.to_csv("orangecap.csv")
pdf = pd.DataFrame.from_dict(p_cap, orient='index')
pdf.reset_index(level=0, inplace=True, col_fill='Team')
pdf.columns = ['Player','Wickets']
pdf.sort_values(by=["Wickets"], ascending=False, inplace=True)
pdf = pdf.reset_index(drop=True)
pdf.to_csv("purplecap.csv")
print("The orange cap winner is", odf.loc[0]["Player"], odf.loc[0]["Runs"])
print("The purple cap winner is", pdf.loc[0]["Player"], pdf.loc[0]["Wickets"])

# # Display points table for midseason
print("MidSeason Points Table")
midseason = pd.read_csv("midseasonpointstable.csv")
print(midseason)
# Display points table for full season
print("Full Season Points Table")
print(pointstable)

'''
match = dict(league.loc[1])
winner, loser = simulate_match(match, venuebias[venuebias["Place"] == match["Venue"]]["bias"], False)
print(winner)
print(loser)
'''
