from loader import load_patient_json
from transformer import transform_labs
from feature import generate_features
from embedder import generate_embeddings

from store import (
    store_facts,
    store_summaries,
    store_chunks
)
#data = load_patient_json("../data/patient.json") for laptop local run
data = load_patient_json("/data/patient.json") # for docker run volume 


print(data.keys())
labs = transform_labs(data)

print(labs[:3])

# -------------------------
# FEATURE ENGINEERING
# -------------------------
facts, summaries, chunks = generate_features(labs)

print("\n--- SUMMARIES ---")
print(summaries[:3])

print("\n--- CHUNKS ---")
print(chunks[:3])




# -------------------------
# STORE
# -------------------------
store_facts(facts)

store_summaries(summaries)

# -------------------------
# GENERATE EMBEDDINGS
# -------------------------
embedded_chunks = generate_embeddings(chunks)
# Print sample embedding
print(embedded_chunks[0]["embedding"][:5])
# -------------------------
# STORE EMBEDDED CHUNKS
# -------------------------
store_chunks(embedded_chunks)

print("\n✅ Phase A preprocessing completed")

