## error in this file

import asyncio
from dotenv import load_dotenv
import os 
# from openai import AsyncOpenAI
from agents import Agent , Runner , AsyncOpenAI , OpenAIChatCompletionsModel , set_tracing_disabled



load_dotenv()

OPENROUTER_API_KEY = os.getenv("OpenRouterApiKey")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"


client = AsyncOpenAI(
    api_key = OPENROUTER_API_KEY,
    base_url = "https://openrouter.ai/api/v1",
)

set_tracing_disabled(True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())