#!/usr/bin/env python3
"""Run the MCP server."""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
