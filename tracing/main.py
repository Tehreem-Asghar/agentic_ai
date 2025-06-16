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
