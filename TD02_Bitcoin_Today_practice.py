import secrets
import hashlib
import binascii
import unicodedata
import hmac
import ecdsa
import struct
import base58
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa import int_to_string, string_to_int
from mnemonic import Mnemonic
import bip32utils
from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN

##############
#Créer un entier aléatoire pouvant servir de seed à un wallet de façon sécurisée
##############

bits = secrets.randbits(128)
bits_hex = hex(bits)
private_key = bits_hex[2:]

##############
#Représenter cette seed en binaire et le découper en lot de 11 bits
##############

bits_bin = bin(bits)
bits_bin = bits_bin[2:]

data = binascii.unhexlify(private_key)
h = hashlib.sha256(data).hexdigest()
b = bin(int(binascii.hexlify(data),16))[2:].zfill(len(data)*8) 
checksum =  bin(int(h,16))[2:].zfill(256)[: len(data)* 8//32]

tab=[]
word=""
cpt=0
if(len(str(b))<128):
    for i in range(0, 128-len(str(b))):
        word+="0"
        cpt+=1

for j in b:
    word=str(word)+str(j)
    cpt+=1
    if cpt==11:
        cpt=0
        tab.append(word)
        word=""
word+=str(checksum)
tab.append(word)

##############
#Attribuer à chaque lot un mot selon la liste BIP 39 et afficher la seed en mnémonique 
##############

with open("english.txt", "r") as f:
         wordlist = [w.strip() for w in f.readlines()]
seed = []
for k in range(len(tab)):
    for i in range(len(tab[k])//11):
        indx = int(tab[k][11*i:11*(i+1)],2)
        seed.append(wordlist[indx])
phrase = " ".join(seed)

##############
#Permettre l’import d’une seed mnémonique
##############

seed_temp = str(input("\nVoulez vous importer votre propre seed ? (y/n)"))
if(seed_temp=="y"):
    phrase = str(input("\nEntrez votre propre seed : "))
print(phrase)

normalized_mnemonic = unicodedata.normalize("NFKD", phrase)
password = ""
normalized_passphrase = unicodedata.normalize("NFKD", password)

passphrase = "mnemonic" + normalized_passphrase
mnemonic = normalized_mnemonic.encode("utf-8")
passphrase = passphrase.encode("utf-8")

bin_seed = hashlib.pbkdf2_hmac("sha512", mnemonic, passphrase, 2048)
hex_bin = binascii.hexlify(bin_seed[:64])

mnemon = Mnemonic('english')
seed_mnemonic = mnemon.to_seed(mnemonic)

##############
#Extraire la master private key et le chain code
##############

seed_bytes = binascii.unhexlify(hex_bin)
I = hmac.new(b"Bitcoin seed", seed_bytes, hashlib.sha512).digest()
L, R = I[:32], I[32:]

master_private_key = int.from_bytes(L, 'big')
master_chain_code = R

##############
#Extraire la master public key and private 
##############

seed = binascii.unhexlify(hex_bin)
I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
Il, Ir = I[:32], I[32:]  

secret = Il 
chain = Ir 
xprv = binascii.unhexlify("0488ade4") 
xpub = binascii.unhexlify("0488b21e")
depth = b"\x00" 
fpr = b'\0\0\0\0'
index = 0 
child = struct.pack('>L', index) 

k_priv = ecdsa.SigningKey.from_string(secret, curve=SECP256k1)
K_priv = k_priv.get_verifying_key()

data_priv = b'\x00' + (k_priv.to_string()) 

if K_priv.pubkey.point.y() & 1:
    data_pub= b'\3'+int_to_string(K_priv.pubkey.point.x())
else:
    data_pub = b'\2'+int_to_string(K_priv.pubkey.point.x())

raw_priv = xprv + depth + fpr + child + chain + data_priv
raw_pub = xpub + depth + fpr + child + chain + data_pub

hashed_xprv = hashlib.sha256(raw_priv).digest()
hashed_xprv = hashlib.sha256(hashed_xprv).digest()
hashed_xpub = hashlib.sha256(raw_pub).digest()
hashed_xpub = hashlib.sha256(hashed_xpub).digest()

raw_priv += hashed_xprv[:4]
raw_pub += hashed_xpub[:4]

#######################
#Full information root key (master public key, master private key...)
######################

root_key = bip32utils.BIP32Key.fromEntropy(seed)
root_address = root_key.Address()
root_public_hex = root_key.PublicKey().hex()
root_private_wif = root_key.WalletImportFormat()
print("\n--------------------------------")
print('Root key:')
print(f'\t{root_key.dump()}')

#######################
#Générer un clé enfant
######################

child_key = root_key.ChildKey(0).ChildKey(0)
child_address = child_key.Address()
child_public_hex = child_key.PublicKey().hex()
child_private_wif = child_key.WalletImportFormat()
print("\n--------------------------------")
print('Child key m/0/0:')
print(f'\t{child_key.dump()}')

#######################
#Générer une clé enfant à l’index N
######################

t = str(input("\nVoulez vous utiliser un index (sans niveau d'indexation) ? (y/n)"))
if (t=="y"):
    n = int(input("\nVeuillez choisir le niveau d'indexation ? "))
    print("Index choisi : ",n)
    i = 0
    for x in range(n):
        i=i+1
        child_key_son = root_key.ChildKey(0).ChildKey(i)
        child_address_son = child_key_son.Address()
        child_public_hex_son = child_key_son.PublicKey().hex()
        child_private_wif_son = child_key_son.WalletImportFormat()
        print("--------------------------------")
        print('Child key m/0/',i)
        print(f'\tAddress: {child_address_son}')
        print(f'\tPublic : {child_public_hex_son}')
        print(f'\tPrivate: {child_private_wif_son}\n')
        print(i)

#######################
#Générer une clé enfant à l’index N au niveau de dérivation M 
######################

else:
    n = int(input("\nVeuillez choisir le niveau d'indexation ? "))
    print("Index choisi : ",n)

    m = int(input("\nVeuillez choisir le niveau de dérivation ? "))
    print("Dérivation choisi : ",m)
    i = 0
    for x in range(n):
        i=i+1
        child_key_son = root_key.ChildKey(m).ChildKey(i)
        child_address_son = child_key_son.Address()
        child_public_hex_son = child_key_son.PublicKey().hex()
        child_private_wif_son = child_key_son.WalletImportFormat()
        print("--------------------------------")
        print('Child key m/',m,'/',i)
        print(f'\tAddress: {child_address_son}')
        print(f'\tPublic : {child_public_hex_son}')
        print(f'\tPrivate: {child_private_wif_son}\n')
        print(i)

#######################
#Information propre
######################
print("-------------------------------------")
print("Vous allez choisir toutes les informations que vous souhaitez récupérer.")
step1 = str(input("\nVoulez vous récupérer la private key? (y/n)"))
if(step1=="y"):
    print("private key : ",private_key)
print("-------------------------------------")
step2 = str(input("\nVoulez vous afficher la seed en lot de 11 bites? (y/n)"))
if(step2=="y"):
    print("Seed en lot : ",tab)
print("-------------------------------------")
step3 = str(input("\nVoulez vous afficher la phrase en mnémonique? (y/n)"))
if(step3=="y"):
    print("Phrase : ",phrase)
print("-------------------------------------")
step4 = str(input("\nVoulez vous afficher la seed BIP39? (y/n)"))
if(step4=="y"):
    print(f'BIP39 Seed: {seed_mnemonic.hex()}\n')
print("-------------------------------------")
step5 = str(input("\nVoulez vous afficher la master publique key et la master private key? (y/n)"))
if(step5=="y"):
    print("\nOnly public and private root keys:")
    print(f'\tPrivate : ,{base58.b58encode(raw_priv)}')
    print(f'\tPublic : ,{base58.b58encode(raw_pub)}')
    print(f'master chain code (bytes): {master_chain_code}')
print("-------------------------------------")
print("Merci pour votre confiance.")




