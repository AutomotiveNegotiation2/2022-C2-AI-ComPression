import torch
import torch.nn.functional as F
from torch import nn, optim
import numpy as np

class BootstrapNN(nn.Module):
    def __init__(self, vocab_size, emb_size, length, jump, hdim1, hdim2, n_layers, bidirectional,epochs,batch_size):
        super(BootstrapNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, emb_size)
        self.vocab_size = vocab_size
        self.len = length
        self.hdim1 = hdim1
        self.hdim2 = hdim2
        self.n_layers = n_layers
        self.bidirectional = bidirectional
        self.jump = jump
        self.rnn_cell = nn.GRU(emb_size, hdim1, n_layers, batch_first=True, bidirectional=bidirectional)
        
        if bidirectional:
            self.lin1 = nn.Sequential(
            nn.Linear(2*hdim1*(length//jump), hdim2),
            nn.ReLU(inplace=True)
            )
            self.flin1 = nn.Linear(2*hdim1*(length//jump), vocab_size)
        else:
            self.lin1 = nn.Sequential(
            nn.Linear(hdim1*(length//jump), hdim2),
            nn.ReLU(inplace=True)
            )
            self.flin1 = nn.Linear(hdim1*(length//jump), vocab_size)
        self.flin2 = nn.Linear(hdim2, vocab_size)

    def forward(self, inp):
        emb = self.embedding(inp)
        output, hidden = self.rnn_cell(emb)
        slicedoutput = torch.flip(output, [1])[:,::self.jump,:]
        batch_size = slicedoutput.size()[0]
        flat = slicedoutput.contiguous().view(batch_size, -1)
        prelogits = x = self.lin1(flat)
        x = self.flin1(flat) + self.flin2(x)
        out = F.log_softmax(x, dim=1)

        return out

