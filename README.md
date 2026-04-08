# Stylus Merkle Airdrop

A gas-efficient airdrop contract built with Arbitrum Stylus (Rust → WASM), 
capable of verifying eligibility for 10,001 wallet addresses while storing 
only 32 bytes on-chain.

## How It Works

Instead of storing every eligible address in contract storage (expensive), 
this contract stores a single 32-byte Merkle Root — a cryptographic 
fingerprint of the entire eligibility list.

When a user wants to claim:
1. They generate a Merkle proof off-chain (Python script)
2. Submit the proof to `claim()`
3. The contract verifies it against the root in milliseconds
4. If valid and unclaimed → marked as claimed ✅

## Key Numbers

| Metric | Value |
|--------|-------|
| Contract size | 8.5 KB |
| Addresses supported | 10,001+ |
| On-chain storage | 32 bytes |
| Deployment cost | ~0.000079 ETH |
| Proof verification | ✅ Tested on-chain |

## Tech Stack

- **Rust** — contract logic
- **Arbitrum Stylus** — WASM runtime on Arbitrum
- **Python** — off-chain Merkle tree generation
- **Foundry (cast)** — on-chain testing

## Deployed Contract

- **Network:** Arbitrum Sepolia Testnet
- **Address:** `0x4ec8a2a51e92a0380c4f8bb53cf9b79aa005edaa`
- **Verified claim tx:** `0xc68fb18b2f8e8f5c5135e0e14657621aa5f7ecf8ad20e3115f97701dc7ca89e9`

## Contract Functions

| Function | Description |
|----------|-------------|
| `claim(bytes32[])` | Submit a Merkle proof to claim |
| `isClaimed(address)` | Check if an address has already claimed |
| `merkleRoot()` | Read the current Merkle root |
| `setMerkleRoot(bytes32)` | Set the Merkle root (owner action) |

## This Pattern Is Used By

- 🦄 Uniswap — UNI token airdrop (400,000 addresses)
- 🔵 ENS — governance token distribution
- 🟣 Arbitrum — ARB token airdrop (625,000 addresses)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate Merkle tree and proof
python3 generate_merkle.py

# Build and check contract
cargo stylus check --endpoint https://sepolia-rollup.arbitrum.io/rpc

# Deploy
cargo stylus deploy --endpoint https://sepolia-rollup.arbitrum.io/rpc --private-key $PRIVATE_KEY
```

⚠️ *Arbitrum Sepolia Testnet only — no real funds involved.*
