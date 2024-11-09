use openssl::nid::Nid;
use openssl::pkey::{PKey, Private, Public};
use openssl::derive::Deriver;
use openssl::sign::{Signer, Verifier};
use aes_gcm::aead::{Aead, KeyInit, generic_array::GenericArray};
use aes_gcm::{Aes256Gcm, Nonce}; // AES-GCM 256-bit variant
use std::error::Error;
use openssl::ec::{EcGroup, EcKey, EcPoint};

pub struct EccKeyPair {
    private_key: PKey<Private>,
    public_key: PKey<Public>,
}

impl EccKeyPair {
    /// Generates a new ECC key pair
    pub fn generate() -> Result<Self, Box<dyn Error>> {
        let group = EcGroup::from_curve_name(Nid::SECP256K1)?;
        let ec_key = EcKey::generate(&group)?;
        let private_key = PKey::from_ec_key(ec_key.clone())?;
        let public_key = PKey::from_ec_key(EcKey::from_public_key(&group, ec_key.public_key())?)?;

        Ok(EccKeyPair { private_key, public_key })
    }

    /// Signs data using the private key
    pub fn sign(&self, data: &[u8]) -> Result<Vec<u8>, Box<dyn Error>> {
        let mut signer = Signer::new_without_digest(&self.private_key)?;
        signer.update(data)?;
        let signature = signer.sign_to_vec()?;
        Ok(signature)
    }

    /// Verifies a signature using the public key
    pub fn verify(&self, data: &[u8], signature: &[u8]) -> Result<bool, Box<dyn Error>> {
        let mut verifier = Verifier::new_without_digest(&self.public_key)?;
        verifier.update(data)?;
        Ok(verifier.verify(signature)?)
    }

    /// Derives a shared secret using ECDH
    pub fn derive_shared_secret(&self, peer_public_key: &PKey<Public>) -> Result<Vec<u8>, Box<dyn Error>> {
        let mut deriver = Deriver::new(&self.private_key)?;
        deriver.set_peer(peer_public_key)?;
        let shared_secret = deriver.derive_to_vec()?;
        Ok(shared_secret)
    }

    /// Encrypts data using AES-GCM with a derived shared secret
    pub fn encrypt(&self, peer_public_key: &PKey<Public>, plaintext: &[u8]) -> Result<Vec<u8>, aes_gcm::Error> {
        let shared_secret = self.derive_shared_secret(peer_public_key).map_err(|_| aes_gcm::Error)?;
        let key = GenericArray::from_slice(&shared_secret[..32]);
        let cipher = Aes256Gcm::new(key);
        let nonce = Nonce::from_slice(&[0u8; 12]);
        let ciphertext = cipher.encrypt(nonce, plaintext)?;

        Ok([nonce.as_slice(), &ciphertext].concat())
    }

    /// Decrypts data using AES-GCM with a derived shared secret
    pub fn decrypt(&self, peer_public_key: &PKey<Public>, ciphertext_with_nonce: &[u8]) -> Result<Vec<u8>, aes_gcm::Error> {
        let shared_secret = self.derive_shared_secret(peer_public_key).map_err(|_| aes_gcm::Error)?;
        let key = GenericArray::from_slice(&shared_secret[..32]);
        let cipher = Aes256Gcm::new(key);
        let (nonce, ciphertext) = ciphertext_with_nonce.split_at(12);
        let plaintext = cipher.decrypt(Nonce::from_slice(nonce), ciphertext)?;

        Ok(plaintext)
    }

    /// Returns the public key as a point
    pub fn public_key_point(&self) -> Result<EcPoint, Box<dyn Error>> {
        let ec_key = self.public_key.ec_key()?;
        let group = EcGroup::from_curve_name(Nid::SECP256K1)?;
        Ok(ec_key.public_key().to_owned(&group)?)
    }
    

    /// Exports the public key in uncompressed format
    pub fn public_key_bytes(&self) -> Result<Vec<u8>, Box<dyn Error>> {
        let group = EcGroup::from_curve_name(Nid::SECP256K1)?;
        let mut ctx = openssl::bn::BigNumContext::new()?;
        let point = self.public_key_point()?;
        let buf = point.to_bytes(&group, openssl::ec::PointConversionForm::UNCOMPRESSED, &mut ctx)?;
        Ok(buf)
    }
    
}

fn main() -> Result<(), aes_gcm::Error> {
    let alice_keypair = EccKeyPair::generate().expect("Failed to generate key pair");
    let bob_keypair = EccKeyPair::generate().expect("Failed to generate key pair");

    let message = b"Hello, Bob!";
    let ciphertext = alice_keypair.encrypt(&bob_keypair.public_key, message)?;
    println!("Ciphertext: {:?}", ciphertext);

    let decrypted_message = bob_keypair.decrypt(&alice_keypair.public_key, &ciphertext)?;
    println!("Decrypted message: {:?}", String::from_utf8(decrypted_message).expect("Failed to convert to UTF-8"));
    
    // Generate ECC key pair
    let ecc_keypair = EccKeyPair::generate().expect("Failed to generata key pair");

        // Message to be signed
    let message = b"Hello, ECC!";
    
    // Sign the message
    let signature = ecc_keypair.sign(message).expect("signature failed");
    println!("Signature: {:?}", signature);
    
    // Verify the signature
    let is_valid = ecc_keypair.verify(message, &signature).expect("verification failed");
    println!("Signature valid: {}", is_valid);

    Ok(())
}
