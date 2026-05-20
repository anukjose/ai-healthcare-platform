from fastapi import FastAPI

from router import detect_query_type

from sql_engine import (
    get_latest_test,
    get_test_history
)

from vector_engine import semantic_search

from hybrid_engine import run_hybrid_query

from formatter import format_response
from fastapi.middleware.cors import CORSMiddleware


# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/")

def home():

    return {
        "status": "Healthcare AI API running"
    }


# -----------------------------------
# MAIN QUERY ENDPOINT
# -----------------------------------

@app.post("/ask")

def ask_question(payload: dict):

    patient_id = payload["patient_id"]

    question = payload["question"]

    query_type = detect_query_type(question)

    # -----------------------------------
    # SQL QUERY
    # -----------------------------------

    if query_type == "sql":

        result = get_latest_test(
            patient_id,
            "CRP"
        )

        return format_response(

            query_type="sql",

            question=question,

            answer=result,

            sources=["patient_lab_summary"],

            metadata={
                "patient_id": patient_id
            }
        )

    # -----------------------------------
    # VECTOR QUERY
    # -----------------------------------

    elif query_type == "vector":

        results = semantic_search(
            patient_id,
            question
        )

        return format_response(

            query_type="vector",

            question=question,

            answer=results,

            sources=["patient_chunks"],

            metadata={
                "patient_id": patient_id
            }
        )

    # -----------------------------------
    # HYBRID QUERY
    # -----------------------------------

    elif query_type == "hybrid":

        result = run_hybrid_query(
            patient_id=patient_id,
            question=question,
            test_name="CRP"
        )

        return format_response(

            query_type="hybrid",

            question=question,

            answer=result["answer"],

            sources=[
                "patient_lab_summary",
                "patient_chunks"
            ],

            metadata={
                "patient_id": patient_id
            }
        )