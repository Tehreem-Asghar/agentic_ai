from agents import (
    Agent,
    TResponseInputItem,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    OutputGuardrailTripwireTriggered,
    InputGuardrailTripwireTriggered,
    input_guardrail
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
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=External_Client,
)

# Config for agent runs
config = RunConfig(
    model=model,
    model_provider=External_Client,
    tracing_disabled=True,
)


class Is_Coding_input(BaseModel):
    is_coding: bool
    reason: str
    answer: str

coding_input_guardrail = Agent(
    name = "Coding Guardrail Agent",
    instructions = "Check if the user's input is related to programming or coding.",
    output_type = Is_Coding_input
    
)

@input_guardrail
async def is_coding_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        coding_input_guardrail,
        input,
        context=ctx.context,
        run_config=config
    )


    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_coding
    )


class MessageOutput(BaseModel):
    response: str

class Is_Coding_output(BaseModel):
    is_coding: bool
    reason: str
    answer: str


check_agent = Agent(
    name = "Coding Guardrail Agent",
   instructions = """
Check the output to ensure it is about programming or coding.
"""
,
    output_type=Is_Coding_output
)

@output_guardrail      
async def output_guardrail(
    ctx : RunContextWrapper[None] , agent : Agent , output : MessageOutput
)-> GuardrailFunctionOutput:
    result = await Runner.run(
        check_agent,
        output.response,
        context=ctx.context,
        run_config=config
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_coding
    )
    


Coding_Agent = Agent(
    name = "Coding Agent",
    instructions = "You are a coding expert. You help customers with their coding questions.",
    input_guardrails=[is_coding_guardrail],
    output_guardrails=[output_guardrail],
    output_type=MessageOutput,
)


async def main():
    try:
        runner = await Runner.run(
            Coding_Agent,
            "write a function that adds two numbers in python?",
            run_config=config
        )
      
        print(runner.final_output.response)

    except InputGuardrailTripwireTriggered as e:
        print("Your  Question not related about Coding: I couldn't help you. Please try again" )

    except OutputGuardrailTripwireTriggered as e:
        print("Output not related about Coding:  Please try again", e)



if __name__ == "__main__":
    asyncio.run(main())
