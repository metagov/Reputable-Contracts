import json

# Create a dictionary with hardcoded values
data = {
  "11": "0xb7a000c543ac7e39fdf4fc391b3900078e070325",
  "12": "0x1ef94bea1542da6d61c68f26f7a3933a240c87bd",
  "13": "0x710dd7f6e3e47ddc08fac4795694d7ec4506c4e6"
}


# Define the output file path
output_file = 'sellerData.json'

# Write the dictionary to a JSON file
with open(output_file, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Data successfully written to {output_file}")
