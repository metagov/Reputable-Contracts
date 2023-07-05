import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

# Initialize Firebase SDK
cred = credentials.Certificate('Attest/serviceAccountKey.json')  # Replace with your own service account key
firebase_admin.initialize_app(cred)

# Fetch the Ethereum addresses for sellers from the sellerMap.json file
with open('sellerData.json', 'r') as f:
    seller_map = json.load(f)

seller_ids = [11, 12, 13]

# Create Firestore client
db = firestore.client()

# Fetch reputation and verify reputation for each seller
for seller_id in seller_ids:
    if str(seller_id) in seller_map:
        ethereum_address = seller_map[str(seller_id)]

        # Fetch reputation
        reputation_url = f'http://localhost:5000/reputation?sellerId={seller_id}'
        reputation_response = requests.get(reputation_url)
        print(reputation_response)
        reputation = reputation_response.json()
        print(reputation)

        # Verify reputation
        verify_url = f'http://localhost:5000/verify_reputation?sellerId={seller_id}'
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
            "type": "membershipAttestation",
            "id": ethereum_address,
            "internale_memberID": seller_id,
            "reputation": reputation['score'],
             "verify_reputation": {
                "score": verify_reputation['score'],
                "timestamp": verify_reputation['timestamp'],
                "hash": verify_reputation['hash']
            },
            "attestationURI": attestation_uri,
            "expiration_date": expiration_date_str,
            "daoURI": daoURI
        }

        # Save seller data to Firestore
        doc_ref = db.collection('memberAttestationURI').document(ethereum_address)
        doc_ref.set(seller_data)

        print(f"Data for seller ID {seller_id} saved to Firestore.")

print("All seller data saved to Firestore.")
