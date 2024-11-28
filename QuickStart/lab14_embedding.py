from numpy import dot
from numpy.linalg import norm

a = [1,2,3]
b = [4,5,6]

cosine_similarity_result = dot(a,b) / (norm(a) * norm(b))
print("Cosine_similarity result:", cosine_similarity_result)