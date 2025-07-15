
from inference_client import get_response 
from dotenv import load_dotenv
from utils import load_and_split_pdf, build_astra_vectorstore, retrieve_context


load_dotenv()

pdf_path = "Stefin Seminar Report.pdf"


chunks = load_and_split_pdf(pdf_path)
vs = build_astra_vectorstore(chunks.pdf_path)

try:
    while True:
        query = input("💬 Ask a question about the PDF (press Ctrl+C to exit): ")

        if not query.strip():
            print("⚠️ Please enter a valid question.")
            continue

        print("🔍 Retrieving context...")
        context, _ = retrieve_context(query, vs, k=3)

        prompt = [
            {"role": "system", "content": "Answer the user's question based on the context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]

        print("🤖 Generating response...")
        answer = get_response(prompt)

        print("\n🧠 Answer:")
        print(answer)
        print("-" * 80)

except KeyboardInterrupt:
    print("\n👋 Exiting. See you next time!")

