# Define the repeating_key_XOR function to encrypt text using a key
def repeating_key_XOR(text, key):
    # Initialize an empty bytearray to store the result of XOR operations
    result = bytearray()

    # Loop through each character in the input text
    for i in range(len(text)):
        # Get the current character from the text
        current_char = text[i]

        # Get the corresponding character from the key, repeating if necessary
        key_char = key[i % len(key)]

        # Perform XOR between the current character (converted to its ASCII value) and the key character
        byte = ord(current_char) ^ ord(key_char)

        # Append the result of XOR to the result bytearray
        result.append(byte)

        # Print the step-by-step XOR operation for debugging purposes (can be removed in production code)
        print(f"Char: {current_char} (hex: {ord(current_char):02x}) XOR {key_char} (hex: {ord(key_char):02x}) → {byte:02x}")

    # Return the result as a hexadecimal string representation
    return result.hex()

# Define the plaintext and key for encryption
plaintext = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
key = "ICE"

# Strip any leading/trailing whitespace from the plaintext (ensure consistency)
plaintext = plaintext.strip()

# Call the repeating_key_XOR function to encrypt the plaintext using the key
encrypted = repeating_key_XOR(plaintext, key)

# Print the final encrypted text in hexadecimal format
print(f"Encrypted hex: {encrypted}")

