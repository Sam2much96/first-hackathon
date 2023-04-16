import json
import hashlib

def GenerateTEAL(filename: str) -> str:

    with open(filename, 'r') as f:
        data = json.load(f)

    # Extract necessary data from the JSON file
    call_configs = []
    for interface in data['Interfaces']:
        for method in interface['methods']:
            call_configs.extend(method['call_config'])

    # Use the extracted data to build the TEAL smart contract template string
    template = f"""# TEAL smart contract template generated from {filename}


    {json.dumps(call_configs, indent=4)}

    """
    return template


# For Local Testing
#if __name__ == "__main__":
#    print(GenerateTEAL("Test1.json"))
