import torch
import random

dictio = torch.load("prem_FINAL_dictionary")

count = 0
for key in dictio:
	count += 1

#print(count)

data_set = []
target_set = []

# in the target_set, I want the 6 to 38 matches for each player which means I want the 5 to 37 index in the dictionary for each player.


# THIS PART BELOW IS WORKING AS INTENDED, I.E, it is creating a list called target_set which looks like [M6,M7,...,M38, M6_2, M7_2, ..., M38_2, ..., M6_n, ..., M38_n]
#######################################################################################################################################################################
for key in dictio:
	for i in range(5,38):
		target_set.append(dictio[key][i])

#print(target_set[34])
#######################################################################################################################################################################

target = []
for i in range(len(target_set)):
	current_tensor_categorical = target_set[i][:5]
	current_tensor_numerical = target_set[i][111:137]
	tensor = torch.cat((current_tensor_categorical, current_tensor_numerical))
	float_tensor = tensor.float()
	target.append(float_tensor)


print(len(target[0]))

#print(target[0])


# THIS PART BELOW WORKS AS INTENDED, I.E, it is creating a list called data_set which looks like [M1,M2,...M37, M1_2, M2_2, ..., M37_2, M1_n, ...,M37_n]
#########################################################################################################################################################
for key in dictio:
	for i in range(37):
		current_tensor = dictio[key][i]
		next_tensor = dictio[key][i+1]

		next_tensor_teams_and_position = next_tensor[5:111] # both teams + position
		tensor = torch.cat(((current_tensor, next_tensor_teams_and_position)))
		float_tensor = current_tensor.float()
		data_set.append(float_tensor)

print(len(data_set[0]))
print(data_set[0])
#print(data_set[74])
#########################################################################################################################################################



# THIS PART BELOW WORKS AS INTENDED, every 33 indecis in data per player and 37 matches per player
#########################################################################################################################################################
data = []
'''for i in range(len(target)):
	current_list = []
	for j in range(5):
		#current_list.append(data_set[i+j])
	#data.append(torch.stack(current_list))
		current_list.append(i+j)
	data.append(current_list)

print(data[33][0])

print(data_set[33])'''

w = 0
for player in dictio:
	for i in range(33):
		current_list = []
		for j in range(5):
			current_list.append(data_set[i+j+w])
		data.append(torch.stack(current_list))
	w += 37

#print(data[65][4])
#########################################################################################################################################################



DATA = []
for i in range(len(data)):
	DATA.append((data[i], target[i]))

# print(DATA[0])

# TO SHUFFLE PROPERLY: FIRST, MAKE AN ARRAY FOR EACH PLAYER WITH ALL THEIR ENTRIES IN DATA. SHUFFLE THAT ARRAY, AND THEN TAKE THE FIRST 24 AND PLACE THOSE IN TEST_DATA, NEXT

random.seed(1)
w=0 

train_set = []
test_set = []
val_set = []


for player in dictio:
	shuffled_player = []
	for i in range(33):
		shuffled_player.append(DATA[i+w])

	random.shuffle(shuffled_player)
	for j in range(23):
		train_set.append(shuffled_player[j])

	for j in range(23, 29):
		test_set.append(shuffled_player[j])
	
	for j in range(29,33):
		val_set.append(shuffled_player[j])

	w+=33

# print(train_set[0])



index = 0
while index < len(train_set):
    seq, target  = train_set[index]

    if torch.isnan(seq).any():
        # If NaN values are found, remove the tensor from the list
        train_set.pop(index)

    elif torch.isnan(target).any():
    	train_set.pop(index)

    elif torch.allclose(target, torch.zeros_like(target)):
    	train_set.pop(index)

    else:
        # If no NaN values are found, move to the next tensor
        index += 1


nan_count = 0
for i in range(len(train_set)):
	if torch.isnan(train_set[i][1]).any():
		nan_count+=1
		print(f"at index {i} : {train_set[i][1]}")

	elif torch.isnan(train_set[i][0]).any():
		nan_count+=1
		print(f"at index {i} : {train_set[i][0]}")





index = 0
while index < len(val_set):
    seq, target  = val_set[index]

    if torch.isnan(seq).any():
        # If NaN values are found, remove the tensor from the list
        val_set.pop(index)

    elif torch.isnan(target).any():
    	val_set.pop(index)

    elif torch.allclose(target, torch.zeros_like(target)):
    	val_set.pop(index)

    else:
        # If no NaN values are found, move to the next tensor
        index += 1


nan_count = 0
for i in range(len(val_set)):
	if torch.isnan(val_set[i][1]).any():
		nan_count+=1
		print(f"at index {i} : {val_set[i][1]}")

	elif torch.isnan(val_set[i][0]).any():
		nan_count+=1
		print(f"at index {i} : {val_set[i][0]}")



index = 0
while index < len(test_set):
    seq, target  = test_set[index]

    if torch.isnan(seq).any():
        # If NaN values are found, remove the tensor from the list
        test_set.pop(index)

    elif torch.isnan(target).any():
    	test_set.pop(index)

    elif torch.allclose(target, torch.zeros_like(target)):
    	test_set.pop(index)

    else:
        # If no NaN values are found, move to the next tensor
        index += 1


nan_count = 0
for i in range(len(test_set)):
	if torch.isnan(test_set[i][1]).any():
		nan_count+=1
		print(f"at index {i} : {test_set[i][1]}")

	elif torch.isnan(test_set[i][0]).any():
		nan_count+=1
		print(f"at index {i} : {test_set[i][0]}")

torch.save(train_set[0][0], "nonextteams_sequence")

#torch.save(train_set, "TRAIN.pt")
#torch.save(val_set, "VAL.pt")