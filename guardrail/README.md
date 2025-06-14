# 🛡️ Guardrails in Agents – Coding Filter Project

## 📌 What are Guardrails?

**Guardrails** are rules that check or validate the input and output of an AI agent to make sure the agent behaves the way we want.

They are used to:
- ❌ **Stop** unwanted questions (e.g., off-topic or harmful queries)
- ✅ **Ensure** the response is related to the expected topic (e.g., programming)

---

## 💡 Types of Guardrails

There are **two types** of guardrails:

### 1. Input Guardrail
> Checks if the user's input is valid or on-topic **before** the AI processes it.

For example:
- Input: `"What is a variable in Python?"` ✅ (allowed)
- Input: `"Who is the president?"` ❌ (blocked)

### 2. Output Guardrail
> Checks the AI's response **after** generation to confirm it's relevant.

For example:
- Output: `"A lambda function is used to create anonymous functions."` ✅
- Output: `"I like pizza."` ❌ (rejected)

---

## 🧭 Where Are Guardrails Applied?

- ✅ **Input guardrails** are applied **only if the agent is the first agent in the chain**.  
  That's because guardrails should filter **user input** before it reaches any other processing.

- ✅ **Output guardrails** are applied **only if the agent is the last agent in the chain**.  
  That ensures that the **final response** is safe and relevant.

> 🔁 Guardrails are added inside the agent definition (not passed separately to `Runner.run`) because they are specific to that agent. This makes your code **clean and easy to read**, especially when multiple agents have different rules.

---

## ⚙️ How it Works in This Project

### 🎯 Objective:
Only allow **coding-related** questions and answers.

### 👇 Workflow:
1. **User Input** → Passes through `input_guardrail`
2. If valid → Sent to main `Coding Agent`
3. Response → Checked by `output_guardrail`
4. Final answer is shown if both checks pass

---


## 🔒 Example Guardrail Model

### Input Guardrail Model:
``` from agents import (
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
            "what is lambda function in python?",
            run_config=config
        )
      
        print(runner.final_output)

    except InputGuardrailTripwireTriggered as e:
        print("Your  Question not related about Coding: I couldn't help you. Please try again" )

    except OutputGuardrailTripwireTriggered as e:
        print("Output not related about Coding:  Please try again", e)



if __name__ == "__main__":
    asyncio.run(main())
