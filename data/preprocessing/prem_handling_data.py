import json
import torch
import time

with open('dict.json', 'r') as f:
    loaded_dict = json.load(f)

with open('matchweek_dictionary.json', 'r') as q:
    matchweek_dictionary = json.load(q)

with open('missing_matchweeks_dictionary.json', 'r') as m:
    missing_matchweeks_dictionary = json.load(m)

with open('raw_prem_dictionary.json', 'r') as h:
    raw_prem_dictionary = json.load(h)


list_of_positions = ['FW', 'RM', 'GK', 'DM', 'RW', 'FW,LW', 'LW', 'CB', 'CM', 'RM,CB,LM', 'LB', 'LM', 'AM', 'WB', 'RB', 'FW,CM', 'CM,DM', 'RM,CM', 'LW,AM', 'FW,AM', 'CM,RM', 'LW,FW', 'FW,RW', 'CB,CM', 'DM,CM', 'AM,LW', 'LM,FW', 'LW,FW,RW', 'RW,RM,AM', 'CM,RM,AM', 'LB,CB', 'LM,LW', 'DM,RM', 'CM,RW', 'WB,RB', 'AM,FW', 'RW,FW', 'RW,RB', 'RW,RM', 'RM,LM', 'CB,RB', 'RW,LB,WB', 'LW,LM', 'CM,LB', 'RW,AM', 'RW,WB', 'LW,RW', 'RW,CM', 'RM,CB', 'LM,RM', 'CM,LM,DM', 'WB,LB', 'CM,FW', 'RW,LW', 'LM,CM', 'RB,CB', 'CM,LM', 'RM,AM', 'FW,DM', 'LM,RW', 'LB,LM', 'RB,RM', 'DM,AM', 'AM,LM', 'RW,LM', 'LW,LB']

teams = ["Southampton", "Leeds United", "Leicester City", "Everton", "Nott'ham Forest", "Bournemouth",  "West Ham", "Wolves", "Chelsea", "Crystal Palace", "Fulham", "Brentford", "Tottenham", "Aston Villa", "Brighton", "Liverpool", "Newcastle Utd", "Manchester Utd", "Arsenal", "Manchester City"]

win_draw_loss = ["W", "L", "D"]


removed = []
for key in loaded_dict:
    if len(loaded_dict[key]) == 0:
        removed.append(key)
        continue
    if len(loaded_dict[key][0]) < 32:
        removed.append(key)

    if loaded_dict[key][0][5] == "GK":
        removed.append(key)


for remove in removed:
    del(loaded_dict[remove])
    #print(remove)

del(loaded_dict["Mykhailo-Mudryk"]) # problem with the ukranian premier league being confused with english premier league

one_hot_encoded_categorical_dict = {}

#b=0
for key in loaded_dict:
    '''if b == 1:
        break'''
    
    one_hot_encoded_categorical_dict[key] = []
    #print(len(loaded_dict[key]))

    for i in range(len(loaded_dict[key])):
        #print(loaded_dict[key][i][3])
    

        #b += 1
        
        if loaded_dict[key][i][5] == "On matchday squad, but did not play":

                home_or_away = torch.tensor([0])
                #print(home_or_away)
                if loaded_dict[key][i][0] == "Home":
                    home_or_away = torch.tensor([1])
                #print(home_or_away)

                start_or_bench = torch.tensor([0])
                if loaded_dict[key][i][4] == "Y" or loaded_dict[key][i][4] == "Y*":
                    start_or_bench = torch.tensor([1])

                categorical_player_data_vector = [loaded_dict[key][i][1][0], loaded_dict[key][i][2], loaded_dict[key][i][3]]
                one_hot_encoded = [
                            torch.tensor([
                                int(category == element) for category in category_list
                            ]) for element, category_list in zip(categorical_player_data_vector, [win_draw_loss, teams, teams])
                        ]
                
                zero_vect = torch.zeros(66)
                one_hot_encoded.append(zero_vect)
                one_hot_encoded.insert(0, home_or_away)
                one_hot_encoded.insert(2, start_or_bench)



                second_zero_vect = torch.zeros(26)

                one_hot_encoded.append(second_zero_vect)

                #print(one_hot_encoded)
                concatenated_one_hot_categorical = torch.cat(one_hot_encoded)
                #print(concatenated_one_hot_categorical)

                one_hot_encoded_categorical_dict[key].append(concatenated_one_hot_categorical)


        elif loaded_dict[key][i][5] != "On matchday squad, but did not play":
            
            home_or_away = torch.tensor([0])
            #print(home_or_away)
            if loaded_dict[key][i][0] == "Home":
                home_or_away = torch.tensor([1])
            #print(home_or_away)

            start_or_bench = torch.tensor([0])
            if loaded_dict[key][i][4] == "Y" or loaded_dict[key][i][4] == "Y*":
                start_or_bench = torch.tensor([1])

            categorical_player_data_vector = [loaded_dict[key][i][1][0], loaded_dict[key][i][2], loaded_dict[key][i][3], loaded_dict[key][i][5]]
            one_hot_encoded = [
                        torch.tensor([
                            int(category == element) for category in category_list
                        ]) for element, category_list in zip(categorical_player_data_vector, [win_draw_loss, teams, teams, list_of_positions])
                    ]

            numerical_match_data_vector = loaded_dict[key][i][-26:]
            numerical_match_data_vector = [float(element) for element in numerical_match_data_vector]


            one_hot_encoded.insert(0, home_or_away)
            one_hot_encoded.insert(2, start_or_bench)

            one_hot_encoded.append(torch.tensor(numerical_match_data_vector))
            #print(one_hot_encoded)


            concatenated_one_hot_categorical = torch.cat(one_hot_encoded)
            #print(concatenated_one_hot_categorical)
            

            one_hot_encoded_categorical_dict[key].append(concatenated_one_hot_categorical)
            #print(concatenated_one_hot_categorical)
#print(one_hot_encoded_categorical_dict["Cristiano-Ronaldo"])



matchweek_numbers_in_squad = {}

for player in one_hot_encoded_categorical_dict:
    matchweek_numbers_in_squad[player] = []
    for i in range(len(one_hot_encoded_categorical_dict[player])):
        matchweek_numbers_in_squad[player].append(int(raw_prem_dictionary[player][i][0].split()[1]))

# matchweek_numbers_in_squad is a dictionary where the keys are player names and the values are lists in which they were in the squad
# missing_matchweeks_dictionary is a dictionary where the keys are player names and the values are lists in which they were NOT in the squad
# matchweek_dictionary is a dictionary where the keys are team names and the values are lists with all the matchweeks in chronological order

prem_FINAL_dictionary = {}
for key in one_hot_encoded_categorical_dict:
    
    #########################################
    prem_FINAL_dictionary[key] = []
    for i in range(38):
        prem_FINAL_dictionary[key].append("hello")
    #########################################

for player in prem_FINAL_dictionary:
    for i in range(len(loaded_dict[player])):
        chrono_for_this_match = matchweek_dictionary[loaded_dict[player][i][2]]
        
        for num in missing_matchweeks_dictionary[player]:
            #print(f"Adding the following tensor to match slot {chrono_for_this_match.index(num)} for {player}: {torch.zeros(137)}")
            #time.sleep(10)
            prem_FINAL_dictionary[player][chrono_for_this_match.index(num)] = 0

        for num in matchweek_numbers_in_squad[player]:
            #print(f"Adding the following tensor to match slot {chrono_for_this_match.index(num)} for {player}: {one_hot_encoded_categorical_dict[player][num]}")
            #time.sleep(10)
            prem_FINAL_dictionary[player][chrono_for_this_match.index(num)] = 1




for player in prem_FINAL_dictionary:
    shorty_counter = 0
    for i in range(38):
        
        if prem_FINAL_dictionary[player][i] == 1:
            prem_FINAL_dictionary[player][i] = one_hot_encoded_categorical_dict[player][shorty_counter]
            shorty_counter += 1


        elif prem_FINAL_dictionary[player][i] == 0:
            prem_FINAL_dictionary[player][i] = torch.zeros(137)

torch.save(prem_FINAL_dictionary, "prem_FINAL_dictionary")





