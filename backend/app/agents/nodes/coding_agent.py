from langgraph.prebuilt import create_react_agent

from app.agents.prompts.loader import load_prompt
from app.agents.tools.java_tools import java_syntax_check, code_formatter
from app.agents.tools.file_tools import file_reader, file_writer
from app.core.llm_factory import create_llm


def build_coding_agent():
    """Build the coding agent as a ReAct agent.

    The coding agent specializes in Java code generation, analysis, and debugging.
    It uses tools for syntax checking and code formatting.
    """
    llm = create_llm()
    system_prompt = load_prompt("coding_system")

    tools = [java_syntax_check, code_formatter, file_reader, file_writer]

    return create_react_agent(
        model=llm,
        tools=tools,
        name="coding_agent",
        prompt=system_prompt,
    )
