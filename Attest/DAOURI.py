import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
daoName="TheFruitShop"
daoURIPrefix = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/DAOURI/"
issuerURI = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/issuerURI/TheFruitShop"
def publish_uri(json_data):
    # Get a reference to the 'DAOURI' collection in the  Database
    collection_ref = fdb.collection('DAOURI').document(daoName)
    doc_ref = collection_ref.set(json_data)
    print("Document published successfully. Document ID:" + daoName, )


    print("URI published successfully.")
    print(daoURIPrefix + daoName)

# Initialize Firebase
cred = credentials.Certificate('Attest/serviceAccountKey.json')  # Replace with your own service account key
firebase_admin.initialize_app(cred)
# Create a reference to firestore
fdb = firestore.client()

# JSON-LD data
json_data = {
    "@context": "<http://www.daostar.org/schemas>",
    "type": "DAO",
    "name": "The Fruit Shop",
    "description": "This a fruit shop aggregator that allows different sellers to sell fruits on our platform",
    "issuerURI": issuerURI
}


publish_uri(json_data)
