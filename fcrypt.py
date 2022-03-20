from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from Crypto import Random
import os
import sys

############################################
#             loading key.pem              #       
############################################
def load_public_key(file):
    with open(file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            #password=None,
            backend=default_backend()
        )
    return public_key

def load_private_key(file):
    with open(file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

############################################
#                 Encryption               #       
############################################

def encrypt(file, key) :
    with open(file) as m:
        message = m.read().encode('ascii')
        ciphertext = key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return ciphertext

############################################
#                 Signature                #       
############################################

def sign_msg(file, key):
    message = file
    signature = key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )
    return signature

############################################
#           Signature verification         #       
############################################

def verify_signature(signature ,message , key):
    return key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

############################################
#                 Decryption               #       
############################################

def decrypt(ciphertext, key):
    plaintext = key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

############################################
#    Function parameters verification      #       
############################################

if len(sys.argv) != 6 :
    print('USAGE:  python fcrypt.py -e destination_public_key_filename sender_private_key_filename input_plaintext_file ciphertext_file')
    sys.exit(2)
    

option = sys.argv[1]
if(option == "-e"):
    #Load parameters
    print('This is the encryption function')
    pubKeyReceiverFile = sys.argv[2]
    privKeysenderFile = sys.argv[3]
    plaintextFile = sys.argv[4]
    cipherTxtFile = sys.argv[5]
    
    pub_recv = load_public_key(pubKeyReceiverFile)
    priv_send = load_private_key(privKeysenderFile)
    
    # encrypt the fle the sign the encrypted file, 
    #and store the signature concatenaetd with 
    #the encrypted message into the output file
    
    encrypted = encrypt(plaintextFile,pub_recv)
    signed = sign_msg(encrypted,priv_send)

    f = open(cipherTxtFile, "wb")
    f.write(signed+encrypted)
    print ('Your encrypted message is saved in ',cipherTxtFile)
    
    
#python fcrypt.py -d destination_private_key_filename sender_public_key_filename ciphertext_file output_plaintext_file

if(option == "-d"):
     #Load parameters
    print('This is the decryption function')
    privKeyReceiverFile = sys.argv[2]
    pubKeysenderFile = sys.argv[3]
    ciphertextFile = sys.argv[4]
    plainTxtFile = sys.argv[5]
    
    pub_send = load_public_key(pubKeysenderFile)
    priv_recv = load_private_key(privKeyReceiverFile)

    #Read the ciphertext file 
    # the first 256 characteres correspond to  the signature, 
    #and the rest of the file corresponds to the encrypted mmessage
    f = open(ciphertextFile, "rb")
    signature = f.read(256)
    encryption = f.read()
    
    v_signed = verify_signature(signature,encryption,pub_send)
    decrypted = decrypt(encryption,priv_recv) 

    
    f = open(plainTxtFile, "w")
    f.write(decrypted.decode("utf-8"))
    print ('You decrypted the message : ')

    f = open(plainTxtFile, "r")
    print(f.read())
    