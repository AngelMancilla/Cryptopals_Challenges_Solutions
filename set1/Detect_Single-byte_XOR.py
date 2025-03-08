# Define a function to perform XOR decryption on the byte string with a given key
def xor_decrypt(byte_str, key):
    """
    Performs XOR operation on each byte of the byte string with the provided key.
    
    Args:
    byte_str (bytes): The byte string to be decrypted.
    key (int): The XOR key (0-255) to decrypt the byte string.
    
    Returns:
    bytes: The decrypted byte string.
    """
    # Use a list comprehension to apply XOR to each byte in the byte string
    return bytes([byte ^ key for byte in byte_str])


# Open the file and process each line
with open('file_data/data4.txt', 'r') as f:
    # Process each line in the file
    for line in f:
        line = line.strip()  # Remove leading/trailing whitespace

        # Skip lines that don't have exactly 60 characters (as per the challenge requirement)
        if len(line) != 60:
            continue
        
        # Convert the hex string to a byte string
        byte_str = bytes.fromhex(line)

        # Try all possible keys (from 0 to 255) to decrypt the string
        for key in range(256):
            decrypted_text = xor_decrypt(byte_str, key)

            # Check if the decrypted text contains common words like " " (space) and "the"
            if b" " in decrypted_text and b"the" in decrypted_text:
                try:
                    # Attempt to decode the byte string into a human-readable string (utf-8)
                    decoded_str = decrypted_text.decode("utf-8")
                    # Print the key and the decrypted string once a valid result is found
                    print(f"Key: {key}, Decoded: {decoded_str}")
                    break  # Stop checking further keys for this line once a valid result is found
                except UnicodeDecodeError:
                    # If the result can't be decoded, skip it and try the next key
                    pass


