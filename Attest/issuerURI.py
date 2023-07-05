import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

issuerURIPrefix = "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/issuerURI/"
def publish_uri(json_data):
    # Get a reference to the 'issuerURI' collection in the  Database
    collection_ref = fdb.collection('issuerURI')
    doc_ref = collection_ref.add(json_data)
    print("Document published successfully. Document ID:", doc_ref[1].id)


    # Update the data in the 'issuerURI' in Realtime Database
    print("URI published successfully.")
    print(issuerURIPrefix + doc_ref[1].id)

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
    "memberAttestationsURI": "https://firestore.googleapis.com/v1/projects/reputable-f7202/databases/(default)/documents/memberAttestationsURI"
}

# Publish the URI to the 'issuerURI' collection in Firebase Realtime Database
publish_uri(json_data)
