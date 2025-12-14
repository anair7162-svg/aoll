import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


data_df = pd.read_csv('Ethereum.csv')  


data_df['Date'] = pd.to_datetime(data_df['Date'])

data_df = data_df[(data_df['Date'] >= '2019-01-01') & (data_df['Date'] <= '2019-12-31')]

prices = data_df['Price'].values
dates = data_df['Date'].values


in_scaler = MinMaxScaler(feature_range=(-1, 1))
prices = in_scaler.fit_transform(prices.reshape(-1, 1))


train_size = int(len(prices) * 0.8)  
test_size = len(prices) - train_size
train_data, test_data = prices[0:train_size], prices[train_size:len(prices)]
test_dates = dates[train_size:len(prices)]  

# LSTM thingy model 
ws = 9 # window size
def data_loader(train, test, dates=None):
    train_seq, train_tar = [], []
    test_seq, test_tar = [], []
    test_seq_dates = []

    for i in range(len(train) - ws):
        train_seq.append(train[i:i + ws])
        train_tar.append(train[i + ws])
    for i in range(len(test) - ws):
        test_seq.append(test[i:i + ws])
        test_tar.append(test[i + ws])
        test_seq_dates.append(dates[i + ws] if dates is not None else None)
        
    return np.array(train_seq), np.array(train_tar), np.array(test_seq), np.array(test_tar), np.array(test_seq_dates)

train_seq, train_tar, test_seq, test_tar, test_seq_dates = data_loader(train_data, test_data, test_dates)


np.save('in_scaler.npy', in_scaler)
np.save('test_dates.npy', test_seq_dates)

def generate_future_dates(last_date, num_days):
    """
    Generate a list of future dates after the last known date.
    Args:
        last_date (datetime): The last date in the dataset.
        num_days (int): Number of future days to generate.
    Returns:
        np.array: Array of future datetime objects.
    """
    return np.array([last_date + pd.Timedelta(days=i) for i in range(1, num_days + 1)])

# Example usage: generate 30 future dates after the last known date
num_future_days = 30
last_known_date = data_df['Date'].max()
future_dates = generate_future_dates(last_known_date, num_future_days)
np.save('future_dates.npy', future_dates)
