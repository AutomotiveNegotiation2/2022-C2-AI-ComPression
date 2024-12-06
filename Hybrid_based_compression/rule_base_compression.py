import zlib
import time
import json

def alg_compression(alg_data,res):
    # Rule based compression using zlib
    with open("zlib_param.json") as f:
        zparam = json.load(f)
    while True:
        if alg_data is not None and len(alg_data) != 0:
            try:
                com_data = alg_data[0][0]
            except Exception as e:
                print(f"ERROR_rule_{e}")
                break
            if com_data == "break":
                break
            start = time.time()
            before_sum = len(com_data)
            zcompress = zlib.compressobj(level = zparam["level"],memLevel = zparam["memLevel"],wbits=zparam["wbits"],strategy = zparam["strategy"])
            compress_data = zcompress.compress(com_data.encode(encoding='utf-8'))
            after_size = len(compress_data)
            saving_space = ( 1 - ( (after_size) /before_sum) )*100
            # if saving_space < 70.0:
            #     print("RULE BASED COMPRESSION")
            #     AI_data.append(com_data)
            # else:
            res.append([alg_data[0][1],"RULE",saving_space,time.time() - start, alg_data[0][2]])
            del alg_data[0]
        
    print("alg compress END")