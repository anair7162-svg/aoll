import torch
import torch.nn as nn

class LSTM_GRU(nn.Module):
    def __init__(self, input_size, hidden_dim, num_layers, output_size, dropout=0.3, bidirectional=True):
        super(LSTM_GRU, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.num_directions = 2 if bidirectional else 1

        self.lstm = nn.LSTM(input_size, hidden_dim, num_layers, batch_first=True, dropout=dropout, bidirectional=bidirectional)
        self.ln1 = nn.LayerNorm(hidden_dim * self.num_directions)
        self.gru = nn.GRU(hidden_dim * self.num_directions, hidden_dim, num_layers, batch_first=True, dropout=dropout, bidirectional=bidirectional)
        self.ln2 = nn.LayerNorm(hidden_dim * self.num_directions)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_dim * self.num_directions, hidden_dim)
        self.act = nn.LeakyReLU()
        self.fc2 = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        h0_lstm = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_dim, device=x.device)
        c0_lstm = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_dim, device=x.device)
        h0_gru = torch.zeros(self.num_layers * self.num_directions, x.size(0), self.hidden_dim, device=x.device)

        out, _ = self.lstm(x, (h0_lstm, c0_lstm))
        out = self.ln1(out)
        out, _ = self.gru(out, h0_gru)
        out = self.ln2(out)
        out = self.dropout(out)
        out = self.fc1(out[:, -1, :])
        out = self.act(out)
        out = self.fc2(out)
        return out
