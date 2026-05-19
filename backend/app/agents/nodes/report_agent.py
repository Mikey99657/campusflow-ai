from langgraph.prebuilt import create_react_agent

from app.agents.prompts.loader import load_prompt
from app.agents.tools.file_tools import file_reader, file_writer
from app.core.llm_factory import create_llm


def build_report_agent():
    """Build the report agent as a ReAct agent.

    The report agent specializes in generating lab reports, experiment summaries,
    and academic writing.
    """
    llm = create_llm()
    system_prompt = load_prompt("report_system")

    tools = [file_reader, file_writer]

    return create_react_agent(
        model=llm,
        tools=tools,
        name="report_agent",
        prompt=system_prompt,
    )
