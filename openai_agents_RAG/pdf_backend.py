from agents import (Agent , Runner , ModelSettings , AsyncOpenAI , OpenAIChatCompletionsModel , 
                    set_default_openai_client , set_tracing_disabled , function_tool)
from agents.run import RunConfig
from dotenv import load_dotenv
import chromadb
from google import genai
from google.genai.types import EmbedContentConfig
import os
from langchain_community.document_loaders import PyPDFLoader

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
set_default_openai_client(external_client)



client = genai.Client(api_key=gemini_api_key)
chroma_client = chromadb.Client()

embed_model = "gemini-embedding-exp-03-07"


model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    model_settings=ModelSettings(tool_choice="required")
)

def load_and_split_multiple_pdfs(pdf_paths: list):
    """Load and split multiple PDF files into pages."""
    all_pages = []
    all_ids = []

    for path in pdf_paths:
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        all_pages.extend(pages)
        all_ids.extend([f"{os.path.basename(path)}_page_{i+1}" for i in range(len(pages))])

        print(f"✅ Loaded {len(pages)} pages from {path}")
        

    return all_pages, all_ids

def load_and_embed_pdf(file_path: str):
    global collection  # so it’s accessible to the tool

    pdf_pages, pdf_doc_ids = load_and_split_multiple_pdfs([file_path])
    document_content = [page.page_content for page in pdf_pages]

    embeddings_resp = client.models.embed_content(
        model=embed_model,
        contents=document_content,
        config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    
   
    doc_embeddings = [emb.values for emb in embeddings_resp.embeddings]

    collection = chroma_client.get_or_create_collection(name="pdf_knowledge_base")
    collection.add(documents=document_content, embeddings=doc_embeddings, ids=pdf_doc_ids)
    print(f"✅ Added {len(pdf_pages)} PDF pages to the knowledge base.")



@function_tool
def answer_from_pdf(query: str) -> str:
    """Search the knowledge base and generate answer using Gemini."""
    q = client.models.embed_content(
        model=embed_model,
        contents=[query],
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )

    q_vector = q.embeddings[0].values

    res = collection.query(query_embeddings=[q_vector], n_results=1, include=["documents"])
 

    if res and res.get("documents") and res["documents"][0]:
        top_doc = res["documents"][0][0]

        prompt = f"""
           Use the following context to answer the question.
           Context:
           {top_doc}
            Question: {query}
            Answer:"""
        resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

        return resp.text


agent = Agent(
    name="Agent 1",
    instructions=(
    "You are a helpful assistant. The user has already uploaded a PDF file. "
    "If the user asks any question related to that PDF, use the provided tool "
    "`answer_from_pdf` to search the knowledge base and generate the answer. "
    "Do not answer on your own. Always use the tool."
     ),

    model=model,
    tools=[answer_from_pdf],
)

async def ask_question_from_agent(input_text ):
    answer = await Runner.run(agent, input_text , run_config=config)
    print("Answer from agent : \n",answer.final_output)
    return answer.final_output