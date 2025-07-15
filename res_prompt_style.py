
wordlimit = (0,5000,100)

styles = ["Short", "Long", "Explain"]

instruction_format = {
                    "Short": f"Give a short, direct answer in under {wordlimit} words.",
                    "Long": f"Provide a thorough, detailed explanation within {wordlimit} words.",
                    "Explain": f"Explain it clearly like teaching a beginner. Use under {wordlimit} words."       
              }


def build_prompt_with_memory(context, 
                             query, 
                             instruction,
                             history, 
                             memory_limit=5):
    
    """
    Construct a chat prompt including limited previous conversation memory.

    Parameters:
    - context (str): Extracted context from the PDF using vector search.
    - query (str): The latest user question.
    - instruction (str): How the assistant should respond (short, long, explain).
    - history (list): List of (question, answer) tuples from previous chat turns.
    - memory_limit (int): Number of previous Q&A pairs to include as memory.

    Returns:
    - List[Dict]: A prompt compatible with LLM chat-completion APIs.
    """
    messages = []

    # Include limited memory from past exchanges
    for prev_q, prev_a in history[-memory_limit:]:
        messages.append({"role": "user", "content": prev_q})
        messages.append({"role": "assistant", "content": prev_a})

    # Add instruction and current question
    messages.append({"role": "system", "content": f"Use the context to answer. {instruction}"})
    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"})

    return messages
