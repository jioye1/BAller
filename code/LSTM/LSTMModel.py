#Naji EL-KHOURI, Nicola LAMBO, Jackson YU
# MAIS 202: Deliverable 3
#LSTM Model for predicting a player's stats for the 2023-2024 season based on their stats from previous seasons


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
    
player_name = input("Please enter the name of a player who played in the top 5 European leagues in the 2022-2023 season: ")

# Defining hyperparameters
input_size = 188 #size of the input vector: position, team, league, and stats
hidden_size = 64 
num_layers = 2    
output_size = 188 
num_epochs = 100
learning_rate = 0.001

train_dataset = torch.load("training_dictionary_80.pt")
val_dataset = torch.load("testing_dictionary_20.pt")

# Preparing data loaders
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)

# Initializing model, loss function, and optimizer
model = LSTMModel(input_size, hidden_size, num_layers, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * inputs.size(0)
    train_loss /= len(train_loader.dataset)
    
    # Validation loop
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, targets in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            val_loss += loss.item() * inputs.size(0)
        val_loss /= len(val_loader.dataset)
    
    print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Test Loss: {val_loss:.4f}')

# Prediction
model.eval()
with torch.no_grad():
    # Assuming test_loader contains data for the 2022-2023 season
    for inputs, _ in val_loader:
        predictions = model(inputs)
    print(model)
       
