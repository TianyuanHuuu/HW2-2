from web3 import Web3
from web3.providers.rpc import HTTPProvider
import requests
import json

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# Load ABI
with open('ape_abi.json', 'r') as f:
    abi = json.load(f)

api_url = "https://mainnet.infura.io/v3/8054c6b6305148d7be6d257adef7a4e6"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(ape_id):
    assert isinstance(ape_id, int), f"{ape_id} is not an int"
    assert 0 <= ape_id <= 9999, f"{ape_id} must be between 0 and 9,999"

    data = {'owner': "", 'image': "", 'eyes': ""}

    owner = contract.functions.ownerOf(ape_id).call()

    token_uri = contract.functions.tokenURI(ape_id).call()

    ipfs_hash = token_uri.replace("ipfs://", "")
    metadata_url = f"https://ipfs.io/ipfs/{ipfs_hash}"

    response = requests.get(metadata_url)
    metadata = response.json()

    image = metadata.get("image", "")
    attributes = metadata.get("attributes", [])
    eyes = next((trait["value"] for trait in attributes if trait["trait_type"] == "Eyes"), "")

    data['owner'] = owner
    data['image'] = image
    data['eyes'] = eyes

    assert isinstance(data, dict), f'get_ape_info({ape_id}) should return a dict'
    assert all(k in data for k in ['owner', 'image', 'eyes']), f"Return value must include keys: owner, image, eyes"
    return data
