from langgraph.prebuilt import create_react_agent

from app.agents.prompts.loader import load_prompt
from app.agents.tools.file_tools import file_reader, file_writer
from app.core.llm_factory import create_llm


def build_summary_agent():
    """Build the summary agent as a ReAct agent.

    The summary agent specializes in creating learning summaries and
    consolidating course notes.
    """
    llm = create_llm()
    system_prompt = load_prompt("summary_system")

    tools = [file_reader, file_writer]

    return create_react_agent(
        model=llm,
        tools=tools,
        name="summary_agent",
        prompt=system_prompt,
    )
