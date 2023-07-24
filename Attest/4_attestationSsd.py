from datetime import datetime, timedelta
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import uuid
import os
from dotenv import load_dotenv
load_dotenv('.env')

issuerURI = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/issuerURI/TheFruitShop"
daoURIPrefix = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/DAOURI/"
attesterURI = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/memberAttestationURI"
completeAttestationURI = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/completeAttestationURI"
issuerName = ""
issuerId = uuid.uuid4()

# Initialize JSONBin

jsonBinAccessKey = os.getenv('JSONBIN_API')
url = 'https://api.jsonbin.io/v3/b'
headers = {
  'Content-Type': 'application/json',
  'X-Access-Key': jsonBinAccessKey,
  'X-Bin-Private' : "false",
  'X-Bin-Name': "completeAttestations",
}

# Initialize Firebase
# Replace with your own service account key
cred = credentials.Certificate('Attest/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Create a reference to firestore
fdb = firestore.client()

# Fetch the Ethereum addresses for sellers from the sellerMap.json file
with open('sellerData.json', 'r') as f:
    seller_map = json.load(f)

seller_ids = [11, 12, 13]


def publish_uri(json_data):
    # Get a reference to the 'completeAttestationStandard' collection in the  Database
    collection_ref = fdb.collection(
        'completeAttestationURI').document(ethereum_address)
    doc_ref = collection_ref.set(json_data)
    print("URI published successfully.")


# Fetch reputation and verify reputation for each seller
for seller_id in seller_ids:
    if str(seller_id) in seller_map:
        ethereum_address = seller_map[str(seller_id)]

        # Fetch reputation
        reputation_url = f'https://reputable-swagger-api.onrender.com/reputation?sellerId={seller_id}'
        reputation_response = requests.get(reputation_url)
        print(reputation_response)
        reputation = reputation_response.json()
        print(reputation)

        # Verify reputation
        verify_url = f'https://reputable-swagger-api.onrender.com/verify_reputation?sellerId={seller_id}'
        verify_response = requests.get(verify_url)
        print(verify_response)
        verify_reputation = verify_response.json()

        # Create attestationURI value
        attestation_uri = f"https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/memberAttestationsURI/{ethereum_address}"
        # Initialize The DAO URI, here its The Fruit Shop
        daoURI = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/DAOURI/TheFruitShop"
        # Calculate expiration date (1 week from the upload date)
        expiration_date = datetime.now() + timedelta(weeks=1)
        expiration_date_str = expiration_date.isoformat()

        # Store seller data in JSON-LD format with Ethereum address
        seller_data = {
            "@context": "http://www.daostar.org/schemas",
            "type": "arrayAttestation",
            "issuer": issuerURI,
            "member": {
                "type": "EthereumAddress",
                "id": ethereum_address
            },
            "organizations": [
                {
                    "expiration": expiration_date_str,
                    "attesterURI": attesterURI,
                    "name": "DAOstar One",
                    "daoURI": daoURI
                }
            ],
            "contributions": [
                {
                    "type": "contribution",
                    "referenceURI?": "",
                    "reference?": {
                        "version": "1.0",
                        "issuer": issuerName,
                        "issuerURI": issuerURI,
                        "issuerID": str(issuerId),
                        "title": "",
                        "description": "",
                        "category": "",
                        "contributors": [

                        ],
                        "contributorSignatures":[

                        ],
                        "dateOfEngagement": "",
                        "external": {
                            "govrn": {
                                "daoId": 1,
                                "bannerUrl": "https://hackmd.io/_uploads/HJnP_Zr9n.png"
                            }
                        }

                    }
                }
            ],
            "reputation": [
                {
                    "issuer": "REPUTABLE",
                    "issuerURI": issuerURI,
                    "issuerID": str(issuerId),
                    "internal_memberID": seller_id,
                    "score": verify_reputation['score'],
                    "proof": verify_reputation['hash'],
                    "expiration": expiration_date_str,
                    "dateOfEngagement": verify_reputation['timestamp'],
                },
            ]
        }

        # Save seller data to Firestore
        doc_ref = fdb.collection(
            'completeAttestationURI').document(ethereum_address)
        doc_ref.set(seller_data)

        print(f"Data for seller ID {seller_id} saved to Firestore.")

print("All seller data saved to Firestore.")

req = requests.post(url, json=seller_data, headers=headers)
print(req.text)
