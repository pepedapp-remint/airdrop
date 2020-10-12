from collections import defaultdict
from typing import NamedTuple, Dict, List

from web3 import Web3


def hash_leaf(t) -> bytes:
    idx, sig, acct, count = t
    hb = Web3.solidityKeccak(['uint256', 'string', 'address', 'uint256'], [idx, sig, acct, count])
    return bytes(hb)


def combine_nodes(n1: bytes, n2: bytes) -> bytes:
    hb = Web3.solidityKeccak(['bytes32', 'bytes32'], [n1, n2])
    return bytes(hb)


def build_index_tuples():
    with open('data/ownership.csv', 'r') as f:
        reader = csv.reader(f)
        ownership_tuples = list(reader)

    index_tuples = []
    i = 0
    for t in ownership_tuples:
        index_tuples.append([i, t[0], t[1], int(t[2])])
        i += 1

    return index_tuples


class MerkleTree(NamedTuple):
    root: bytes
    leaf_to_branch: Dict[bytes, List[bytes]]


NULL_NODE = b'\x00' * 32


def build_tree(index_tuples) -> MerkleTree:
    leaves = [hash_leaf(t) for t in index_tuples]

    leaf_to_branch = defaultdict(list)

    cur_layer = leaves
    cur_layer_node_to_leaves = defaultdict(list)
    for leaf in leaves:
        cur_layer_node_to_leaves[leaf].append(leaf)

    while len(cur_layer) > 1:
        # construct next layer and add to branches at the same time
        next_layer = []
        for i in range(0, len(cur_layer), 2):
            n1 = cur_layer[i]
            n2 = cur_layer[i + 1] if i + 1 < len(cur_layer) else NULL_NODE

            n1_leaves = cur_layer_node_to_leaves[n1]
            for leaf in n1_leaves:
                leaf_to_branch[leaf].append(n2)

            n2_leaves = cur_layer_node_to_leaves[n2]
            for leaf in n2_leaves:
                leaf_to_branch[leaf].append(n1)

            p = combine_nodes(n1, n2)

            cur_layer_node_to_leaves[p].extend(n1_leaves + n2_leaves)
            next_layer.append(p)

        cur_layer = next_layer

    assert len(cur_layer) == 1

    return MerkleTree(cur_layer[0], dict(leaf_to_branch))
