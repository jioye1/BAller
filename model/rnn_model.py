import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from matplotlib import pyplot as plt
import numpy as np

TRAIN = torch.load("NONEXT_TEAMS_TRAIN.pt")
VAL = torch.load("NONEXT_TEAMS_VAL.pt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(RNNModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Define the RNN layer
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        # self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        # Define the output layer
        self.fc1 = nn.Linear(hidden_size, 128)
        self.fc2 = nn.Linear(128, output_size)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.rnn(x, h0)
        out = self.fc1(out[:, -1, :])
        out = self.fc2(out)
        out=self.relu(out)
        return out

class FootballDataset(Dataset):
    def __init__(self, data):
        self.data = data
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        input_sequence, target = self.data[idx]
        return input_sequence, target


input_size = 137  # Number of features in each time step of the input sequence
hidden_size = 200  # Number of units in the hidden state of the RNN
num_layers = 2  # Number of recurrent layers in the RNN
output_size = 31  # Number of features in the output tensor

batch_size = 32
learning_rate = 0.0003
num_epochs = 30


model = RNNModel(input_size, hidden_size, num_layers, output_size)
model.to(device)


criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


dataset = FootballDataset(TRAIN)
valset = FootballDataset(VAL)


train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
val_loader = DataLoader(valset, batch_size=batch_size, shuffle=False)


total_steps = len(train_loader)

count_removed = 0

losses = []
avg_losses = []
count = 0
for epoch in range(num_epochs):
    model.train()
    for i, (input_sequence, target) in enumerate(train_loader):
  
        input_sequence, target = input_sequence.to(device), target.to(device)

        outputs = model(input_sequence)
        loss = criterion(outputs, target)

        losses.append(loss.item())
        count+=1
        if count == 10:
            count = 0
            avg_losses.append(np.mean(losses))
            losses.clear()

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()

        if (i+1) % 100 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_steps, loss.item()))


    model.eval()
    val_losses = []
    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            val_loss = criterion(outputs, targets)
            val_losses.append(val_loss.item())


    avg_val_loss = sum(val_losses) / len(val_losses)
    print(avg_val_loss)


torch.save(model.state_dict(), 'weights.pth')