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
