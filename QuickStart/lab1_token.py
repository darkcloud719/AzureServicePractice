import tiktoken

encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")

print(encoder.encode("apple"))