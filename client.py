import socket
import rsa
import json
import ast
from pprint import pprint
from server_creds import *

CREDS_FILE = "creds/client0.json"
PKDA_CREDS_FILE = "creds/pkda.json"

with open (CREDS_FILE, "r") as f:
    creds = json.load(f)
    d, e, n = int(creds["d"]), int(creds["e"]), int(creds["n"])
    
with open (PKDA_CREDS_FILE, "r") as f:
    creds = json.load(f)
    pkda_e, pkda_n = int(creds["e"]), int(creds["n"])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

nonce = "buttons - by the pussycat girls"

# Request PKDA to get public key of client1
request_dict = {
    "request_type": "request_public_key",
    "initiator": 0,
    "requested": 1,
    "timestamp": "ignore",
    "nonce": nonce
}

request_str = str(request_dict)
print(request_str)

encrypted_message = str(rsa.encrypt(request_str, pkda_e, pkda_n))

client_socket.send(encrypted_message.encode())

# encrypted_response = int(client_socket.recv(40960).decode())
encrypted_response = client_socket.recv(40960).decode()

# response_dict = ast.literal_eval(str(rsa.decrypt(encrypted_response, d, n)))
response_dict = ast.literal_eval(encrypted_response)

print("Decrypted response from PKDA")
pprint(response_dict)

client_socket.close()
