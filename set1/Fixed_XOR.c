#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Function to convert a hex character to an integer (0-15)
uint8_t hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') return c - '0';        // Convert '0'-'9' to 0-9
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;    // Convert 'a'-'f' to 10-15
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;    // Convert 'A'-'F' to 10-15
    return 0; // Return 0 for any invalid characters
}

// Function to convert a hex string to a byte array
void hex_to_bytes(const char *hex, uint8_t *bytes, size_t len) {
    // Iterate through the hex string and convert each pair of characters to a byte
    for (size_t i = 0; i < len; i++) {
        // Combine two hex characters (each representing 4 bits) into a byte
        bytes[i] = (hex_char_to_int(hex[i * 2]) << 4) | hex_char_to_int(hex[i * 2 + 1]);
    }
}

// Function to convert a byte array to a hex string
void bytes_to_hex(const uint8_t *bytes, char *hex, size_t len) {
    // Iterate through the byte array and convert each byte to two hex characters
    for (size_t i = 0; i < len; i++) {
        sprintf(hex + (i * 2), "%02x", bytes[i]); // Format each byte as two hex digits
    }
    hex[len * 2] = '\0'; // Null-terminate the string
}

// Function to XOR two hex strings and output the result as a hex string
void fixed_xor(const char *hex1, const char *hex2, char *output) {
    size_t len = strlen(hex1) / 2;  // Calculate the number of bytes (half the length of the hex string)

    // Allocate memory for byte arrays and result
    uint8_t *bytes1 = malloc(len);
    uint8_t *bytes2 = malloc(len);
    uint8_t *result = malloc(len);

    // Check for memory allocation errors
    if (!bytes1 || !bytes2 || !result) {
        printf("Memory allocation error.\n");
        return;
    }

    // Convert hex strings to byte arrays
    hex_to_bytes(hex1, bytes1, len);
    hex_to_bytes(hex2, bytes2, len);

    // Perform the XOR operation byte by byte
    for (size_t i = 0; i < len; i++) {
        result[i] = bytes1[i] ^ bytes2[i];
    }

    // Convert the result back to a hex string
    bytes_to_hex(result, output, len);

    // Free allocated memory
    free(bytes1);
    free(bytes2);
    free(result);
}

// Main function to read input and execute the XOR operation
int main() {
    char input1[1024], input2[1024];

    // Read the first hex string from user input
    printf("Enter hex string 1: ");
    if (fgets(input1, sizeof(input1), stdin) == NULL) {
        printf("Error reading input.\n");
        return 1;
    }
    input1[strcspn(input1, "\n")] = '\0';  // Remove the newline character

    // Read the second hex string from user input
    printf("Enter hex string 2: ");
    if (fgets(input2, sizeof(input2), stdin) == NULL) {
        printf("Error reading input.\n");
        return 1;
    }
    input2[strcspn(input2, "\n")] = '\0';  // Remove the newline character

    // Ensure both hex strings have the same length
    if (strlen(input1) != strlen(input2)) {
        printf("Error: Strings must have the same length.\n");
        return 1;
    }

    size_t len = strlen(input1); // Length of the hex string
    char *output = malloc(len + 1); // Allocate memory for the output hex string

    // Check for memory allocation error
    if (!output) {
        printf("Memory allocation error.\n");
        return 1;
    }

    // Perform the XOR operation
    fixed_xor(input1, input2, output);

    // Print the XOR result
    printf("XOR Result: %s\n", output);

    // Free allocated memory for the output
    free(output);

    return 0;
}

