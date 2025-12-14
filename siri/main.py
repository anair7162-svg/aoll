import websocket
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize lists for buy and sell orders
buyorders, sellorders = [], []
in_position = False
df = pd.DataFrame(columns=["price"])
total_bitcoins = 1  # Your current Bitcoin holdings
endpoint = 'wss://stream.binance.com:9443/ws'

# Message to subscribe to the ticker
our_msg = json.dumps({
    'method': 'SUBSCRIBE',
    'params': ['btcusdt@ticker'],
    'id': 1
})

def on_open(ws):
    ws.send(our_msg)
    print("Connection opened and subscribed to ticker.")

def on_message(ws, message):
    global df, in_position, buyorders, sellorders, total_bitcoins
    out = json.loads(message)
    out = pd.DataFrame({'price': float(out['c'])}, index=[pd.to_datetime(out['E'], unit='ms')])
    df = pd.concat([df, out], axis=0)
    df = df.tail(30)  # Keep only the last 30 prices for plotting

    last_price = df.tail(1).price.values[0]
    sma_5 = df.price.rolling(5).mean().tail(1).values[0]

    if not in_position and last_price > sma_5:
        print('Bought for ' + str(last_price))
        buyorders.append(last_price)
        total_bitcoins += 1  # Update Bitcoin holdings
        in_position = True
    elif in_position and last_price < sma_5:
        profit = (last_price - buyorders[-1]) * total_bitcoins
        if profit > 1:
            print('Sold for ' + str(last_price))
            print('Profit: ' + str(profit))
            sellorders.append(last_price)
            total_bitcoins -= 1  # Update Bitcoin holdings
            in_position = False

    # Display current Bitcoin price and total value of holdings
    total_value = total_bitcoins * last_price
    print(f'Current Bitcoin Price: {last_price}')
    print(f'Total Bitcoins Owned: {total_bitcoins}')
    print(f'Total Value of Holdings: {total_value}')
    
    # Update the plot
    plt.clf()
    plt.plot(df.index, df.price, label='Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Real-time Bitcoin Price')
    plt.legend()
    plt.draw()
    plt.pause(0.1)

def start_ws():
    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_open=on_open)
    ws.run_forever()

# Start the websocket connection and the plot
if __name__ == "__main__":
    plt.ion()
    plt.figure()
    start_ws()
