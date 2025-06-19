# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# import chromadb
# from google import genai
# from google.genai.types import EmbedContentConfig

# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled, function_tool

# # ========== Setup ==========
# load_dotenv()
# set_tracing_disabled(True)

# # Colors and Theme
# st.set_page_config(page_title="Gemini PDF QA Dashboard", layout="wide")
# st.markdown("""
#     <style>
#         .main {
#             background-color: #f4f6fa;
#         }
#         .sidebar .sidebar-content {
#             background-color: #001f3f;
#             color: white;
#         }
#         .stButton>button {
#             background-color: #0074D9;
#             color: white;
#             font-weight: bold;
#         }
#         .stTextInput>div>div>input {
#             background-color: #e6f0ff;
#         }
#         .block-container {
#             padding: 2rem;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # API key setup
# gemini_api_key = os.getenv("api_key")
# if not gemini_api_key:
#     st.sidebar.error("❌ API key not found. Please add it to your .env file.")
#     st.stop()

# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )
# set_default_openai_client(external_client)

# client = genai.Client(api_key=gemini_api_key)
# chroma_client = chromadb.Client()
# embed_model = "gemini-embedding-exp-03-07"

# # ========== Session State Setup ==========
# if "collection" not in st.session_state:
#     st.session_state.collection = None
# collection = st.session_state.collection

# # ========== Functions ==========
# def load_and_split_pdf(file_path: str):
#     loader = PyPDFLoader(file_path)
#     pages = loader.load_and_split()
#     return pages

# @function_tool
# def answer_from_knowledge_base(query: str) -> str:
#     q_resp = client.models.embed_content(
#         model=embed_model,
#         contents=[query],
#         config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
#     )
#     q_vector = q_resp.embeddings[0].values

#     res = st.session_state.collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
#     if res and res.get("documents") and res["documents"][0]:
#         top_doc = res["documents"][0][0]
#         prompt = f"Context:\n{top_doc}\n\nQuestion:\n{query}\n\nAnswer the question using only the context above. If the context does not contain relevant information, reply: 'Sorry, I couldn't find relevant information in the uploaded PDF.'"
#         resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
#         return resp.text
#     else:
#         return "Sorry, I couldn't find relevant information in the uploaded PDF."

# qa_agent = Agent(
#     name="PDF QA Agent",
#     instructions="You are a helpful assistant. Use the knowledge base to answer questions. If the information is not in the PDF, clearly say it is unavailable.",
#     tools=[answer_from_knowledge_base],
#     model=OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )
# )

# # ========== Sidebar for File Upload ==========
# st.sidebar.header("📂 Upload Your PDF")
# uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

# if uploaded_file:
#     with st.spinner("Reading and embedding PDF..."):
#         with open("temp.pdf", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         try:
#             pages = load_and_split_pdf("temp.pdf")
#             documents = [page.page_content for page in pages]
#             doc_ids = [f"pdf_page_{i+1}" for i in range(len(pages))]

#             embeddings_resp = client.models.embed_content(
#                 model=embed_model,
#                 contents=documents,
#                 config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
#             )
#             doc_embeddings = [emb.values for emb in embeddings_resp.embeddings]

#             st.session_state.collection = chroma_client.get_or_create_collection(name="kb_streamlit")
#             st.session_state.collection.add(documents=documents, embeddings=doc_embeddings, ids=doc_ids)

#             st.sidebar.success(f"✅ {len(pages)} pages added to knowledge base")
#         except Exception as e:
#             st.sidebar.error(f"❌ Error processing PDF: {e}")

# # ========== Main Panel for Question Input ==========
# st.title("💬 Ask Questions from Your PDF")

# if st.session_state.collection:
#     st.markdown("### 🤔 Ask a Question")
#     with st.form(key="question_form"):
#         user_query = st.text_input("Type your question here:", placeholder="e.g. What is the purpose of this document?")
#         submit_button = st.form_submit_button("Ask")

#     if submit_button and user_query:
#         with st.spinner("🔍 Searching answer..."):
#             try:
#                 result = asyncio.run(Runner.run(qa_agent, user_query))
#                 if "Sorry, I couldn't find relevant information" in result.final_output:
#                     st.warning(result.final_output)
#                 else:
#                     st.success("✅ Answer:")
#                     st.write(result.final_output)
#             except Exception as e:
#                 st.error(f"❌ Failed to get answer: {e}")
# else:
#     st.info("👈 Upload and process a PDF file to start asking questions.")





# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv

# from langchain_community.document_loaders import PyPDFLoader
# import chromadb
# from google import genai
# from google.genai.types import EmbedContentConfig

# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled, function_tool

# # ========== Setup ==========

# load_dotenv()
# set_tracing_disabled(True)

# gemini_api_key = os.getenv("api_key")
# if not gemini_api_key:
#     st.error("API key not found. Please add it to your .env file.")
#     st.stop()

# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )
# set_default_openai_client(external_client)

# client = genai.Client(api_key=gemini_api_key)
# chroma_client = chromadb.Client()

# embed_model = "gemini-embedding-exp-03-07"

# # ========== Functions ==========

# def load_and_split_pdf(file_path: str):
#     loader = PyPDFLoader(file_path)
#     pages = loader.load_and_split()
#     return pages

# @function_tool
# def answer_from_knowledge_base(query: str) -> str:
#     q_resp = client.models.embed_content(
#         model=embed_model,
#         contents=[query],
#         config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
#     )
#     q_vector = q_resp.embeddings[0].values

#     res = collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
#     if res and res.get("documents") and res["documents"][0]:
#         top_doc = res["documents"][0][0]
#         prompt = f"Context:\n{top_doc}\n\nQuestion:\n{query}\n\nAnswer the question using only the context above."
#         resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
#         return resp.text
#     else:
#         return "No relevant info found in the knowledge base."

# qa_agent = Agent(
#     name="PDF QA Agent",
#     instructions="You are a helpful assistant. Use the knowledge base to answer questions.",
#     tools=[answer_from_knowledge_base],
#     model=OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )
# )

# # ========== Streamlit App ==========

# st.set_page_config(page_title="Gemini RAG QA", layout="wide")
# st.title("📄 Gemini PDF QA with RAG")

# uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# if uploaded_file:
#     with st.spinner("Reading and embedding PDF..."):
#         with open("temp.pdf", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         pages = load_and_split_pdf("temp.pdf")
#         documents = [page.page_content for page in pages]
#         doc_ids = [f"pdf_page_{i+1}" for i in range(len(pages))]

#         embeddings_resp = client.models.embed_content(
#             model=embed_model,
#             contents=documents,
#             config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
#         )
#         doc_embeddings = [emb.values for emb in embeddings_resp.embeddings]

#         collection = chroma_client.get_or_create_collection(name="kb_streamlit")
#         try:
#             collection.add(
#                 documents=documents,
#                 embeddings=doc_embeddings,
#                 ids=doc_ids
#             )
#             st.success(f"Added {len(pages)} pages to the knowledge base.")
#         except Exception as e:
#             st.warning(f"Could not add documents (maybe duplicates): {e}")

#     query = st.text_input("Ask a question based on the uploaded PDF:")

#     if query:
#         with st.spinner("Getting answer..."):
#             result = asyncio.run(Runner.run(qa_agent, query))
#             st.subheader("Answer:")
#             st.write(result.final_output)



















# import os
# import asyncio
# from dotenv import load_dotenv

# from langchain_community.document_loaders import PyPDFLoader
# import chromadb
# from google import genai
# from google.genai.types import EmbedContentConfig

# # Custom modules
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled, function_tool

# # ========== Setup ==========

# load_dotenv()
# set_tracing_disabled(True)

# gemini_api_key = os.getenv("api_key")
# if not gemini_api_key:
#     raise ValueError("API key not found. Please add it to your .env file.")

# # Gemini + ChromaDB Clients
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )
# set_default_openai_client(external_client)

# client = genai.Client(api_key=gemini_api_key)
# chroma_client = chromadb.Client()

# # Embedding model
# embed_model = "gemini-embedding-exp-03-07"

# # ========== Step 1: Load and split multiple PDFs ==========

# def load_and_split_multiple_pdfs(pdf_paths: list):
#     """Load and split multiple PDF files into pages."""
#     all_pages = []
#     all_ids = []

#     for path in pdf_paths:
#         loader = PyPDFLoader(path)
#         pages = loader.load_and_split()
#         all_pages.extend(pages)
#         all_ids.extend([f"{os.path.basename(path)}_page_{i+1}" for i in range(len(pages))])
#         print(f"✅ Loaded {len(pages)} pages from {path}")

#     return all_pages, all_ids

# # Example usage:
# pdf_files = ["profile.pdf"]  # Add your PDF file paths here
# pdf_pages, pdf_doc_ids = load_and_split_multiple_pdfs(pdf_files)

# # Extract text from all pages
# pdf_documents_text = [page.page_content for page in pdf_pages]

# # ========== Step 2: Embed documents using Gemini ==========

# pdf_embeddings_response = client.models.embed_content(
#     model=embed_model,
#     contents=pdf_documents_text,
#     config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
# )
# pdf_doc_embeddings = [emb.values for emb in pdf_embeddings_response.embeddings]

# # ========== Step 3: Store to ChromaDB ==========

# collection = chroma_client.get_or_create_collection(name="knowledge_base1")

# try:
#     collection.add(
#         documents=pdf_documents_text,
#         embeddings=pdf_doc_embeddings,
#         ids=pdf_doc_ids
#     )
#     print(f"✅ Added {len(pdf_pages)} PDF pages to the knowledge base.")
# except Exception as e:
#     print(f"⚠️ Could not add PDF documents (maybe duplicates): {e}")

# print("📄 Total documents in collection:", collection.count())

# # ========== Step 4: RAG Tool Function ==========

# @function_tool
# def answer_from_knowledge_base(query: str) -> str:
#     """Search the knowledge base and generate answer using Gemini."""
#     print(f"[Debug] Question received: {query}")
#     q_resp = client.models.embed_content(
#         model=embed_model,
#         contents=[query],
#         config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
#     )
#     q_vector = q_resp.embeddings[0].values

#     res = collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
#     if res and res.get("documents") and res["documents"][0]:
#         top_doc = res["documents"][0][0]

#         # Structured input to Gemini for accurate results
#         resp = client.models.generate_content(
#             model="gemini-1.5-flash",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [
#                         {
#                             "text": f"Using the context below, answer the question strictly based on it:\n\nContext:\n{top_doc}\n\nQuestion:\n{query}"
#                         }
#                     ]
#                 }
#             ]
#         )
#         print(f"[Debug] Gemini response: {resp.text}")
#         return resp.text
#     else:
#         return "No relevant info found in the knowledge base."

# # ========== Step 5: Create Agent ==========

# qa_agent = Agent(
#     name="PDF QA Agent",
#     instructions="You are a helpful assistant. Use the knowledge base to answer questions. User will give you PDFs and you will answer from them using the tool.",
#     tools=[answer_from_knowledge_base],
#     model=OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )
# )

# # ========== Step 6: Ask Question ==========

# async def main_pdf_question():
#     pdf_question = "i give you pdf in that pdf is also email of tehreem so now tell me what is the email of tehreem?"
#     result = await Runner.run(qa_agent, pdf_question)
#     print("🤖 Agent result:", result)
#     print("📢 Final answer:", result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main_pdf_question())
































import os
import asyncio
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
import chromadb
from google import genai
from google.genai.types import EmbedContentConfig

# Custom modules
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled, function_tool

# ========== Setup ==========

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("api_key")
if not gemini_api_key:
    raise ValueError("API key not found. Please add it to your .env file.")

# Gemini + ChromaDB Clients
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

client = genai.Client(api_key=gemini_api_key)
chroma_client = chromadb.Client()

# Embedding model
embed_model = "gemini-embedding-exp-03-07"

# ========== Step 1: Load PDF file ==========

def load_and_split_pdf(file_path: str):
    """Loads a PDF and splits it into pages using Langchain PyPDFLoader."""
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages

# Replace this with the actual path to your PDF file
pdf_file_path = "day1.pdf"  # Example: "docs/info.pdf"
pdf_pages = load_and_split_pdf(pdf_file_path)

print(f"✅ Loaded {len(pdf_pages)} pages from {pdf_file_path}")

# Extract text and prepare IDs
pdf_documents_text = [page.page_content for page in pdf_pages]
pdf_doc_ids = [f"pdf_page_{i+1}" for i in range(len(pdf_pages))]


# def load_and_split_multiple_pdfs(pdf_paths: list):
#     """Load and split multiple PDF files into pages."""
#     all_pages = []
#     all_ids = []

#     for path in pdf_paths:
#         loader = PyPDFLoader(path)
#         pages = loader.load_and_split()
#         all_pages.extend(pages)
#         all_ids.extend([f"{os.path.basename(path)}_page_{i+1}" for i in range(len(pages))])

#         print(f"✅ Loaded {len(pages)} pages from {path}")

#     return all_pages, all_ids

# Example usage:
pdf_files = "profile.pdf" # Add your PDF file paths here
pdf_pages = load_and_split_pdf(pdf_files)

# Extract text from all pages
pdf_documents_text = [page.page_content for page in pdf_pages]

# ========== Step 2: Embed documents using Gemini ==========
pdf_embeddings_response = client.models.embed_content(
    model=embed_model,
    contents=pdf_documents_text,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
)
pdf_doc_embeddings = [emb.values for emb in pdf_embeddings_response.embeddings]


# ========== Step 3: Store to ChromaDB ==========

collection = chroma_client.get_or_create_collection(name="knowledge_base1")

try:
    collection.add(
        documents=pdf_documents_text,
        embeddings=pdf_doc_embeddings,
        ids=pdf_doc_ids
    )
    print(f"✅ Added {len(pdf_pages)} PDF pages to the knowledge base.")
except Exception as e:
    print(f"⚠️ Could not add PDF documents (maybe duplicates): {e}")

print("📄 Total documents in collection:", collection.count())

# ========== Step 4: RAG Tool Function ==========

@function_tool
def answer_from_knowledge_base(query: str) -> str:
    """Search the knowledge base and generate answer using Gemini."""
    print(f"[Debug] Question received: {query}")
    q_resp = client.models.embed_content(
        model=embed_model,
        contents=[query],
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    q_vector = q_resp.embeddings[0].values

    res = collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
    if res and res.get("documents") and res["documents"][0]:
        top_doc = res["documents"][0][0]
        prompt = f"Context:\n{top_doc}\n\nQuestion:\n{query}\n\nAnswer the question using only the context above."
        resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)


        print(f"[Debug] Gemini response: {resp.text}")
        return resp.text
    else:
        return "No relevant info found in the knowledge base."

# ========== Step 5: Create Agent ==========

qa_agent = Agent(
    name="PDF QA Agent",
    instructions="You are a helpful assistant. Use the knowledge base to answer questions. user will give you pdf and you will answer from that pdf answer ka liya tm tool call karna hoga",
    tools=[answer_from_knowledge_base],
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
)

# ========== Step 6: Ask Question (Main Run Function) ==========

async def main_pdf_question():
    pdf_question = "who is tehreem"  # Ask based on your PDF content
    result = await Runner.run(qa_agent, pdf_question)
    print("🤖 Agent result:", result)
    print("📢 Final answer:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main_pdf_question())

 