# Cryptopals Crypto Challenge Set 1

This is the first set of challenges from the **Cryptopals Crypto Challenges**, designed to introduce you to the basics
of cryptography and binary data manipulation. This set is intended to ramp you up gradually into coding cryptography,
while also serving as a qualification to ensure you're ready for more advanced challenges ahead.

## Challenges

The following challenges are included in **Set 1**:

1. **Convert hex to base64**  
   Implement a function that converts a hex-encoded string to base64. This will help you understand basic encoding
   techniques.

2. **Fixed XOR**  
   Implement a function that takes two equal-length hex-encoded strings and returns the result of applying the XOR
   operation to each byte.

3. **Single-byte XOR cipher**  
   Implement a function that encrypts a message using a single-byte XOR cipher. Then, find the key used to encrypt the
   given message by trying all possible single-byte keys.

4. **Detect single-character XOR**  
   Given a list of hex-encoded strings, identify which one was encoded using a single-byte XOR cipher. This will require
   detecting patterns typical of XOR encryption.

5. **Implement repeating-key XOR**  
   Implement a function that encrypts a message using the repeating-key XOR cipher. This is a simple cipher, but
   important for understanding how stream ciphers work.

6. **Break repeating-key XOR**  
   Given a repeating-key XOR encrypted ciphertext, attempt to break the cipher and recover the plaintext. You'll need to
   use frequency analysis and other techniques to solve this.

7. **AES in ECB mode**  
   Implement AES encryption in ECB mode. AES is one of the most widely used symmetric encryption algorithms, and
   understanding ECB mode is key to understanding how block ciphers work.

8. **Detect AES in ECB mode**  
   Given a list of ciphertexts, detect which ones are encrypted using AES in ECB mode. You'll need to look for patterns
   in the ciphertext that reveal the use of ECB.

## Notes

- Some of these exercises will require you to manipulate binary data and work with hex-encoded strings, so be sure to
  understand how to convert between different data representations (hex, base64, ASCII, etc.).
- While this set is relatively simple, many of the challenges are designed to provide foundational knowledge for the
  more complex challenges to come. Don’t rush through them!

---

You can find the solutions to these challenges in the respective files in this repository, each written in **C**.

Happy coding!!!