import csv
import json

from web3 import Web3

INFURA_URI = 'https://mainnet.infura.io/v3/46e1129337704902bc55c7b1f3315a72'
w3 = Web3(Web3.HTTPProvider(INFURA_URI))

PEPE_CORE_ADDRESS = '0xE4Bd56Cbf537074e3836a1721983107cce9e689F'
with open('PepeCore.json') as f:
    pepe_core_data = json.load(f)
    pepe_core_abi = pepe_core_data['abi']
pepe_core = w3.eth.contract(address=PEPE_CORE_ADDRESS, abi=pepe_core_abi)


def load_tx_rows():
    # pickled in tx_rows.p
    tx_rows = []
    with open('data/transactions.csv') as f:
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            to_address = row[3]
            fn_call = pepe_core.decode_function_input(row[4])
            fn_name = fn_call[0].fn_name
            fn_args = fn_call[1]
            tx_rows.append((to_address, fn_name, fn_args))
    return tx_rows

# TODO: load tx_rows.p and simulate!
