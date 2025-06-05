# code is right running
# This code is a Chainlit application that integrates with the Gemini API to create an AI programming assistant.

import os
from dotenv import load_dotenv
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()
API_KEY = os.getenv("api_key")

if not API_KEY:
    raise ValueError("API_KEY is missing. Please check your .env file.")

@cl.on_chat_start
async def on_chat_start():


# step 1 : Provider
    external_client = AsyncOpenAI(
        api_key=API_KEY ,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    

# step 2 : Model    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",  # ✅ make sure this model exists
        openai_client=external_client
     )

# step 3 : Config
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
     )

# step 4 : Agent
    agent: Agent = Agent(
    name="coder",
    instructions=(
        "You are Coder, an expert programming assistant. "
        "Your job is to help users with clean, efficient, and well-explained code in Python, JavaScript, TypeScript, React, and Next.js. "
        "Always provide accurate solutions, include helpful comments in code, and keep your responses simple and beginner-friendly. "
        "If a user asks for explanation, use real-life examples and explain step-by-step in plain language. "
        "If the question is unclear, politely ask for more details. Never assume or hallucinate answers. "
        "Keep a friendly tone and encourage learning."
    ),
    model=model,
     )



# step 5 : history , config and agent in session
    """Set up the chat session when a user connects."""
   
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    cl.user_session.set("agent", agent)

    # Send a welcome message to the user
    await cl.Message(content="👋 Hello! I'm Coder, your AI programming assistant. Whether you're stuck with code, debugging, or just want to learn something new — I'm here to help! 🚀").send()



@cl.on_message
async def on_message(message: cl.Message):
    """Process incoming messages and generate responses."""

    # Send a thinking message to indicate processing
    msg = cl.Message(content="Thinking...")
    await msg.send() # This sends the message to the user interface

    agent : Agent = cast(Agent, cl.user_session.get("agent")) # Retrieve the agent from the session
    config : RunConfig = cast(RunConfig, cl.user_session.get("config")) # Retrieve the run configuration from the session

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role" : "user" , "content" : message.content })


    try:
        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        response_content  = result.final_output

        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()
        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        a = result.to_input_list()
        print(f"""=========================
              {a}
              ==========================""")
    #   Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")        












# import os
# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load the environment variables from the .env file
# load_dotenv()

# gemini_api_key = os.getenv("api_key")

# # Check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


# @cl.on_chat_start
# async def start():
#     #Reference: https://ai.google.dev/gemini-api/docs/openai
#     external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )

#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )
#     """Set up the chat session when a user connects."""
#     # Initialize an empty chat history in the session.
#     cl.user_session.set("chat_history", [])

#     cl.user_session.set("config", config)
#     agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
#     cl.user_session.set("agent", agent)

#     await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     """Process incoming messages and generate responses."""
#     # Send a thinking message
#     msg = cl.Message(content="Thinking...")
#     await msg.send()

#     agent: Agent = cast(Agent, cl.user_session.get("agent"))
#     config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

#     # Retrieve the chat history from the session.
#     history = cl.user_session.get("chat_history") or []
    
#     # Append the user's message to the history.
#     history.append({"role": "user", "content": message.content})
    

#     try:
#         print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
#         result = Runner.run_sync(starting_agent = agent,
#                     input=history,
#                     run_config=config)
        
#         response_content = result.final_output
        
#         # Update the thinking message with the actual response
#         msg.content = response_content
#         await msg.update()
    
#         # Update the session with the new history.
#         cl.user_session.set("chat_history", result.to_input_list())
#         # a = result.to_input_list()
#         # print(f"""=========================
#         #       {a}
#         #       ==========================""")
        
#         # Optional: Log the interaction
#         print(f"User: {message.content}")
#         print(f"Assistant: {response_content}")
        
#     except Exception as e:
#         msg.content = f"Error: {str(e)}"
#         await msg.update()
#         print(f"Error: {str(e)}")