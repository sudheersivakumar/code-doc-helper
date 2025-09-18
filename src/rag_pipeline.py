# src/rag_pipeline.py
from google.generativeai import GenerativeModel

# Simple CRAG Correction Loop
def crag_generate_answer(question: str, context: str, model: GenerativeModel, max_retries=2):
    """
    Implements a basic CRAG loop:
    1. Generate answer.
    2. Validate confidence.
    3. If low confidence → retry with expanded context or re-query (future).
    """
    prompt_template = """
You are a helpful code assistant. Answer the question based ONLY on the context below.
If the context is insufficient or irrelevant, say "I cannot answer confidently based on available context."

Context:
{context}

Question: {question}

Answer:
"""

    retry_count = 0
    while retry_count <= max_retries:
        prompt = prompt_template.format(context=context, question=question)
        response = model.generate_content(prompt)
        answer = response.text.strip()

        # Simple confidence check: if answer says it can't answer, retry or break
        low_confidence_phrases = [
            "cannot answer confidently",
            "don't know",
            "not sure",
            "insufficient context",
            "irrelevant"
        ]

        if any(phrase in answer.lower() for phrase in low_confidence_phrases):
            if retry_count < max_retries:
                print(f"🔁 Low confidence detected. Retry {retry_count + 1}/{max_retries}...")
                # You can enhance this: expand context, re-query with refined keywords, etc.
                # For now, just retry with same context (could add more chunks in future)
                retry_count += 1
                continue
            else:
                answer = "⚠️ After multiple attempts, I still cannot answer confidently. Try rephrasing or check if relevant code is ingested."
                break
        else:
            # Answer seems confident
            break

    return answer