"""Test client for the MCP server."""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_search_docs():
    """Test the search_docs tool."""
    import os
    server_script = os.path.join(os.path.dirname(__file__), "..", "run_server.py")
    server_params = StdioServerParameters(
        command="python3",
        args=[server_script],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\n=== Available Tools ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test search_docs
            print("\n=== Testing search_docs ===")
            result = await session.call_tool("search_docs", arguments={"query": "Day"})
            print(result.content[0].text)

            # Test get_file with a valid path
            print("\n=== Testing get_file (valid path) ===")
            result = await session.call_tool(
                "get_file",
                arguments={"path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md"}
            )
            print(result.content[0].text[:500] + "..." if len(result.content[0].text) > 500 else result.content[0].text)

            # Test get_file with invalid path (should fail)
            print("\n=== Testing get_file (invalid path - should fail) ===")
            try:
                result = await session.call_tool(
                    "get_file",
                    arguments={"path": "/etc/passwd"}
                )
                print(result.content[0].text)
            except Exception as e:
                print(f"Expected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_search_docs())
