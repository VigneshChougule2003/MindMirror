# File: run_rag.py

from components.generate_summary import generate_user_summary
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub

def run_rag():
    # Step 1: Generate input
    summary = generate_user_summary()
    print("📝 Generated summary for analysis:\n", summary)

    # Step 2: Load vector DB
    try:
        vectorstore = FAISS.load_local("rag_store", HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))
    except Exception as e:
        print(f"❌ Failed to load vector store: {e}")
        return

    # Step 3: Retrieve relevant context
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(summary)

    # Step 4: RAG Chain
    llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature": 0.5, "max_length": 512})
    chain = load_qa_chain(llm=llm, chain_type="stuff")

    result = chain.run(
        input_documents=docs,
        question="Given this user content consumption summary, what can you infer about their psychology and mental health?"
    )
    
    print("\n🧠 RAG Output:\n", result)

if __name__ == '__main__':
    run_rag()
