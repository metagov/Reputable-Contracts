import json
gateway_compiled_path = '../src/abi/GatewayInterface.json'
with open(gateway_compiled_path) as file:
    gateway_json = json.load(file)  # load contract info as JSON
    gateway_abi = gateway_json['abi']
    print(gateway_abi)
