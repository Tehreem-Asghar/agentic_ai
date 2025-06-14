from agents import (
    Agent, TResponseInputItem, Runner, OpenAIChatCompletionsModel,
    AsyncOpenAI, input_guardrail, GuardrailFunctionOutput,
    RunContextWrapper, InputGuardrailTripwireTriggered
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
class Is_MathHomework_input(BaseModel):
    is_math_homework: bool
    reason: str
    answer: str

# Guardrail Agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="check user ask about math homework related questions",
    output_type=Is_MathHomework_input
)

# Guardrail function
@input_guardrail
async def input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        input,
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
    input_guardrails=[input_guardrail],
    output_type=Is_MathHomework_input
)

# Run the agent
async def main():
    try:
        runner = await Runner.run(
            agent,
            "what is 2 + 2?",
            run_config=config
        )
        print("is_math_homework : ",runner.final_output.is_math_homework)
        print("Reason : " ,runner.final_output.reason)
        print("Answer : ",runner.final_output.answer)

    except InputGuardrailTripwireTriggered as e:
        print("Your  Question not related about math homework: try again", e)

asyncio.run(main())