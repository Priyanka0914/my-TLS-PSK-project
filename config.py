#config.py

# first code before unique psks for each client 
PSK_MAP = {
    b'client1':bytes.fromhex('1a2b3c4d5e6f708192a3b4c5d6e7f809'),
    b'client2':bytes.fromhex('abcdefabcdefabcdefabcdefabcdefab'),
    b'client3':bytes.fromhex('1234567890abcdef1234567890abcdef')    
}

# CLIENT_ID = b'client2'
# CLIENT_PSK = PSK_MAP[CLIENT_ID]

# CLIENT_ID = b'client1'
# CLIENT_PSK = bytes.fromhex('1a2b3c4d5e6f708192a3b4c5d6e7f809') 




# import os 

# CLIENT_ID = [b'client1',b'client2',b'client3']

# PSK_MAP = {cid: os.urandom(16) for cid in CLIENT_ID}

# # CLIENT_ID = b'client2'
# CLIENT_PSK = PSK_MAP[CLIENT_ID]

# for cid, psk in PSK_MAP.items():
#     print(f"{cid.decode()} PSK: {psk.hex()}")




