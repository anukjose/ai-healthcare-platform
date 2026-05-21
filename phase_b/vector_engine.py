import os
import psycopg2

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)


# ---------------------------------------------------
# KUBERNETES DATABASE CONNECTION
# ---------------------------------------------------
# Kubernetes services communicate internally
# using Service names.
#
# postgres-service
# is the Kubernetes Service hostname.
# ---------------------------------------------------

DB_CONFIG = {
    "dbname": "healthcare_demo",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres-service",
    "port": "5432"
}


# ---------------------------------------------------
# GET DATABASE CONNECTION
# ---------------------------------------------------

def get_connection():

    conn = psycopg2.connect(**DB_CONFIG)

    return conn


# ---------------------------------------------------
# PREVIOUS DOCKER COMPOSE CONFIG
# ---------------------------------------------------
'''
Docker Compose networking used:

host="postgres-db"

because services communicated through
Docker Compose internal network.

Example:

conn = psycopg2.connect(
    dbname="healthcare_demo",
    user="postgres",
    password="postgres",
    host="postgres-db",
    port="5432"
)
'''


# ---------------------------------------------------
# PREVIOUS LOCAL LAPTOP CONFIG
# ---------------------------------------------------
'''
Local Mac PostgreSQL connection:

conn = psycopg2.connect(
    dbname="healthcare_demo",
    user="anusmacbook",
    host="localhost",
    port="5432"
)
'''


# ---------------------------------------------------
# GENERATE QUESTION EMBEDDING
# ---------------------------------------------------

def generate_question_embedding(question):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    embedding = response.data[0].embedding

    return embedding


# ---------------------------------------------------
# VECTOR SEARCH
# ---------------------------------------------------

def semantic_search(patient_id, question, limit=3):

    question_embedding = generate_question_embedding(question)

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            content,

            embedding <=> %s::vector AS distance

        FROM patient_chunks

        WHERE patient_id = %s

        ORDER BY embedding <=> %s::vector

        LIMIT %s

    """, (
        question_embedding,
        patient_id,
        question_embedding,
        limit
    ))

    rows = cur.fetchall()

    cur.close()

    conn.close()

    results = []

    for row in rows:

        results.append({
            "content": row[0],
            "distance": row[1]
        })

    return results


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    question = "How have inflammation markers behaved?"

    results = semantic_search(
        "P001",
        question
    )

    print("\n--- VECTOR SEARCH RESULTS ---\n")

    for r in results:

        print("Distance:", r["distance"])

        print(r["content"])

        print("\n-------------------\n")