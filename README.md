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

## This Pattern Is Used By

- 🦄 Uniswap — UNI token airdrop (400,000 addresses)
- 🔵 ENS — governance token distribution
- 🟣 Arbitrum — ARB token airdrop (625,000 addresses)

## 🛠 Troubleshooting & Environment Stability

This project uses **Stylus SDK 0.6.0** which can be sensitive to transitive 
dependency updates. If you encounter `rustc` version errors or WASM evaluation 
panics during `cargo stylus check`, follow these steps:

### 1. Pin the Toolchain
```bash
rustup override set 1.82.0
```

### 2. Fix Dependency Conflicts

**Fix `unicode-segmentation` (MSRV issue):**
```bash
cargo update -p unicode-segmentation --precise 1.12.0
```

**Fix `ruint` (WASM evaluation panic):**
```bash
cargo update -p ruint --precise 1.12.3
```

### 3. Verify Everything Works
```bash
cargo stylus check --endpoint https://sepolia-rollup.arbitrum.io/rpc
```

You should see:
contract size: 8.5 KB (8518 bytes)
wasm data fee: 0.000079 ETH

### Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `BYTES must be equal to Self::BYTES` | Run `cargo update -p ruint --precise 1.12.3` |
| `unicode-segmentation requires rustc 1.85.0` | Run `cargo update -p unicode-segmentation --precise 1.12.0` |
| `missing an entrypoint` | Ensure `#[entrypoint]` is inside `sol_storage!` macro |
| `#[public] not found` | You are on sdk 0.4.x — upgrade to `stylus-sdk = "=0.6.0"` |
| `--locked` error | Delete `Cargo.lock` and run `cargo generate-lockfile` |

## License

MIT

⚠️ *Arbitrum Sepolia Testnet only — no real funds involved.*