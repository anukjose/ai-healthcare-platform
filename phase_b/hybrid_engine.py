from sql_engine import get_latest_test
from vector_engine import semantic_search

from llm import generate_answer


# -----------------------------------
# HYBRID QUERY ENGINE
# -----------------------------------

def run_hybrid_query(patient_id, question, test_name):

    # -----------------------------------
    # SQL FACTS
    # -----------------------------------

    latest = get_latest_test(
        patient_id,
        test_name
    )

    # -----------------------------------
    # VECTOR CONTEXT
    # -----------------------------------

    chunks = semantic_search(
        patient_id,
        question
    )

    # -----------------------------------
    # BUILD CONTEXT
    # -----------------------------------

    context = ""

    # SQL factual context
    if latest:

        context += (
            f"Latest {latest['test']} value: "
            f"{latest['latest_value']}.\n"
        )

        context += (
            f"Trend: {latest['trend']}.\n\n"
        )

    # Semantic chunk context
    context += "Relevant history:\n\n"

    for c in chunks:

        context += c["content"]
        context += "\n\n"

    # -----------------------------------
    # LLM RESPONSE
    # -----------------------------------

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "context": context,
        "answer": answer
    }


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    question = (
        "What is latest CRP and summarize inflammation history?"
    )

    result = run_hybrid_query(
        patient_id="P001",
        question=question,
        test_name="CRP"
    )

    print("\n--- ANSWER ---\n")

    print(result["answer"])