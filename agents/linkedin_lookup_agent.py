from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

load_dotenv()

def lookup(name_and_info: str) -> str:
    # llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    llm = ChatOllama(model="llama3.1")

    template = """
        Given the full name and some info {name_and_info_of_person}, find and return their LinkedIn profile URL.
        You MUST return ONLY the LinkedIn profile URL without any additional text, explanations, or formatting.
        The URL should be in the format: https://linkedin.com/in/... or https://[country].linkedin.com/in/...
    """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_and_info_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the linkedin Page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input" : prompt_template.format_prompt(name_and_info_of_person=name_and_info)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name_and_info="Shubham Phapale NIT Nagpur")
    print(linkedin_url)