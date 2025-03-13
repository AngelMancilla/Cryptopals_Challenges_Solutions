import base64
import binascii

def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError(f"Strings must be of equal length, but got lengths {len(str1)} and {len(str2)}")
    
    byte_str1 = str1.encode()
    byte_str2 = str2.encode()

    distance = 0

    for byte1, byte2 in zip(byte_str1, byte_str2):
        if byte1 != byte2:
            distance += 1 

    return distance

def find_keysize(ciphertext, min_size=2, max_size=10):
    best_size = None
    best_distance = float('inf') 
    for size in range(min_size, max_size + 1):
        distances = []
        
        blocks = [ciphertext[i:i + size] for i in range(0, len(ciphertext), size)]
        
        if len(blocks) > 1 and len(blocks[-1]) == size:
            for i in range(len(blocks) - 1):
                hamming_dist = hamming_distance(blocks[i], blocks[i + 1])
                distances.append(hamming_dist)
            
            average_distance = sum(distances) / len(distances)
            normalized_hamming = average_distance / size
            
            if normalized_hamming < best_distance:
                best_distance = normalized_hamming
                best_size = size
    
    return best_size

ciphertext = "090c0f2f2c0e442645042e0c09400c"  #"Hello, world!", KEY =  "ABC", KEYSIZE = 3

keysize = find_keysize(ciphertext)

print(keysize)

# with open('file_data/data6.txt', 'r') as f:
#     for line in f:
        
#         line = line.strip()

#         data = base64.b64decode(line)
        
#         print(f"data: {data}\n")