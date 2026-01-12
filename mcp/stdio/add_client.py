from fastmcp import Client
import asyncio

# Connect to the Add Server using STDIO transport
client = Client('add_server.py')

async def call_tool():
    async with client:
        # List available tools from the server
        tools = await client.list_tools() 
        print("Available tools:", [t.name for t in tools])

      

        # Call add
        result = await client.call_tool("add", {"a": 5, "b": 7})
        print("Result of add(5, 7):", result.content[0].text)


asyncio.run(call_tool())

