#![cfg_attr(not(feature = "export-abi"), no_main)]
extern crate alloc;

use alloc::vec::Vec;
use stylus_sdk::{
    alloy_primitives::{Address, FixedBytes},
    crypto::keccak,
    prelude::*,
};

sol_storage! {
    #[entrypoint]
    pub struct Airdrop {
        mapping(address => bool) claimed;
        bytes32 merkle_root;
    }
}

#[public]
impl Airdrop {
    pub fn claim(&mut self, proof: Vec<FixedBytes<32>>) -> Result<bool, Vec<u8>> {
        let user: Address = stylus_sdk::msg::sender();

        if self.claimed.get(user) {
            return Ok(false);
        }

        let mut computed_hash: FixedBytes<32> = keccak(user.as_slice()).into();

        for element in &proof {
            let element_bytes: FixedBytes<32> = *element;
            let mut data = [0u8; 64];

            if computed_hash <= element_bytes {
                data[..32].copy_from_slice(computed_hash.as_slice());
                data[32..].copy_from_slice(element_bytes.as_slice());
            } else {
                data[..32].copy_from_slice(element_bytes.as_slice());
                data[32..].copy_from_slice(computed_hash.as_slice());
            }

            computed_hash = keccak(&data).into();
        }

        if computed_hash == self.merkle_root.get() {
            self.claimed.insert(user, true);
            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub fn is_claimed(&self, user: Address) -> Result<bool, Vec<u8>> {
        Ok(self.claimed.get(user))
    }

    pub fn merkle_root(&self) -> Result<FixedBytes<32>, Vec<u8>> {
        Ok(self.merkle_root.get())
    }
}