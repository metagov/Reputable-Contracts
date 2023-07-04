import json

# Create a dictionary with hardcoded values
data = {
    '11': '0xb7a000c543aC7E39fDf4fC391B3900078E070325',
    '12': '0x1eF94BEa1542da6d61c68f26f7a3933A240C87bD',
    '13': '0x710DD7f6e3e47Ddc08fac4795694d7ec4506C4e6',
}

# Define the output file path
output_file = 'sellerData.json'

# Write the dictionary to a JSON file
with open(output_file, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Data successfully written to {output_file}")
