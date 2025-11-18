from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

# Available tools for the agent
tools = [TavilySearch()]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
structured_llm = llm.with_structured_output(AgentResponse)
# Pull the community React agent prompt template (used below).
react_prompt = hub.pull("hwchase17/react")
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
    partial_variables={
        "format_instructions": (
            "\nDo not include ```json or ``` fences. Only return valid JSON."
        )
    },
)


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)
extract_output = RunnableLambda(lambda x: x["output"])
# parse_output = RunnableLambda(lambda x: output_parser.parse(x))
# chain = agent_executor | extract_output | parse_output
chain = agent_executor | extract_output | structured_llm


def main():
    # The natural language query we want the agent to handle.
    query = (
        "search for 3 job postings for an ai engineer using langchain in the "
        "banglore area online and list their details and the url of the source "
        "and the job posting should be open and for freshers"
    )

    try:
        result = chain.invoke(input={"input": query})
        print(result)
    except KeyboardInterrupt:
        # Allow user to cancel with Ctrl-C without a long traceback.
        print("Interrupted by user.")
    except Exception as exc:  # noqa: BLE001 - broad catch for top-level script
        # Print a concise error message to help debugging.
        print("Error running agent:", type(exc).__name__, str(exc))


if __name__ == "__main__":
    main()
