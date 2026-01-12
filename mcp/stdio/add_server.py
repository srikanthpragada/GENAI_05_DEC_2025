from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Add Server")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


mcp.run(transport='stdio')
 