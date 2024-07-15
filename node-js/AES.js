const { randomBytes, createCipheriv, createDecipheriv} = require('crypto');

class AESCipher {
  constructor() {
    this.key = randomBytes(32); // 256-bit key
    this.iv = randomBytes(16); // Initialization vector
  }

  encrypt(text) {
    const cipher = createCipheriv('aes-256-cbc', this.key, this.iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
  }

  decrypt(encryptedData) {
    const decipher = createDecipheriv('aes-256-cbc', this.key, this.iv);
    let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}

function example(){
  const myCipher = new AESCipher();
  const text = 'Hello World!';
  const encrypted = myCipher.encrypt(text);
  console.log(myCipher)
  console.log('Encrypted:', encrypted);

  const decrypted = myCipher.decrypt(encrypted);
  console.log('Decrypted:', decrypted);
  console.log(myCipher)
}

//example()

module.exports = { AESCipher }

