from pathlib import Path
from langchain_core.tools import tool

# Default working directory for file operations
WORK_DIR = Path("./workspace")
WORK_DIR.mkdir(exist_ok=True)


@tool
def file_reader(filename: str) -> str:
    """Read content from a file in the workspace.

    Args:
        filename: Name of the file to read

    Returns:
        File content
    """
    file_path = WORK_DIR / filename

    if not file_path.exists():
        return f"Error: File '{filename}' not found."

    if not file_path.is_file():
        return f"Error: '{filename}' is not a file."

    try:
        content = file_path.read_text(encoding="utf-8")
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def file_writer(filename: str, content: str) -> str:
    """Write content to a file in the workspace.

    Args:
        filename: Name of the file to write
        content: Content to write

    Returns:
        Success message
    """
    file_path = WORK_DIR / filename

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_files(directory: str = ".") -> str:
    """List files in a workspace directory.

    Args:
        directory: Directory path relative to workspace

    Returns:
        List of files
    """
    dir_path = WORK_DIR / directory

    if not dir_path.exists():
        return f"Error: Directory '{directory}' not found."

    if not dir_path.is_dir():
        return f"Error: '{directory}' is not a directory."

    try:
        files = []
        for item in sorted(dir_path.iterdir()):
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            files.append(f"{prefix} {item.name}")

        if not files:
            return "Directory is empty."

        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"
