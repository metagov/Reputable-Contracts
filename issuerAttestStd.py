import json

# Load the logged data from the file
with open("off-chain.json", "r") as file:
    logged_data = json.load(file)

# Define the JSON-LD context
context = {
    "@context": {
        "schema": "http://schema.org/",
        "seller": "schema:Organization",
        "user": "schema:Person",
        "score": "schema:Rating",
        "timestamp": "schema:DateTime",
        "transactionHash": "schema:Text"
    }
}

# Create an empty JSON-LD document
json_ld = {}

# Add the context to the JSON-LD document
json_ld.update(context)

# Process each logged data entry
for entry in logged_data["data"]:
    # Create a new JSON-LD object for each entry
    data_entry = {
        "@type": "schema:Review",
        "seller": {
            "@type": "seller",
            "seller_id": entry["seller_id"]
        },
        "user": {
            "@type": "user",
            "user_id": entry["user_id"]
        },
        "score": {
            "@type": "score",
            "value": entry["individual_score"]
        },
        "timestamp": {
            "@type": "timestamp",
            "value": entry["Timestamp"]
        },
        "transactionHash": {
            "@type": "transactionHash",
            "value": entry["tx_hash"]
        }
    }
    
    # Add the data entry to the JSON-LD document
    json_ld.update(data_entry)

# Convert the JSON-LD document to a JSON string
json_ld_str = json.dumps(json_ld, indent=4)

# Print the JSON-LD string
print(json_ld_str)
