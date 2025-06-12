from agents import Agent , AsyncOpenAI , OpenAIChatCompletionsModel , Runner
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from pydantic import BaseModel



load_dotenv()
# Set the OpenAI API key from environment variables
api_key = os.getenv("api_key")
if not api_key:
    raise ValueError("API key not found. Please set the 'api_key' environment variable.")


External_client = AsyncOpenAI(
    api_key = api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = External_client
)

config = RunConfig(
    model=model,
    model_provider=External_client,
    tracing_disabled=True,
)

class Quiz_Answer(BaseModel):
    Question: str
    Options: list[str]
    Answer: str


agent = Agent(
    name="Quiz Agent",
    instructions="""
You are a Python Quiz Agent.

When a user asks for a Python quiz, respond with one multiple-choice question related to Python programming. Your response must follow a strict structured format defined by the output schema.

Please provide:
- A clear and concise Python-related question.
- Four multiple-choice options as a list of strings.
- The correct answer selected from the options.

Make sure your response is informative, accurate, and suitable for beginner to intermediate Python learners.

Respond with only one question per request in the structured format.
""",
    output_type=Quiz_Answer,
    model=model
)

async def main():
    runner = await Runner.run(
        agent,
        "Give me a Python quiz question.",
        run_config=config,
    )
 
    result = runner.final_output

    print("\n🧠 Python Quiz Question:")
    print(f"❓ Question: {result.Question}")
    print("\n🔘 Options:")
    for option in result.Options:
        print(f"- {option}")
    print(f"\n✅ Correct Answer: {result.Answer}")



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())