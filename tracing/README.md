# 📊 Tracing in Agentic AI Projects

This README explains **Tracing** in Agentic AI applications using OpenAI's Agents SDK. Tracing helps developers **visualize, debug, and monitor** agent workflows by capturing every step (like API calls, model outputs, spans, and logic flow).

---

## 🔍 What is Tracing?

Tracing is the process of **tracking and recording the flow of your AI agent’s operations** — such as when it:

- starts a task (trace)
- calls a function (span)
- generates LLM output
- returns a final response

It helps you answer questions like:

> 🔹 "Which part took the most time?"  
> 🔹 "What was the input and output of the model?"  
> 🔹 "Where did the error occur in the agent's run?"

---

## ✨ Types of Tracing Used

### ✅ 1. **Local Tracing (Terminal Output)**

You can create your own custom tracing processor to print trace & span information directly to the terminal:

```python
from agents import Agent,set_trace_processors, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , trace
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from agents.tracing.processor_interface import TracingProcessor


load_dotenv()


API_KEY = os.getenv("api_key")

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

class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started: {trace.trace_id}")

    def on_trace_end(self, trace):
        print(f"Trace ended: {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)
        print("*"*20)
        print(f"Span started: {span.span_id}")
        print(f"Span details: ")
        print(span.export())

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(f"Span details:")
        print(span.export())

    def force_flush(self):
        print("Forcing flush of trace data")

    def shutdown(self):
        print("=======Shutting down trace processor========")
        # Print all collected trace and span data
        print("Collected Traces:")
        for trace in self.traces:
            print(trace.export())
        print("Collected Spans:")
        for span in self.spans:
            print(span.export())

LocalProcessor = LocalTraceProcessor()
set_trace_processors([LocalProcessor])

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

```


#  2. AgentOps Integration (Dashboard Monitoring)
# AgentOps provides cloud-based tracing and observability for your agents.

- Just initialize:
```
import agentops
agentops.init("YOUR_AGENTOPS_API_KEY")
```
---------------------------------------------------
```
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

```

- Now, all traces/spans will be visible in the AgentOps dashboard — perfect for teams and production use.

# 🛠️ How Tracing Works (Under the Hood)
## Trace
- Represents a full logical task like:
- "Prepare a meal order"

# ✅ Spans
Nested units inside the trace, like:

- "Calling LLM for burger"

- "Executing function make_dessert()"

# Spans capture:

- start & end time

- input/output data

- parent-child relationship

- model usage or function calls

## Sensitive Data Handling
- To disable sensitive data tracing:

```
RunConfig(trace_include_sensitive_data=False)
```
- To skip audio content in voice pipelines:

```
VoicePipelineConfig(trace_include_sensitive_audio_data=False)

```
## 💼 Use-Cases for Tracing

🔍 Debug broken runs or unexpected outputs

⚙️ Optimize performance (track time spent in each span)

🧪 Understand agent decision-making

📈 Monitor agent performance in production with AgentOps

