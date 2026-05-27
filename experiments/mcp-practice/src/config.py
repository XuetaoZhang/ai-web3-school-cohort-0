"""Configuration for the MCP server."""
import os
from pathlib import Path
from typing import List

# Base directory for the project
BASE_DIR = Path("/Users/zhangxuetao/ai-web3-school-cohort-0")

# Whitelist of allowed directories for file access
ALLOWED_DIRECTORIES: List[Path] = [
    BASE_DIR / "daily",
]

# Log file location
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "mcp_server.log"

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

def is_path_allowed(path: Path) -> bool:
    """Check if a path is within the allowed directories."""
    try:
        resolved_path = path.resolve()
        return any(
            resolved_path.is_relative_to(allowed_dir.resolve())
            for allowed_dir in ALLOWED_DIRECTORIES
        )
    except (ValueError, OSError):
        return False
