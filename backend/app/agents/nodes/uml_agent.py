from langgraph.prebuilt import create_react_agent

from app.agents.prompts.loader import load_prompt
from app.agents.tools.file_tools import file_reader, file_writer
from app.core.llm_factory import create_llm


def build_uml_agent():
    """Build the UML agent as a ReAct agent.

    The UML agent specializes in UML diagram analysis and generation.
    """
    llm = create_llm()
    system_prompt = load_prompt("uml_system")

    tools = [file_reader, file_writer]

    return create_react_agent(
        model=llm,
        tools=tools,
        name="uml_agent",
        prompt=system_prompt,
    )
