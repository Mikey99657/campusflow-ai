import subprocess
import tempfile
from pathlib import Path
from langchain_core.tools import tool


@tool
def java_syntax_check(code: str) -> str:
    """Check Java code for syntax errors.

    Args:
        code: Java code to check

    Returns:
        Syntax check result
    """
    # Extract class name from code
    class_name = "Main"
    for line in code.split("\n"):
        if "public class" in line:
            parts = line.split()
            idx = parts.index("class")
            if idx + 1 < len(parts):
                class_name = parts[idx + 1].split("{")[0].strip()

    with tempfile.TemporaryDirectory() as tmpdir:
        java_file = Path(tmpdir) / f"{class_name}.java"
        java_file.write_text(code, encoding="utf-8")

        try:
            result = subprocess.run(
                ["javac", str(java_file)],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return "Syntax check passed: No errors found."
            else:
                return f"Syntax errors found:\n{result.stderr}"
        except FileNotFoundError:
            return "Java compiler (javac) not found. Please install JDK."
        except subprocess.TimeoutExpired:
            return "Syntax check timed out."


@tool
def code_formatter(code: str) -> str:
    """Format Java code with proper indentation.

    Args:
        code: Java code to format

    Returns:
        Formatted code
    """
    lines = code.split("\n")
    formatted_lines = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        # Decrease indent for closing braces
        if stripped.startswith("}"):
            indent_level = max(0, indent_level - 1)

        # Add indented line
        if stripped:
            formatted_lines.append("    " * indent_level + stripped)
        else:
            formatted_lines.append("")

        # Increase indent for opening braces
        if stripped.endswith("{"):
            indent_level += 1

    return "\n".join(formatted_lines)
