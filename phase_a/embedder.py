# Add imports
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create embedding function
def generate_embeddings(chunks):

    embedded_chunks = []

    for chunk in chunks:

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["content"]
        )

        embedding = response.data[0].embedding

        embedded_chunk = {
            "patient_id": chunk["patient_id"],
            "chunk_type": chunk["chunk_type"],
            "content": chunk["content"],
            "embedding": embedding
        }

        embedded_chunks.append(embedded_chunk)

    print(f"✅ Generated embeddings for {len(embedded_chunks)} chunks")

    return embedded_chunks