# Define the hexadecimal string to be decrypted
hex_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# Convert the hexadecimal string to bytes
byte_str = bytes.fromhex(hex_str)
# Define a function to perform XOR decryption on the byte string with a given key
def xor_decrypt(byte_str, key):
    """
    Decrypts a byte string using XOR with a given key.

    Args:
    byte_str (bytes): The encrypted byte string to decrypt.
    key (int): The XOR key (an integer between 0 and 255) used for decryption.

    Returns:
    bytes: The decrypted byte string after applying XOR with the key.
    """
    # Perform XOR operation for each byte in the byte string with the key
    return bytes([byte ^ key for byte in byte_str])


# Loop through all possible XOR keys from 0 to 255
for key in range(256):
    # Decrypt the byte string using the current XOR key
    decrypted_text = xor_decrypt(byte_str, key)
    
    try:
        # Attempt to decode the decrypted byte string into a human-readable string using UTF-8
        decoded_str = decrypted_text.decode("utf-8")
        
        # Check if the decoded string consists only of valid ASCII characters
        # and optionally contains the word "Cooking"
        if all([32 <= ord(c) < 127 for c in decoded_str]):
            # Print the key and decoded message if it's a valid ASCII string
            print(f"Key: {key}, Decoded: {decoded_str}")
    
    # Handle UnicodeDecodeError if decoding fails (e.g., invalid UTF-8 data)
    except UnicodeDecodeError:
        pass

