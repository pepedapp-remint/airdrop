import csv
import json
from typing import NamedTuple, Dict, List

from web3 import Web3

INFURA_URI = 'https://mainnet.infura.io/v3/46e1129337704902bc55c7b1f3315a72'
w3 = Web3(Web3.HTTPProvider(INFURA_URI))

PEPE_CORE_ADDRESS = '0xE4Bd56Cbf537074e3836a1721983107cce9e689F'
ADMIN_ADDRESS = '0xf7dBFe7dcFBA501464008554e7c5EddE8ab7B0ff'
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
            from_address = row[3]
            fn_call = pepe_core.decode_function_input(row[4])
            fn_name = fn_call[0].fn_name
            fn_args = fn_call[1]
            tx_rows.append((from_address, fn_name, fn_args))
    return tx_rows


Address = str
Sig = str


class Sale(NamedTuple):
    seller: Address
    price: int


class PepeState(NamedTuple):
    ownership: Dict[Address, Dict[Sig, int]]
    sales: Dict[Sig, List[Sale]]


def get_all_sigs():
    return pepe_core.functions.getAllSigs().call()


def get_sig_count(sig: Sig):
    return pepe_core.functions.getNumSigs(sig).call()


def load_initial_state():
    # sigs =
    ...


# State =
# sales: sig -> list of (price, seller)
# owner -> sig -> count

# TODO: load tx_rows.p and simulate! Note that I'm only going over *successful* txes here
# Should seed ownership map with root owner owning all cards
# Methods to simulate:
# - createSale(sig, price)
# - removeSale(sig)
# - buy(sig)
# - transferSig(sig)
