import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")

print(encoder.encode("I am Nick."))