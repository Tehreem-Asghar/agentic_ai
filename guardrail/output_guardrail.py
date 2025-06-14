from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    AsyncOpenAI, output_guardrail, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered,
    RunContextWrapper
)
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import asyncio

# Load API Key
load_dotenv()
API_key = os.getenv("api_key")
if not API_key:
    raise ValueError("API key not found. Please set the 'api_key' environment variable.")

# Set up client and model
External_Client = AsyncOpenAI(
    api_key=API_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=External_Client,
)

# Config for agent runs
config = RunConfig(
    model=model,
    model_provider=External_Client,
    tracing_disabled=True,  # Tracing off for now
)

# Define expected output schema
class Is_MathHomework_output(BaseModel):
    is_math_homework: bool
    reason: str
    answer: str

# Guardrail Agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="check output is related math homework",
    output_type=Is_MathHomework_output
)

class MessageOutput(BaseModel):
    response: str

# Guardrail function
@output_guardrail
async def output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        output.response,
        context=ctx.context,
        run_config=config
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_math_homework
    )

# Main Agent
agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[output_guardrail],
    output_type=MessageOutput
)

# Run the agent
async def main():
    try:
        runner = await Runner.run(
            agent,
            "how are you?",
            run_config=config
        )
        print(runner.final_output)

    except OutputGuardrailTripwireTriggered as e:
        print("Output not related about math homework:  Please try again")

asyncio.run(main())