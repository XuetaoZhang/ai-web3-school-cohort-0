"""Logging utilities for the MCP server."""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from .config import LOG_FILE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("mcp_server")

def log_tool_call(tool_name: str, arguments: Dict[str, Any], success: bool, result: Any = None, error: str = None):
    """Log a tool call with its arguments and result."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "arguments": arguments,
        "success": success,
    }

    if success:
        log_entry["result_summary"] = {
            "type": type(result).__name__,
            "length": len(str(result)) if result else 0
        }
    else:
        log_entry["error"] = error

    logger.info(f"Tool call: {json.dumps(log_entry, indent=2)}")
