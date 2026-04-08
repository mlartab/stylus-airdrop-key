import json
from eth_utils import keccak

def get_leaf(address):
    # Match contract: keccak of raw 20 bytes
    return keccak(bytes.fromhex(address[2:]))

def hash_pair(a, b):
    # Match contract: always put smaller first
    if a <= b:
        return keccak(a + b)
    else:
        return keccak(b + a)

def build_tree(leaves):
    nodes = sorted(leaves)
    tree = [list(nodes)]
    while len(nodes) > 1:
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])
        nodes = [hash_pair(nodes[i], nodes[i+1]) for i in range(0, len(nodes), 2)]
        tree.append(list(nodes))
    return tree

def get_proof(tree, leaf_index):
    proof = []
    index = leaf_index
    for level in tree[:-1]:
        if len(level) % 2 != 0:
            level = level + [level[-1]]
        sibling = index ^ 1
        if sibling < len(level):
            proof.append(level[sibling])
        index //= 2
    return proof

with open('addresses.txt', 'r') as f:
    addresses = [line.strip() for line in f if line.strip()]

leaves = [get_leaf(addr) for addr in addresses]
tree = build_tree(leaves)
root = tree[-1][0]

print(f"DONE! Processed {len(addresses)} addresses.")
print(f"Merkle Root: 0x{root.hex()}")

# Generate proof for your wallet address
test_address = "0xFaE9cEe9A627E64F3Bec462159828bfbfBB872E7"
test_leaf = get_leaf(test_address)
sorted_leaves = sorted(leaves)
test_index = sorted_leaves.index(test_leaf)
proof = get_proof(tree, test_index)

print(f"\n--- Test Proof ---")
print(f"Address: {test_address}")
print(f"Proof ({len(proof)} elements):")
for i, p in enumerate(proof):
    print(f"  [{i}] 0x{p.hex()}")

proof_data = {
    "address": test_address,
    "root": f"0x{root.hex()}",
    "proof": [f"0x{p.hex()}" for p in proof]
}
with open('proof.json', 'w') as f:
    json.dump(proof_data, f, indent=2)
print(f"\nProof saved to proof.json")