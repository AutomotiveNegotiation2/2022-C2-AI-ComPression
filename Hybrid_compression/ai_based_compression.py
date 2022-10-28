
import os
import json
import torch
import arithmeticcoding_fast
import shutil
from models_torch import *
from torch.autograd import Variable
import time
import json
from utils import *


def compress(dparam,model, X, Y, bs, vocab_size, timesteps, device, final_step=False):
    # Dzip compression model
    if not final_step:
        num_iters = (len(X)+timesteps) // bs
        ind = np.array(range(bs))*num_iters

        f = [open(dparam["temp_file_prefix"]+'.'+str(i),'wb') for i in range(bs)]
        bitout = [arithmeticcoding_fast.BitOutputStream(f[i]) for i in range(bs)]
        enc = [arithmeticcoding_fast.ArithmeticEncoder(32, bitout[i]) for i in range(bs)]

        prob = np.ones(vocab_size)/vocab_size
        cumul = np.zeros(vocab_size+1, dtype = np.uint64)
        cumul[1:] = np.cumsum(prob*10000000 + 1)

        # Encode first K symbols in each stream with uniform probabilities
        for i in range(bs):
            for j in range(min(timesteps, num_iters)):
                enc[i].write(cumul, X[ind[i],j])

        cumul = np.zeros((bs, vocab_size+1), dtype = np.uint64)

        for j in (range(num_iters - timesteps)):
            # Create Batches
            bx = Variable(torch.from_numpy(X[ind,:])).to(device)
            by = Variable(torch.from_numpy(Y[ind])).to(device)
            with torch.no_grad():
                model.eval()
                prob = torch.exp(model(bx)).detach().cpu().numpy()
            cumul[:,1:] = np.cumsum(prob*10000000 + 1, axis = 1)

            # Encode with Arithmetic Encoder
            for i in range(bs):
                enc[i].write(cumul[i,:], Y[ind[i]])
            ind = ind + 1
        # close files
        for i in range(bs):
            enc[i].finish()
            bitout[i].close()
            f[i].close()
    
    else:
        f = open(dparam["temp_file_prefix"]+'.last','wb')
        bitout = arithmeticcoding_fast.BitOutputStream(f)
        enc = arithmeticcoding_fast.ArithmeticEncoder(32, bitout)
        prob = np.ones(vocab_size)/vocab_size
        cumul = np.zeros(vocab_size+1, dtype = np.uint64)
        cumul[1:] = np.cumsum(prob*10000000 + 1)        

        for j in range(timesteps):
            enc.write(cumul, X[0,j])
        for i in (range(len(X))):
            bx = Variable(torch.from_numpy(X[i:i+1,:])).to(device)
            with torch.no_grad():
                model.eval()
                prob = torch.exp(model(bx)).detach().cpu().numpy()
            cumul[1:] = np.cumsum(prob*10000000 + 1)
            enc.write(cumul, Y[i])
        enc.finish()
        bitout.close()
        f.close()
    return


def AI_compression(AI_data,res):
    # AI compression based Dzip
    with open("dzip_param.json") as f:
        dparam = json.load(f)
    use_cuda = dparam["use_cuda"] and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    os.environ["CUDA_VISIBLE_DEVICES"]=dparam["gpu"]
    id2char = dparam["transform_dict"]
    if os.path.isfile(id2char):
        with open(id2char,'r') as f:
            print("LOAD model hyper parameter")
            params = json.load(f)
    else:
        print("No model parameter")
        return 
    batch_size = dparam["batch_size"]
    timesteps = dparam["timesteps"]

    # Select Model Parameters based on Alphabet Size
    with open(dparam["model_weights_path"]+"_hyper", 'r') as ff:
        bsdic = json.load(ff)
        if bsdic:
            print("LOAD_WEIGHT")
        else:
            print("NOT_LOAD_WEIGHT")

    vocab_size = bsdic["vocab_size"]
    model = BootstrapNN(**bsdic).to(device)
    model.load_state_dict(torch.load(dparam["model_weights_path"]))
    char2id_dict = params["char2id_dict"]
    while True:
        if AI_data:
            try:
                com_data = AI_data[0][0]
            except Exception as e:
                print(f"ERROR_AI_{e}")
                break
            if com_data == "break":
                break

            com_data = bytes(com_data,encoding = "utf-8")
            start_time = time.time()
            before_size_ai = len(com_data)
            before_size = before_size_ai
            out = [ char2id_dict[ str(c) ] for c in com_data]
            sequence = np.array(out)
            series = sequence.reshape(-1)
            if os.path.exists(dparam["temp_dir"]):
                os.system("rm -r {}".format(dparam["temp_dir"]))

            if not os.path.exists(dparam["temp_dir"]):
                os.makedirs(dparam["temp_dir"])
            # Convert data into context and target symbols
            data = strided_app(series, timesteps+1, 1)
            X = data[:, :-1]
            Y = data[:, -1]
            l = int(len(series)/batch_size)*batch_size
            
            compress(dparam, model, X, Y, batch_size, vocab_size, timesteps, device)
            if l < len(series)-timesteps:
                compress(dparam, model, X[l:], Y[l:], 1, vocab_size, timesteps, device, final_step = True)
            else:
                f = open(dparam["temp_file_prefix"]+'.last','wb')
                bitout = arithmeticcoding_fast.BitOutputStream(f)
                enc = arithmeticcoding_fast.ArithmeticEncoder(32, bitout) 
                prob = np.ones(vocab_size)/vocab_size
                
                cumul = np.zeros(vocab_size+1, dtype = np.uint64)
                cumul[1:] = np.cumsum(prob*10000000 + 1)        
                for j in range(l, len(series)):
                        enc.write(cumul, series[j])
                enc.finish()
                bitout.close() 
                f.close()
            
            # combine files into one file
            f = open('res.combined','wb')
            for i in range(batch_size):
                f_in = open(dparam["temp_file_prefix"]+'.'+str(i),'rb')
                byte_str = f_in.read()
                byte_str_len = len(byte_str)
                var_int_encode(byte_str_len, f)
                f.write(byte_str)
                f_in.close()
            f_in = open(dparam["temp_file_prefix"]+'.last','rb')
            byte_str = f_in.read()
            byte_str_len = len(byte_str)
            var_int_encode(byte_str_len, f)
            f.write(byte_str)
            f_in.close()
            f.close()
            shutil.rmtree('temp')
            end_time = time.time()
            after_size_ai = os.path.getsize('res.combined')
            after_size = after_size_ai
            
            saving_spaces = (1 - (after_size/before_size))*100
            res.append([AI_data[0][1]," AI ",saving_spaces, end_time - start_time,AI_data[0][2]])
            del AI_data[0]
    print("AI_compress END")