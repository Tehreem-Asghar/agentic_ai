from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, ModelSettings
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

API_KEY = os.getenv("api_key")
if not API_KEY:
    raise ValueError("API key is not set in the environment variables.")

# 🌦️ Step 0: Define Context Data
@dataclass
class WeatherContext:
    city: str
    country: str

# 🛠 Step 1: Function Tool
@function_tool
async def generate_weather_report(data: RunContextWrapper[WeatherContext]) -> str:
    return f"The weather report for {data.context.city}, {data.context.country} has been generated successfully."

# 🌐 Step 2: Provider
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🔍 Step 3: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# ⚙️ Step 4: Config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
    model_settings=ModelSettings(tool_choice="required")
)

# 🧠 Step 5: Agent
agent: Agent = Agent[WeatherContext](
    name="WeatherBot",
    instructions="You are an assistant that generates weather reports based on city and country.",
    model=model,
    tools=[generate_weather_report]
)

# 🚀 Step 6: Runner
async def main():
    runner = await Runner.run(
        starting_agent=agent,
        input="Can you give me a weather update?",
        run_config=config,
        context=WeatherContext(city="Karachi", country="Pakistan")
    )

    print(runner.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
