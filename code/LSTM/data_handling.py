import csv
import torch

player_names = []

position_categories = []
squad_categories = []
league_categories = []


# Open the CSV file for reading
for i in range(1,9):

    csv_file_path = f'{i}.csv'
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Loop through each row in the CSV file
        for row in csv_reader:
            # Print the entry in the first column
            if row[1] not in player_names:
                player_names.append(row[1])

            if row[3] not in position_categories:
                position_categories.append(row[3])

            if row[4] not in squad_categories:
                squad_categories.append(row[4])

            if row[5] not in league_categories:
                league_categories.append(row[5])

player_names.remove("Player")
player_names.remove("Unnamed: 1_level_0")

position_categories.remove("Pos")
position_categories.remove("Unnamed: 3_level_0")

squad_categories.remove("Squad")
squad_categories.remove("Unnamed: 4_level_0")

league_categories.remove("Comp")
league_categories.remove("Unnamed: 5_level_0")

#print(position_categories)
#print(league_categories)
#print(squad_categories)

player_dictionary = {}


for i in range(1,9):
    csv_file_path = f"{i}.csv"
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        for _ in range(2):
            next(csv_reader)
        # Loop through each row in the CSV file
        #count = 0
        for row in csv_reader:
            if row[1] == "Player":
                continue
            
            if row[1] not in player_dictionary:
                player_dictionary[row[1]] = []

            #if count == 3:
                #break
            categorical_player_data_vector = [row[3], row[4], row[5]]
            one_hot_encoded = [
                torch.tensor([
                    int(category == element) for category in category_list
                ]) for element, category_list in zip(categorical_player_data_vector, [position_categories, squad_categories, league_categories])
            ]

            # Concatenate the one-hot encoded tensors to get the final encoding
            one_hot_encoded = torch.cat(one_hot_encoded)


            if any(field == '' for field in row):
                # Skip this row if any field is empty
                continue
            else:
                numerical_player_data_vector = torch.tensor([int(value) if value.isdigit() else float(value) for value in row[6:25]])
                final_player_data_vector = torch.cat((one_hot_encoded, numerical_player_data_vector))

            player_dictionary[row[1]].append(final_player_data_vector)
            # print(final_player_data_vector)
            #count += 1



clubs_list = []
for i in range(1,9):
    csv_file_path = f"{i}.csv"
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[4] not in clubs_list:
                clubs_list.append(row[4])

clubs_list.remove('Unnamed: 4_level_0')
clubs_list.remove('Squad')


#print(f"\n\nNUMBER OF CLUBS: {len(clubs_list)}")
#print(clubs_list)

# print(player_dictionary)
print(len(player_dictionary["Eden Hazard"][0]))

#torch.save(player_dictionary, 'player_dictionary.pt')
