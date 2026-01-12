import asyncio
from fastmcp import Client

client = Client("http://localhost:9999/mcp")

async def greet(user : str):
    async with client:
        # Call resource 
        result = await client.read_resource(f"resource://greeting/{user}")
        print(result[0].text)

asyncio.run(greet("Srikanth"))