# decode function from tx input using contract!
# 1. [DONE] set up w3 w/infura
# 2. [DONE] load contract in with ABI found in PepeCore.json
# 3. [DONE] try decoding a function call from transactions.csv
# 4. simulate txes in order for drop!
import json

from web3 import Web3

INFURA_URI = 'https://mainnet.infura.io/v3/46e1129337704902bc55c7b1f3315a72'
w3 = Web3(Web3.HTTPProvider(INFURA_URI))

PEPE_CORE_ADDRESS = '0xE4Bd56Cbf537074e3836a1721983107cce9e689F'
with open('PepeCore.json') as f:
    pepe_core_data = json.load(f)
    pepe_core_abi = pepe_core_data['abi']
pepe_core = w3.eth.contract(address=PEPE_CORE_ADDRESS, abi=pepe_core_abi)

TRANSACTIONS_FILE = 'data/transactions.csv'
