"""MCP Server implementation with read-only document access."""
import os
from pathlib import Path
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import ALLOWED_DIRECTORIES, is_path_allowed
from .logger import logger, log_tool_call

# Create server instance
app = Server("readonly-docs-server")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_docs",
            description="Search for documents in the allowed directories. Returns matching file paths with context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find in document contents"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_file",
            description="Read the contents of a file from allowed directories. Returns file content with source path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read (must be within allowed directories)"
                    }
                },
                "required": ["path"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "search_docs":
            result = await search_docs(arguments.get("query", ""))
            log_tool_call("search_docs", arguments, True, result)
            return [TextContent(type="text", text=result)]

        elif name == "get_file":
            result = await get_file(arguments.get("path", ""))
            log_tool_call("get_file", arguments, True, result)
            return [TextContent(type="text", text=result)]

        else:
            error_msg = f"Unknown tool: {name}"
            log_tool_call(name, arguments, False, error=error_msg)
            return [TextContent(type="text", text=f"Error: {error_msg}")]

    except Exception as e:
        error_msg = str(e)
        log_tool_call(name, arguments, False, error=error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]

async def search_docs(query: str) -> str:
    """Search for documents containing the query string."""
    if not query:
        raise ValueError("Query cannot be empty")

    results = []
    query_lower = query.lower()

    for allowed_dir in ALLOWED_DIRECTORIES:
        if not allowed_dir.exists():
            logger.warning(f"Allowed directory does not exist: {allowed_dir}")
            continue

        for file_path in allowed_dir.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip binary files
            if file_path.suffix in ['.pyc', '.so', '.dylib', '.png', '.jpg', '.jpeg', '.gif']:
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if query_lower in content.lower():
                    # Find context around the match
                    lines = content.split('\n')
                    matching_lines = [
                        (i, line) for i, line in enumerate(lines, 1)
                        if query_lower in line.lower()
                    ]

                    results.append({
                        "path": str(file_path),
                        "matches": len(matching_lines),
                        "preview": matching_lines[:3]  # First 3 matches
                    })
            except Exception as e:
                logger.debug(f"Could not read file {file_path}: {e}")
                continue

    if not results:
        return f"No documents found matching query: '{query}'\nSearched in: {', '.join(str(d) for d in ALLOWED_DIRECTORIES)}"

    # Format results
    output = [f"Found {len(results)} document(s) matching '{query}':\n"]
    for result in results:
        output.append(f"\n📄 {result['path']}")
        output.append(f"   Matches: {result['matches']}")
        if result['preview']:
            output.append("   Preview:")
            for line_num, line in result['preview']:
                output.append(f"   Line {line_num}: {line.strip()[:100]}")

    return '\n'.join(output)

async def get_file(path: str) -> str:
    """Read and return the contents of a file."""
    if not path:
        raise ValueError("Path cannot be empty")

    file_path = Path(path)

    # Security check: ensure path is within allowed directories
    if not is_path_allowed(file_path):
        allowed_paths = '\n'.join(f"  - {d}" for d in ALLOWED_DIRECTORIES)
        raise PermissionError(
            f"Access denied: Path '{path}' is not within allowed directories.\n"
            f"Allowed directories:\n{allowed_paths}"
        )

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    # Read file content
    try:
        content = file_path.read_text(encoding='utf-8')

        # Format output with metadata
        output = [
            f"📄 File: {file_path}",
            f"📏 Size: {len(content)} characters",
            f"📝 Lines: {len(content.splitlines())}",
            "─" * 80,
            content,
            "─" * 80,
            f"✓ Source: {file_path.resolve()}"
        ]

        return '\n'.join(output)

    except UnicodeDecodeError:
        raise ValueError(f"Cannot read file (not a text file): {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

async def main():
    """Run the MCP server."""
    logger.info("Starting MCP readonly-docs-server")
    logger.info(f"Allowed directories: {', '.join(str(d) for d in ALLOWED_DIRECTORIES)}")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="readonly-docs-server",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
