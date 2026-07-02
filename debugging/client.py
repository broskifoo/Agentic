from langchain_mcp_adapters import client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

if os.getenv("Groq_API_Key"):
    os.environ["GROQ_API_KEY"] = os.getenv("Groq_API_Key")

async def main():
    mcp_client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["./math_server.py"],##Ensure correct absolute path
                "transport":"stdio",
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp", ##
                "transport":"streamable_http",
            }
        }
    )
        
    # pyrefly: ignore [invalid-syntax]
    tools = await mcp_client.get_tools()
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("Gemini_API_Key"))
    agent = create_react_agent(model,tools)

    math_response = await agent.ainvoke(
        {"messages":[{"role":"user", "content":"what's (3+5)*12?"}]}
    )

    print("Math.response:",math_response["messages"][-1].content)

asyncio.run(main())
