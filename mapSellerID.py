import json
import uuid


# Create a dictionary with hardcoded values
data = {
    "311": "0xb7a000c543ac7e39fdf4fc391b3900078e070325",
    "312": "0x1ef94bea1542da6d61c68f26f7a3933a240c87bd",
    "313": "0x710dd7f6e3e47ddc08fac4795694d7ec4506c4e6",
    "400": "0x977841f226482f7938e179f6fc6f45c175252114",
    "401": "0x3a11f0272dc8bc3842a7bc834e3e79bd474cf43a",
    "402": "0xdf2cdaf893d04b6032e941669f77086e9caf5d86",
    "403": "0x7926dad04fe7c482425d784985b5e24aea03c9ff",
    "404": "0x3121a6f0c30b0ab4c713fa66d3f369ac12d364fd",
    "405": "0x7ace0b7a0cfb2980aa25310af5c2602144d58db2",
    "406": "0x1e8ee48d0621289297693fc98914da2efdce1477",
    "407": "0x1d829bdbd534a70fdf27e959e790ef1d64e10ef8",
    "408": "0x88e50e06efb2b748e2b9670d2a6668237167382b"
}

# Function to assign a unique issuerId to each seller
def assign_issuer_id():
    for key in data:
        issuer_id = str(uuid.uuid4())
        data[key] = {"address": data[key], "issuerId": issuer_id}

# Call the function to assign issuerId to each seller
assign_issuer_id()

# Write the updated JSON data to sellerData.json
with open("sellerData.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data has been written to sellerData.json.")