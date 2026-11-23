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
          "headers": {
              "Authorization": f"Bearer {os.environ['HORIZON_API_KEY']}"
          }
      }
}

async def main():
    client = MultiServerMCPClient(SERVERS) # type: ignore
    tools = await client.get_tools()

    agent = create_agent(llm, tools)

    response = await agent.ainvoke({'messages': [HumanMessage(content="Add an expense of Rs 1000 for fruits on 23 Nov 2026")]})

    print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())