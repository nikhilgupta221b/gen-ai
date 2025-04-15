# Encode and Decoder example code

# Lowercase dictionary
lower_dict = {chr(i) : 10 + (i - ord('a')) for i in range (ord('a'), ord('z') + 1)}

# Uppercase dictionary
upper_dict = {chr(i) : 50 + (i - ord('A')) for i in range (ord('A'), ord('Z') + 1)}

# Final Encoder dictionary
enc_dict = {**lower_dict, **upper_dict}
enc_dict[' '] = 98
enc_dict['.'] = 99

# Final Decoder dictionary
dec_dict = {}
for key, value in enc_dict.items():
    dec_dict[value] = key

# Encoder Class with encode() and decode()
class Encoder:
    def encode(self, input_message):
        encoded_tokens = []
        for c in input_message:
            encoded_tokens.append(enc_dict[c])
        return encoded_tokens
    
    def decode(self, input_tokens):
        decoded_message = ""
        for n in input_tokens:
            decoded_message = decoded_message + dec_dict[n]
        return decoded_message
    
# Usage
encoder = Encoder()

text = "This is a big elephant." 
tokens = encoder.encode(text)
print("Tokens: ", tokens)

input_tokens = [69, 17, 18, 28, 98, 18, 28, 98, 10, 98, 11, 18, 16, 98, 14, 21, 14, 25, 17, 10, 23, 29, 99]
message = encoder.decode(input_tokens)
print("Message: ", message)
