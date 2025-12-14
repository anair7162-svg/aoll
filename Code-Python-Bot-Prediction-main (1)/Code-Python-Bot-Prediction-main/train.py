import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from data_preprocessing import train_seq, train_tar, test_seq, test_tar
import pandas as pd
from model import LSTM_GRU  # Import the combined LSTM-GRU model

train_seq = torch.Tensor(train_seq)
train_tar = torch.Tensor(train_tar)
test_seq = torch.Tensor(test_seq)
test_tar = torch.Tensor(test_tar)

train_dataset = TensorDataset(train_seq, train_tar)
test_dataset = TensorDataset(test_seq, test_tar)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Define hyperparameters
input_size = 1
hidden_dim = 1500
num_layers = 2
output_size = 1

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Instantiate the model
model = LSTM_GRU(input_size=input_size, hidden_dim=hidden_dim, num_layers=num_layers, output_size=output_size).to(device)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

train_seq, train_tar = train_seq.to(device), train_tar.to(device)
test_seq, test_tar = test_seq.to(device), test_tar.to(device)

# Training loop
epochs = 5
e_loss = []
for epoch in range(epochs):
    model.train()
    epoch_loss = 0.0
    for batch in train_loader:
        inputs, targets = batch
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        y_pred = model(inputs)
        loss = criterion(y_pred, targets)
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
    
    e_loss.append(epoch_loss / len(train_loader))
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{epochs}] Loss: {epoch_loss / len(train_loader)}')

# Testing loop
model.eval()
predictions = []
with torch.no_grad():
    for batch in test_loader:
        inputs, _ = batch
        inputs = inputs.to(device)
        outputs = model(inputs)
        predictions.append(outputs.cpu().numpy())
        
predictions = np.concatenate(predictions, axis=0)

in_scaler = np.load('in_scaler.npy', allow_pickle=True).item()
test_dates = np.load('test_dates.npy', allow_pickle=True)

predictions = in_scaler.inverse_transform(predictions)
actual = in_scaler.inverse_transform(test_tar.cpu().reshape(-1, 1))

test_dates = [pd.to_datetime(date) for date in test_dates]

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(test_dates, actual, label='Actual Prices')
plt.plot(test_dates, predictions, label='Predicted Prices', linestyle='--')
plt.title('Ethereum Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)  
plt.show()

# --- Future Prediction Section ---
# Load future dates
future_dates = np.load('future_dates.npy', allow_pickle=True)
num_future_days = len(future_dates)

# Get the last window from the full normalized price series
import data_preprocessing
last_window = data_preprocessing.prices[-data_preprocessing.ws:].reshape(1, -1, 1)
last_window = torch.Tensor(last_window).to(device)

future_preds = []
model.eval()
with torch.no_grad():
    current_window = last_window.clone()
    for _ in range(num_future_days):
        next_pred = model(current_window)
        future_preds.append(next_pred.cpu().numpy().flatten()[0])
        # Update window: remove first, append new prediction
        next_input = next_pred.cpu().numpy().reshape(1, 1, 1)
        current_window = torch.cat([
            current_window[:, 1:, :],
            torch.Tensor(next_input).to(device)
        ], dim=1)

future_preds = np.array(future_preds).reshape(-1, 1)
future_preds = in_scaler.inverse_transform(future_preds)

# Plot future predictions
plt.figure(figsize=(10, 5))
plt.plot(test_dates, actual, label='Actual Prices')
plt.plot(test_dates, predictions, label='Predicted Prices', linestyle='--')
plt.plot(future_dates, future_preds, label='Future Predictions', linestyle=':')
plt.title('Ethereum Price Prediction with Future Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()











