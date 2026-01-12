from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Resource Server")

@mcp.resource("resource://greeting/{name}")
def get_greeting(name : str) -> str:
    """Provides a simple greeting message."""
    return f"Hello {name}, welcome to MCP Server Resources"

if __name__ == '__main__':
    mcp.run(transport="http", port=9999)