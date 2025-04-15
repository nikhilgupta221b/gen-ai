import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocab size ", encoder.n_vocab)

text = "The cat sat on the mat"

tokens = encoder.encode(text)

print("Tokens: ", tokens)

mytokens = [976, 9059, 10139, 402, 290, 2450]

decoded_text = encoder.decode(mytokens)

print("Decoded Message: ", decoded_text)