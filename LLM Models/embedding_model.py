from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
load_dotenv
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Your text data
sentences = [
    "I love coding",
    "Programming is my passion",
    "I enjoy playing cricket"
]
embeddings = model.encode(sentences)

# Print result
print("Embeddings shape:", embeddings.shape)
print("First embedding:", embeddings[0])