from dotenv import load_dotenv
import os
# Import the necessary classes
# from agents import Agent, Runner, function_tool   # OpenAI Agents SDK components
import chromadb                                   # ChromaDB client
# from chromadb.utils import embedding_functions    # (optional, if using embedding functions directly)
from google import genai                          # Google GenAI SDK for Gemini
from google.genai.types import EmbedContentConfig

load_dotenv()

GEMINI_API_KEY = os.getenv("api_key")

# Initialize ChromaDB in-memory client
chroma_client = chromadb.Client()  # default uses an in-memory SQLite store

# Initialize Google GenAI client with the Gemini API key
client = genai.Client(api_key=GEMINI_API_KEY)

# Define a few short text documents (e.g., Wikipedia-style snippets)
documents = [
    "Cats are small, domesticated carnivorous mammals often valued by humans for companionship and for their ability to hunt vermin.",
    "Dogs are domesticated mammals, not natural wild animals. They were originally bred from wolves.",
    "The Apollo program was a series of space missions by NASA in the 1960s and 1970s aimed at landing humans on the Moon."
]
doc_ids = ["doc1", "doc2", "doc3"]

# (Optional) Print the documents to verify
for i, doc in enumerate(documents, 1):
    print(f"Document {i}: {doc[:60]}...")


# Embed each document using the Gemini embedding model
embed_model = "gemini-embedding-exp-03-07"

# Generate embeddings for all documents in one call
response = client.models.embed_content(
    model=embed_model,
    contents=documents,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")  # optimize embeddings for retrieval
)

# Extract the embedding vectors from the response
doc_embeddings = [emb.values for emb in response.embeddings]

# Check the number of embeddings and dimensionality of one embedding
print(f"Generated {len(doc_embeddings)} embeddings.")
print(f"Dimension of first embedding: {len(doc_embeddings[0])}")

print(f"Sample of first embedding vector: {doc_embeddings[0][:5]}...")  # print first 5 values

# Create a ChromaDB collection for our documents
collection = chroma_client.create_collection(name="knowledge_base")

# Add documents, their embeddings, and IDs to the collection
collection.add(
    documents=documents,
    embeddings=doc_embeddings,
    ids=doc_ids
)

# (Optional) verify collection size
print("Documents in collection:", collection.count())



# User's question
user_question = "Which animal were dogs originally bred from?"

# Embed the user query using the same model (use task_type RETRIEVAL_QUERY for queries)
query_response = client.models.embed_content(
    model=embed_model,
    contents=[user_question],
    config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
)
query_vector = query_response.embeddings[0].values
# query_vector

# Use ChromaDB to find the most similar document(s) to the query
results = collection.query(
    query_embeddings=[query_vector],
    n_results=2,  # fetch top 2 most similar docs
    # Remove 'ids' from the include list as it's not a valid option
    include=["documents", "distances"]
)
results

# Print out the retrieved documents and their similarity scores
# print("Query:", user_question)
# for doc, score, doc_id in zip(results["documents"][0], results["distances"][0], results["ids"][0]):
#     print(f"- Retrieved {doc_id} with similarity score {score:.4f}: {doc[:60]}...")

print(f"Sample of first embedding vector: {doc_embeddings[0][:5]}...")  # print first 5 values


# Prepare the context from the retrieved docs
retrieved_docs = results["documents"][0]
context = "\n\n".join(retrieved_docs)

# Formulate the prompt for the LLM
prompt = f"""Use the following context to answer the question.

Context:
{context}

Question:
{user_question}

Answer the question using only the information from the context above."""
print(prompt)


# Use the Gemini 1.5 Flash model to get an answer based on the context
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)
answer = response.text

print("Answer:", answer)




