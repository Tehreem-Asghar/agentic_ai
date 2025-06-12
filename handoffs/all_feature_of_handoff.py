from pydantic import BaseModel # type: ignore
from agents import Agent, handoff, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel , Runner # type: ignore
from agents.run import RunConfig # type: ignore
from agents.extensions import handoff_filters # type: ignore
from dotenv import load_dotenv # type: ignore
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

# Step 1: Create the Agent you're handing off to
refund_agent = Agent(name="Refund Agent")

# Step 2: Create input model to pass data during handoff
class RefundInput(BaseModel):
    order_id: str
    reason: str

# Step 3: Custom on_handoff logic
async def on_refund_handoff(ctx: RunContextWrapper[None], input_data: RefundInput):
    print("🔁 Handoff initiated to Refund Agent")
    print(f"🧾 Order ID: {input_data.order_id}")
    print(f"📝 Reason: {input_data.reason}")
    # Tum yahan koi API call ya DB fetch bhi kar sakti ho

# Step 4: Setup the handoff object with all features
refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="start_refund_process",
    tool_description_override="Use this tool to send the user to Refund Agent for order refunds.",
    on_handoff=on_refund_handoff,
    input_type=RefundInput,
    input_filter=handoff_filters.remove_all_tools  # Optional: remove tool calls from history
)

# Step 5: Create the main agent and pass the handoff
main_agent = Agent(
    name="Support Agent",
    instructions="""
    You are a support agent. You can hand off to the refund agent if someone asks for a refund.
    """,
    handoffs=[refund_handoff],
    model=model
)

async def main():
    # Example input that triggers handoff
    input_text = "I want a refund for order 12345 because the item is damaged."

    runner = await Runner.run(
        main_agent,
        input_text,
        run_config=config,
    )

    print("\n🤖 Main Agent Response:", runner.final_output)
    # print("📦 Handoff History:", runner.handoff_history)

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
