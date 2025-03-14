import string

# English character frequencies
english_freq = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.0236, 'x': 0.0015,
    'y': 0.01974, 'z': 0.00074, ' ': 0.13000  # Space
}

# Function to calculate Hamming distance (number of differing bits)
def hamming_distance(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        raise ValueError(f"Byte strings must be of equal length, but got lengths {len(bytes1)} and {len(bytes2)}")
    
    distance = 0
    for byte1, byte2 in zip(bytes1, bytes2):
        xor = byte1 ^ byte2  # XOR to find differing bits
        distance += bin(xor).count('1')  # Count the number of 1s (differing bits)
    return distance

# Function to find the key size (KEYSIZE) using normalized Hamming distance
def find_keysize(ciphertext_hex, min_size=2, max_size=40):
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)  # Convert hex to bytes
    
    best_size = None
    best_distance = float('inf')  # Initialize with a large value
    
    # Try key sizes from min_size to max_size
    for size in range(min_size, max_size + 1):
        # Split ciphertext into blocks of KEYSIZE
        blocks = [ciphertext_bytes[i:i+size] for i in range(0, len(ciphertext_bytes), size)]
        blocks = [block for block in blocks if len(block) == size]  # Keep only full blocks
        
        # Skip if there are less than 2 blocks to compare
        if len(blocks) < 2:
            continue  
        
        total_distance = 0
        comparisons = 0
        
        # Compare all pairs of blocks
        for i in range(len(blocks) - 1):
            for j in range(i + 1, len(blocks)):
                total_distance += hamming_distance(blocks[i], blocks[j])
                comparisons += 1
        
        # Skip if no comparisons were made
        if comparisons == 0:
            continue
        
        # Calculate average Hamming distance and normalize by KEYSIZE
        avg_distance = total_distance / comparisons
        normalized_distance = avg_distance / size
        
        # Update best KEYSIZE if this one is better
        if normalized_distance < best_distance:
            best_distance = normalized_distance
            best_size = size
    
    return best_size

# Function to transpose blocks (group bytes by their position in the block)
def transpose_blocks(ciphertext_bytes, keysize):
    # Split ciphertext into blocks of KEYSIZE
    blocks = [ciphertext_bytes[i:i+keysize] for i in range(0, len(ciphertext_bytes), keysize)]
    # Create empty bytearrays for each position in the block
    transposed_blocks = [bytearray() for _ in range(keysize)]
    
    # Fill transposed_blocks with bytes from their respective positions
    for block in blocks:
        for i in range(len(block)):
            transposed_blocks[i].append(block[i])  
    
    return transposed_blocks

# Function to calculate chi-squared score for frequency analysis
def chi_squared_score(text, english_freq):
    score = 0
    text = text.lower()  # Convert text to lowercase for comparison
    total_chars = len(text)
    
    # Calculate observed frequency of each character
    observed_freq = {}
    for char in text:
        if char in observed_freq:
            observed_freq[char] += 1
        else:
            observed_freq[char] = 1
    
    # Calculate chi-squared score
    for char in observed_freq:
        if char in english_freq:
            observed = observed_freq[char] / total_chars  # Observed frequency
            expected = english_freq[char]  # Expected frequency
            score += ((observed - expected) ** 2) / expected  # Chi-squared formula
        else:
            # Penalize characters not in english_freq
            score += 1 
    
    return score

# Main function to break repeating-key XOR
def break_repeating_key_xor(ciphertext_hex):
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)  # Convert hex to bytes
    
    # Step 1: Find the key size (KEYSIZE)
    keysize = find_keysize(ciphertext_hex)
    print(f"Probable keysize: {keysize}")
    
    # Step 2: Transpose the blocks
    transposed_blocks = transpose_blocks(ciphertext_bytes, keysize)
    
    # Step 3: Find the key byte by byte
    key = bytearray()
    for block in transposed_blocks:
        best_key_byte = None
        best_score = float('inf')
        
        # Try all possible key bytes (0 to 255)
        for key_byte in range(256):
            try:
                # Decrypt the block with the candidate key byte
                decrypted_block = bytes([byte ^ key_byte for byte in block])
                decrypted_text = decrypted_block.decode('utf-8', errors='replace')
                # Calculate chi-squared score for frequency analysis
                score = chi_squared_score(decrypted_text, english_freq)
                
                # Update best key byte if this one is better
                if score < best_score:
                    best_score = score
                    best_key_byte = key_byte
            except UnicodeDecodeError:
                # Skip if decoding fails
                continue
        
        # Add the best key byte to the key
        key.append(best_key_byte)
    
    # Step 4: Decrypt the message with the found key
    decrypted_message = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_message.append(ciphertext_bytes[i] ^ key[i % len(key)])
    
    return key, decrypted_message.decode('utf-8', errors='replace')

# Example usage
