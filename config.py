import os
from dotenv import load_dotenv

load_dotenv()

# Pinecone Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "midc-land-bank-improved")

# Google Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
GENERATION_MODEL = "gemini-2.5-flash"

# Vector Configuration
VECTOR_DIMENSION = 768
TOP_K_RESULTS = 10
SIMILARITY_THRESHOLD = 0.3
