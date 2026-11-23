from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import asyncio
import time
import os

load_dotenv()

llm = ChatGroq(model='qwen/qwen3.8-27b')

SERVERS = {
    "expense-tracker-remote": {
          "transport": "streamable_http",
          "url": "https://njnjpj.fastmcp.app/mcp",
          "headers": {"X-API-Key": "sk_nitin_secret_123"}
            #   "Authorization": f"Bearer {os.environ['HORIZON_API_KEY']}"
      }
}

async def main():
    client = MultiServerMCPClient(SERVERS) # type: ignore
    tools = await client.get_tools()

    agent = create_agent(llm, tools)

    response = await agent.ainvoke({'messages': [HumanMessage(content="I have paid 16133 Rs for Term Insurance today, please add in my expense")]})

    print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())