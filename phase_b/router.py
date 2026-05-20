# -----------------------------------
# QUERY ROUTER
# -----------------------------------

def detect_query_type(question):

    question = question.lower()

    # -----------------------------------
    # SQL / FACTUAL QUERIES
    # -----------------------------------

    factual_keywords = [

        "latest",
        "value",
        "exact",
        "count",
        "when",
        "date",
        "maximum",
        "minimum",
        "highest",
        "lowest"
    ]

    # -----------------------------------
    # VECTOR / SEMANTIC RETRIEVAL
    # -----------------------------------

    vector_keywords = [

        "find",
        "search",
        "retrieve",
        "related",
        "similar"
    ]

    # -----------------------------------
    # HYBRID / SYNTHESIS QUERIES
    # -----------------------------------

    hybrid_keywords = [

        "summary",
        "summarize",
        "explain",
        "overall",
        "trend",
        "history",
        "pattern",
        "behaviour",
        "behavior",
        "overview",
        "handoff",
        "progression",
        "over time",
        "fluctuating",
        "compare"
    ]

    # -----------------------------------
    # MATCH DETECTION
    # -----------------------------------

    factual_match = any(
        word in question
        for word in factual_keywords
    )

    vector_match = any(
        word in question
        for word in vector_keywords
    )

    hybrid_match = any(
        word in question
        for word in hybrid_keywords
    )

    # -----------------------------------
    # ROUTING LOGIC
    # -----------------------------------

    # SQL + LLM synthesis
    if factual_match and hybrid_match:
        return "hybrid"

    # Pure factual retrieval
    elif factual_match:
        return "sql"

    # Explicit semantic retrieval
    elif vector_match:
        return "vector"

    # Summary / narrative / overview
    elif hybrid_match:
        return "hybrid"

    # Unknown queries fallback
    else:
        return "hybrid"


# -----------------------------------
# TEST ROUTER
# -----------------------------------

if __name__ == "__main__":

    questions = [

        "What is latest CRP?",

        "Find inflammation related records",

        "Summarize inflammatory markers over time",

        "Provide rheumatology overview",

        "What is latest ESR and summarize trend?",

        "How is patient doing overall?"
    ]

    for q in questions:

        query_type = detect_query_type(q)

        print(f"\nQuestion: {q}")
        print(f"Route: {query_type}")