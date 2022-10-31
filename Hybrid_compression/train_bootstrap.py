import numpy as np
import os
import sys
import torch
import torch.nn.functional as F
from torch import nn, optim
import torch.nn.init as init
from torch.utils.data import Dataset, DataLoader
from models_torch import *
from utils import *
import argparse
import time
import json

def get_argument_parser():
    parser = argparse.ArgumentParser();
    parser.add_argument('--file_name', type=str, 
                        help='The name of the input file')
    parser.add_argument('--gpu', type=str, default='0',
                        help='Name for the log file')
    parser.add_argument('--epochs', type=int, 
                        help='Num of epochs')
    parser.add_argument('--model_weights_path', type=str,
                        help='Path to model parameters')
    parser.add_argument('--timesteps', type=int,
                        help='Num of time steps')
    parser.add_argument('--hdim1', type=int, 
                        help='Num of hdim1')
    parser.add_argument('--hdim2', type=int, 
                        help='Num of hdim2')
    parser.add_argument('--n_layers', type=int, 
                        help='Num of n_layers')
    parser.add_argument('--batch_size', type=int, 
                        help='Num of time batch_size')
    parser.add_argument('--emb_size', type=int,
                        help='Num of time emb_size')                        
    return parser

def weight_init(m):
    '''
    Usage:
        model = Model()
        model.apply(weight_init)
    '''
    if isinstance(m, nn.Linear):
        init.xavier_normal_(m.weight.data)
        init.zeros_(m.bias.data)
    elif isinstance(m, nn.GRU):
        for value in m.state_dict():
            if 'weight_ih' in value:
                init.xavier_normal_(m.state_dict()[value])
            elif 'weight_hh' in value:
                init.orthogonal_(m.state_dict()[value])
            elif 'bias' in value:
                init.zeros_(m.state_dict()[value])
    elif isinstance(m, nn.GRUCell):
        for value in m.state_dict():
            if 'weight_ih' in value:
                init.xavier_normal_(m.state_dict()[value])
            elif 'weight_hh' in value:
                init.orthogonal_(m.state_dict()[value])
            elif 'bias' in value:
                init.zeros_(m.state_dict()[value])

def loss_function(pred, target):
    loss = 1/np.log(2) * F.nll_loss(pred, target)
    return loss

def train(epoch, reps=20):
    model.train()
    train_loss = 0
    start_time = time.time()
    loss_list = []
    early_stop_count = 0
    for batch_idx, sample in enumerate(train_loader):
        data, target = sample['x'].to(device), sample['y'].to(device)
        optimizer.zero_grad()
        pred = model(data)
        loss = loss_function(pred, target)
        loss.backward()
        train_loss += loss.item()
        nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()
        scheduler.step()
        if batch_idx % 500 == 0:
            print("{} secs".format(time.time() - start_time))
            print('====> Epoch: {} Batch {}/{} Average loss: {:.4f}'.format(
            epoch, batch_idx+1, len(Y)//batch_size, train_loss / (batch_idx+1)), end='\r', flush=True)
            start_time = time.time()
            if len(loss_list) < 11:
                loss_list.append(train_loss / (batch_idx+1))
            else :
                avg_loss = np.mean(loss_list)
                if (train_loss / (batch_idx+1) ) > avg_loss:
                    early_stop_count +=1
            if early_stop_count == 10:
                print('[EARLY STOP] Epoch: {} Batch {}/{} Average loss: {:.4f}'.format(
            epoch, batch_idx+1, len(Y)//batch_size, train_loss / (batch_idx+1)), end='\r', flush=True)
                break

    print('====> Epoch: {} Average loss: {:.10f}'.format(
        epoch, train_loss / (batch_idx+1)), flush=True)
    return train_loss / (batch_idx+1)

torch.manual_seed(0)
parser = get_argument_parser()
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu
num_epochs=args.epochs
batch_size=args.batch_size
timesteps=args.timesteps
use_cuda = True

use_cuda = use_cuda and torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print("Using", device)
sequence = np.load(args.file_name + ".npy")
vocab_size = len(np.unique(sequence))

# Convert data into context and target symbols
X, Y = generate_single_output_data(sequence, batch_size, timesteps)
kwargs = {'num_workers': 4, 'pin_memory': True} if use_cuda else {}
train_dataset = CustomDL(X, Y)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                        batch_size=batch_size,
                                        shuffle=True, **kwargs)

dic = {'vocab_size': vocab_size, 'emb_size': args.emb_size,
        'length': timesteps, 'jump': 16,
        'hdim1': args.hdim1, 'hdim2': args.hdim2, 'n_layers': args.n_layers,
        'bidirectional': True,
        'epochs' : args.epochs,
        'batch_size' :args.batch_size }
print("Vocab Size {}".format(vocab_size))
print("CudNN version", torch.backends.cudnn.version())
model_dir_name =f"log_dir_epochs_{dic['epochs']}_batch_size_{dic['batch_size']}_hdim1_{dic['hdim1']}_hdim2_{dic['hdim2']}_n_layers_{dic['n_layers']}"
try:
    os.mkdir(model_dir_name)
except :
    print(f"exist File {model_dir_name}")
# Create Bootstrap Model Param
with open(args.model_weights_path+"_hyper", 'w') as f_h:
    json.dump(dic, f_h, indent=4)
model = BootstrapNN(**dic).to(device)
# Apply Weight Initalization
model.apply(weight_init)
# Learning Rate Decay
mul = len(Y)/5e7
decayrate = mul/(len(Y) // batch_size)
# Optimizer
optimizer = optim.Adam(model.parameters(), lr=5e-3)
fcn = lambda step: 1./(1. + decayrate*step)
scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=fcn)
# Training with Best Model Selection
epoch_loss = 1e8
for epoch in range(num_epochs):
    lss = train(epoch+1)
    if lss < epoch_loss:
        torch.save(model.state_dict(), model_dir_name +"/"+args.model_weights_path)
        print("Loss went from {:.4f} to {:.4f}".format(epoch_loss, lss))
        epoch_loss = lss
print("Done")
dzip_dic = { "use_cuda" : 1 if use_cuda == True else 0, "gpu" :  args.gpu,     
    "transform_dict": "1.0s.params",
    "batch_size" : args.batch_size,
    "timesteps" : args.timesteps,
    "model_weights_path" : model_dir_name +"/"+args.model_weights_path,
    "temp_dir" : "temp",
    "temp_file_prefix" : "temp/compressed"}
    
with open("dzip_param.json", 'w') as f_h:
    json.dump(dzip_dic, f_h, indent=4)



