import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , set_default_openai_client, set_tracing_disabled , function_tool
from agents.run import RunConfig
from dotenv import load_dotenv
from agents.tool import function_tool
import chromadb
from google import genai
from google.genai.types import EmbedContentConfig
import asyncio


load_dotenv()

set_tracing_disabled(True)

gemini_api_key = os.getenv("api_key")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")



# Configure the OpenAI-compatible client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set this as the default OpenAI client for agents
set_default_openai_client(external_client)

# Initialize Google GenAI client for RAG embedding/generation
client = genai.Client(api_key=gemini_api_key)

# Initialize ChromaDB in-memory client
chroma_client = chromadb.Client()

# Define and embed documents
documents = [
    "Cats are small, domesticated carnivorous mammals often valued by humans for companionship and for their ability to hunt vermin.",
    "Dogs are domesticated mammals, not natural wild animals. They were originally bred from wolves.",
    "The Apollo program was a series of space missions by NASA in the 1960s and 1970s aimed at landing humans on the Moon."
]
doc_ids = ["doc1", "doc2", "doc3"]
embed_model = "gemini-embedding-exp-03-07" # Or whichever model you used

# Generate embeddings for all documents in one call
response = client.models.embed_content(
    model=embed_model,
    contents=documents,
    config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
)
doc_embeddings = [emb.values for emb in response.embeddings]

# Create or get the collection
collection = chroma_client.get_or_create_collection(name="knowledge_base1")

# Add documents, handling potential duplicates
try:
    collection.add(
        documents=documents,
        embeddings=doc_embeddings,
        ids=doc_ids
          )
except Exception as e:
    print(f"Could not add documents to collection, potentially they already exist: {e}")


# Define the RAG tool using the accessible clients and variables
@function_tool
def answer_from_knowledge_base(query: str) -> str:
    """
    Tool: Given a user query, this tool searches the knowledge base and returns an answer using retrieved documents.
    """
    print(f"[Debug] RAG function call with query {query}")
    # Embed the query using the accessible 'client' and 'embed_model'
    q_resp = client.models.embed_content(
        model=embed_model,
        contents=[query],
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    q_vector = q_resp.embeddings[0].values
 
    # Search the vector store using the accessible 'collection'
    res = collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
    print(f"[Debug] RAG vector db output {res}")
    # Check if any documents were returned
    if res and res.get("documents") and res["documents"][0]:
        top_doc = res["documents"][0][0]  # top result's text
        # Construct prompt with retrieved context
        prompt = f"Context:\n{top_doc}\n\nQuestion:\n{query}\n\nAnswer the question using only the context above."
        # Generate answer with Gemini 1.5 Flash using the accessible 'client'
        resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        print(f"[Debug] RAG function call with response ***{resp.text}***")
        return resp.text
    else:
        return "Could not find relevant information in the knowledge base."

# Create an agent that can use the knowledge base tool
# Use OpenAIChatCompletionsModel with the external_client
qa_agent = Agent(
    name="QA Agent",
    instructions="You are a helpful assistant. If the user asks a question, use your tools to find information in the knowledge base and answer with that information.",
    tools=[answer_from_knowledge_base],
    # Use OpenAIChatCompletionsModel with the pre-configured external_client
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", # Specify the model name compatible with the OpenAI-like endpoint
        openai_client=external_client
    )
)

async def main():
    agent_question = "Which domestic animal was originally bred from wolves? what do you know about Apollo?"

    # Run the agent
    result = await Runner.run(qa_agent, agent_question)

    # Extract and print the final answer
    print("Agent result:", result)
    print("Agent's answer:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())