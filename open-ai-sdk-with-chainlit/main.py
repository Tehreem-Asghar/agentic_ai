import chainlit as cl
from dotenv import load_dotenv, find_dotenv
import os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("api_key")

# Step 1: Provider
provider = AsyncOpenAI(
      api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

# Step 3: Config
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Step 4: Agent (✅ Use different name than class)
agent = Agent(
    name="Doctor",
    instructions="You are a doctor who helps patients with their health issues. You are friendly and professional.",
    model=model
)

# Step 5: Runner
# input = input("Enter your message: ")
# result = Runner.run_sync(agent, input , run_config=config)

# print(result.final_output)


# Step 5: Runner
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I am your virtual doctor. How can I assist you today?").send()

# @cl.on_message
# async def handle_message(message: cl.Message):
#     # Retrieve the conversation history
#     history = cl.user_session.get("history", [])
    
#     # Append the new message to the history
#     history.append({"role": "user", "content": message.content})
    
#     # Prepare the input for the agent, including the history
#     input_text = "\n".join([f"{entry['role']}: {entry['content']}" for entry in history])
    
#     # Run the agent with the updated input
#     result = Runner.run_streamed(agent, input=input_text, run_config=config)

#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             print(event.data.delta, end="", flush=True)

#     # Append the agent's response to the history
#     history.append({"role": "doctor", "content": result.final_output})
    
#     # Update the session with the new history
#     cl.user_session.set("history", history)

#     await cl.Message(content=result.final_output).send()



@cl.on_message
async def handle_message(message: cl.Message):
    # Retrieve the conversation history
    history = cl.user_session.get("history", [])
    
    # Append the new message to the history
    history.append({"role": "user", "content": message.content})
    
    # Prepare the input for the agent, including the history
    input_text = "\n".join([f"{entry['role']}: {entry['content']}" for entry in history])
    
    # Run the agent with the updated input
    result = Runner.run_streamed(agent, input=input_text, run_config=config)

    # Initialize a variable to store the complete response
    complete_response = ""

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # Append the delta to the complete response
            complete_response += event.data.delta
            
            # Send the current delta to the user
            await cl.Message(content=event.data.delta).send()

    # Append the complete response to the history
    history.append({"role": "doctor", "content": complete_response})
    
    # Update the session with the new history
    cl.user_session.set("history", history)

    # Optionally, send the final complete response to the user
    await cl.Message(content=complete_response).send()










# @cl.on_chat_start
# async def on_chat_start():
#     # cl.user_session.set("history",[])
#     await cl.Message(content="Hello! I am your virtual doctor. How can I assist you today?").send()


# @cl.on_message
# async def handle_message(message: cl.Message):
#     result = Runner.run_streamed(agent, input=message.content, run_config=config) 

#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             print(event.data.delta, end="", flush=True)

#     await cl.Message(content=result.final_output).send()
