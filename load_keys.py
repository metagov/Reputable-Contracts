# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 02:05:17 2021

@author: prince
"""
#2 LOADS THE KEYS AND THE VALUES AND DECRYPTS THEM
import json
import phe
from phe import paillier

def keypair_load_pyp(pub_jwk, priv_jwk):
    """Deserializer for public-private keypair, from JWK format."""
    rec_pub = json.loads(pub_jwk)
    rec_priv = json.loads(priv_jwk)
    pub_n = phe.util.base64_to_int(rec_pub['n'])
    pub = paillier.PaillierPublicKey(pub_n)
    priv_p = phe.util.base64_to_int(rec_priv['p'])
    priv_q = phe.util.base64_to_int(rec_priv['q'])
    priv = paillier.PaillierPrivateKey(pub, priv_p, priv_q)
    return pub, priv

with open("phe_key.pub", "r") as f:
     pub_jwk = f.read()

with open("phe_private_key.priv", "r") as f:
     priv_jwk = f.read()

pubkey, privkey = keypair_load_pyp(pub_jwk, priv_jwk)
#load_enc nums
with open("encrypted.json", "r") as f:
        data = f.read()
        data_js = json.loads(data)
        aggr = pubkey.encrypt(0)
        
# for k, v in data_js.items():
#     aggr += paillier.EncryptedNumber(pubkey, v)
a = 863577359994820004195565706512856685772966125189821800244966794431644731403633523118319272256868062390757565531259494709182662245467783045092913690488024
b = paillier.EncryptedNumber(pubkey, a)
print("decrypted score: ", privkey.decrypt(b))