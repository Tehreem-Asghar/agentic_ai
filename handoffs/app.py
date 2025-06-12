from agents import Agent , Runner , OpenAIChatCompletionsModel , AsyncOpenAI , handoff
from agents.run import RunConfig 
from dotenv import load_dotenv
import os

load_dotenv()

Api_KEY = os.getenv("api_key")
if not Api_KEY:
    raise ValueError("API key not found. Please set the 'api_key' environment variable.")

External_client = AsyncOpenAI(
    api_key = Api_KEY,
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



english_agent = Agent(
    name="English Agent",
    instructions="An agent that can assist with English language tasks.",
    model=model,
    
)

urdu_agent = Agent(
    name="Urdu Agent",
     instructions="An agent that can assist with Urdu language tasks.",
    model=model,
   
)


def on_handoff(ctx):
    print("Handoff:", ctx.handoff)
    print("handoff ho gaya")




a = handoff(
     agent = english_agent,
     tool_name_override="English Translation Tool",
     tool_description_override="A tool that can translate text from Urdu to English.",
     on_handoff=on_handoff,

)

main_agent = Agent(
    name="Main Agent",
    instructions="A main agent that can delegate tasks to other agents.",
    model=model,
    
    handoffs = [
        handoff(english_agent),
        handoff(urdu_agent),
    ]
)



async def main():
    runner = await Runner.run(
        main_agent,
        "Translate 'وعلیکم السلام! آپ کیسے ہیں؟ کیا میں آپ کی کوئی مدد کرسکتا ہوں؟' to in english.",
        run_config=config,
    )



    print("Main Agent Response:", runner.final_output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
