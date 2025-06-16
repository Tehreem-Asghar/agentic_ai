from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , trace
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import agentops
load_dotenv()

API_KEY = os.getenv("api_key")
agentops.init(os.getenv("ops_api_key"))

if not API_KEY:
    raise ValueError("API key is not set in the environment variables.")



# 🌐 Step 1: Provider
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🔍 Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# ⚙️ Step 3: Config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,

)

# 🧠 Step 4: Agent
agent: Agent = Agent(
    name="Restaurant Order",
    instructions="Handle customer food orders.",
    model=model,
  
)

# 🚀 Step 5: Runner
async def main():
    
    with trace("Meal Workflow"): 
        burger_result = await Runner.run(agent, "Make a burger" , run_config=config)
        dessert_result = await Runner.run(agent, "Make a dessert" , run_config=config)
        print(f"Burger: {burger_result.final_output}")
        print(f"Dessert: {dessert_result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())