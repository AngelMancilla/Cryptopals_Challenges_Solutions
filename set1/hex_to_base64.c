#include <ctype.h>  // For character handling functions (toupper, isxdigit)
#include <stdio.h>  // For input/output functions (printf, fgets)
#include <stdlib.h> // For memory allocation functions (malloc, free)
#include <string.h> // For string manipulation functions (strlen, strncat, strncpy)

const char base64_chars[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  // Uppercase alphabet
    "abcdefghijklmnopqrstuvwxyz"  // Lowercase alphabet
    "0123456789+/";  // Digits and Base64-specific characters

// Function to convert a hexadecimal character to its 4-bit binary equivalent
const char *hex_to_bin(char hex) {
    switch (toupper(hex)) {  // Convert the hex character to uppercase for consistency
        case '0': return "0000";
        case '1': return "0001";
        case '2': return "0010";
        case '3': return "0011";
        case '4': return "0100";
        case '5': return "0101";
        case '6': return "0110";
        case '7': return "0111";
        case '8': return "1000";
        case '9': return "1001";
        case 'A': return "1010";
        case 'B': return "1011";
        case 'C': return "1100";
        case 'D': return "1101";
        case 'E': return "1110";
        case 'F': return "1111";
        default: return NULL;  // If the character is not valid hex, return NULL
    }
}

// Function to convert a binary string to its decimal equivalent
int bin_to_decimal(const char *bin) {
    int decimal = 0;
    // Iterate through each bit in the binary string
    for (int i = 0; bin[i] != '\0'; i++) {
        decimal = decimal * 2 + (bin[i] - '0');  // Shift left and add the current bit
    }
    return decimal;
}

// Function to convert a hexadecimal string to a Base64-encoded string
void hex_to_base64(const char *hex_str) {
    size_t hex_len = strlen(hex_str);  // Get the length of the hexadecimal string
    size_t bin_size = hex_len * 4 + 1;  // Allocate space for the binary representation (4 bits per hex character)
    char *bin_str = malloc(bin_size);  // Allocate memory for the binary string
    if (bin_str == NULL) {  // If memory allocation fails, exit the function
        printf("Memory allocation error.\n");
        return;
    }
    bin_str[0] = '\0';  // Initialize the binary string as empty

    // Convert each hexadecimal character to its binary equivalent
    for (size_t i = 0; i < hex_len; i++) {
        const char *bin = hex_to_bin(hex_str[i]);
        if (bin == NULL) {  // If the character is not a valid hex, print an error and return
            printf("Error: Invalid hexadecimal character.\n");
            free(bin_str);
            return;
        }
        strncat(bin_str, bin, bin_size - strlen(bin_str) - 1);  // Append the binary representation to the binary string
    }

    size_t bin_len = strlen(bin_str);  // Get the length of the binary string
    size_t base64_len = ((bin_len + 5) / 6) * 4 + 1;  // Calculate the required length for the Base64 string
    char *base64_str = malloc(base64_len);  // Allocate memory for the Base64 string
    if (base64_str == NULL) {  // If memory allocation fails, exit the function
        printf("Memory allocation error.\n");
        free(bin_str);
        return;
    }

    int index = 0;
    // Process the binary string in chunks of 6 bits
    for (size_t i = 0; i < bin_len; i += 6) {
        char temp[7] = "000000";  // Temporary buffer to hold a 6-bit chunk (initialize with zeros)
        int bits_to_copy = (bin_len - i < 6) ? (bin_len - i) : 6;  // Determine how many bits to copy
        strncpy(temp, &bin_str[i], bits_to_copy);  // Copy the current 6-bit chunk into the temporary buffer
        temp[bits_to_copy] = '\0';  // Null-terminate the string

        // If the chunk is smaller than 6 bits, pad with zeros
        if (bits_to_copy < 6) {
            for (int j = bits_to_copy; j < 6; j++) {
                temp[j] = '0';
            }
        }

        int decimal = bin_to_decimal(temp);  // Convert the 6-bit chunk to decimal
        base64_str[index++] = base64_chars[decimal];  // Map the decimal value to the corresponding Base64 character
    }

    // Add padding ('=') to the Base64 string if necessary
    while (index % 4 != 0) {
        base64_str[index++] = '=';  // Ensure the Base64 string has a length that is a multiple of 4
    }
    base64_str[index] = '\0';  // Null-terminate the Base64 string

    printf("Base64: %s\n", base64_str);  // Print the final Base64 string

    free(bin_str);  // Free the allocated memory for the binary string
    free(base64_str);  // Free the allocated memory for the Base64 string
}

// Main function
int main() {
    size_t buffer_size = 1024;  // Set the size of the buffer for user input
    char *hex_str = malloc(buffer_size);  // Allocate memory for the input hexadecimal string
    if (hex_str == NULL) {  // If memory allocation fails, print an error and exit
        printf("Memory allocation error.\n");
        return 1;
    }

    printf("Enter a hexadecimal string: ");
    if (fgets(hex_str, buffer_size, stdin) == NULL) {  // Read the input string
        printf("Error reading input.\n");
        free(hex_str);  // Free the allocated memory for the string
        return 1;
    }

    size_t hex_len = strlen(hex_str);  // Get the length of the input string
    if (hex_str[hex_len - 1] == '\n') {  // Remove the newline character if present
        hex_str[hex_len - 1] = '\0';
        hex_len--;
    }

    // Validate that all characters in the input string are valid hexadecimal digits
    for (size_t i = 0; i < hex_len; i++) {
        if (!isxdigit(hex_str[i])) {  // Check if the character is a valid hexadecimal digit
            printf("Error: Invalid hexadecimal character.\n");
            free(hex_str);  // Free the allocated memory for the string
            return 1;
        }
    }

    hex_to_base64(hex_str);  // Call the function to convert the hexadecimal string to Base64

    free(hex_str);  // Free the allocated memory for the input string

    return 0;  // Exit the program
}

