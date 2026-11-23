import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv
import time
import os

load_dotenv()

llm = ChatGroq(model='qwen/qwen3.8-27b')

SERVERS = {
#   "expense-tracker-local": {
#     "transport": "stdio",
#     "command": "uv",
#     "args": [
#       "run",
#       "--with",
#       "fastmcp",
#       "fastmcp",
#       "run",
#       "C:\\NJ\\Projects\\MCP\\expense_tracker_mcp_server\\src\\expense_tracker_mcp_server\\main.py"
#     ]
#   },
  "expense-tracker-remote": {
      "transport": "streamable_http",
      "url": "https://njnjpj.fastmcp.app/mcp",
      "headers": {
          "Authorization": f"Bearer {os.environ['HORIZON_API_KEY']}"
      }
  }
}

async def main():
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()

    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool
        
    llm_with_tools = llm.bind_tools(tools)

    prompt = "Add an expense of Rs 11000 for exotic fruits on 22 Nov 2026"
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print(response.content)
        return
    
    selected_tool = response.tool_calls[0]["name"]
    selected_tool_args = response.tool_calls[0]["args"]
    selected_tool_id = response.tool_calls[0]["id"]

    tool_result = await named_tools[selected_tool].ainvoke(selected_tool_args)

    tool_message = ToolMessage(content=tool_result, tool_call_id=selected_tool_id)

    final_response = await llm_with_tools.ainvoke([prompt, response, tool_message])
    print(final_response.content)

if __name__ == "__main__":
    asyncio.run(main())