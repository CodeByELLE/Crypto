from cryptography.hazmat.backends import default_backend
import base64
import os
import sys
import hashlib
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


#  python fcrypt.py -e destination_public_key_filename sender_private_key_filename input_plaintext_file ciphertext_file

#  python fcrypt.py -d destination_private_key_filename sender_public_key_filename ciphertext_file output_plaintext_file
if len(sys.argv) != 6 :
    print('USAGE:  python fcrypt.py -e destination_public_key_filename sender_private_key_filename input_plaintext_file ciphertext_file')
    sys.exit(2)
    

option = sys.argv[1]
if(option == "-e"):
    
    print("hi")
    PubKeyBobFile = sys.argv[2]
    PrivKeyAliceFile = sys.argv[3]
    PlaintextFile = sys.argv[4]
    cipherTxtFile = sys.argv[5]
    
    '''private_key_Bob = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend())
    # to get the public key
    public_key_Bob = private_key_Bob.public_key()
    
    private_key_Alice = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend())
    # to get the public key
    public_key_Alice = private_key_Alice.public_key()'''
    
    with open(PubKeyBobFile, "rb") as key_file:
         public_key_Bob = serialization.load_pem_public_key(open('keys/pubKeyBob.pem', 'rb').read(),default_backend()) 
            
    with open(PlaintextFile) as m:
        message = m.read().encode('ascii')
        prehashed = hashlib.sha256(message).hexdigest()
    
    
    ciphertext = public_key_Bob.encrypt(
    bytes(prehashed.encode('ascii')),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA512()),
        algorithm=hashes.SHA512(),
        label=None))
    print(base64.b64encode(ciphertext))
    
    