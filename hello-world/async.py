import asyncio
from dotenv import load_dotenv
import os
from agents import Agent, Runner , AsyncOpenAI, OpenAIChatCompletionsModel 
from agents.run import RunConfig  # ✅ Correct import

load_dotenv()

gemini_api_key = os.getenv("api_key")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(  # ✅ Correct usage
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=model  # ✅ Required: pass model here too
    )

    result = await Runner.run(agent, "What is the meaning of life?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
