from dotenv import load_dotenv
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import nest_asyncio
nest_asyncio.apply()


load_dotenv()

gemini_api_key = os.getenv("api_key")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Custom model of gemini-2.0-flash
agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config) # ya runner hamara agents sa kam krwana ka zumadar hai ya runner ka andar hamara pass mukhtalif method hai 

print("\nCALLING AGENT\n")
print(result.final_output)




# .venv\Scripts\activate