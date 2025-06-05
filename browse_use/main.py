import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

async def main():
    agent = Agent(
        task = "open the browser and go to https://github.com/Tehreem-Asghar this is my github profile and open my agentic-ai repository",
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    )
    await agent.run()

asyncio.run(main()) 