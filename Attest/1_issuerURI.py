import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import uuid
import os
from dotenv import load_dotenv
load_dotenv('.env')

issuerDAOName= "TheFruitShop"
issuerURIPrefix = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/issuerURI/"

jsonBinAccessKey = os.getenv('JSONBIN_API')
url = 'https://api.jsonbin.io/v3/b'
headers = {
  'Content-Type': 'application/json',
  'X-Access-Key': jsonBinAccessKey,
  'X-Bin-Private' : "false",
  'X-Bin-Name': "issuerURI",
}

def publish_uri(json_data):
    # Get a reference to the 'issuerURI' collection in the  Database
    collection_ref = fdb.collection('issuerURI').document(issuerDAOName)
    doc_ref = collection_ref.set(json_data)
    print("Document published successfully. Document ID:", issuerDAOName)


    # Update the data in the 'issuerURI' in Realtime Database
    print("URI published successfully.")
    print(issuerURIPrefix + issuerDAOName)

# Initialize Firebase
cred = credentials.Certificate('Attest/serviceAccountKey.json')  # Replace with your own service account key
firebase_admin.initialize_app(cred)
# Create a reference to firestore
fdb = firestore.client()

# JSON-LD data
json_data = {
    "@context": "https://schema.org",
    "@type": "issuer",
    "name": "REPUTABLE",
    "description": "A on-chain service for reputation developed by the REPUTABLE team and the EU NGI's ONTOCHAIN project.",
    "memberAttestationsURI": "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/memberAttestationURI"
}

# Publish the URI to the 'issuerURI' collection in Firebase Realtime Database
publish_uri(json_data)
req = requests.post(url, json=json_data, headers=headers)
print(req.text)