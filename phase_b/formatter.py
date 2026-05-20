# -----------------------------------
# FORMAT RESPONSE
# -----------------------------------

def format_response(

    query_type,
    question,
    answer,
    sources=None,
    metadata=None
):

    response = {

        "query_type": query_type,

        "question": question,

        "answer": answer,

        "sources": sources or [],

        "metadata": metadata or {}
    }

    return response


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    response = format_response(

        query_type="hybrid",

        question="What is latest CRP?",

        answer=(
            "Latest CRP value is 3.64 mg/L. "
            "Historical values fluctuated over time."
        ),

        sources=[
            "patient_lab_summary",
            "patient_chunks"
        ],

        metadata={
            "patient_id": "P001"
        }
    )

    print("\n--- FORMATTED RESPONSE ---\n")

    print(response)