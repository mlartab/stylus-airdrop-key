#![cfg_attr(not(feature = "std"), no_std)]
extern crate alloc;

use alloc::vec::Vec;
use stylus_sdk::{prelude::*};

// This is the "Emergency Brake" required for Stylus
#[cfg(target_arch = "wasm32")]
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[storage]
#[entrypoint]
pub struct Airdrop {
    // Empty for now
}

#[public]
impl Airdrop {
    pub fn is_active(&self) -> Result<bool, Vec<u8>> {
        Ok(true)
    }
}