import os
from itertools import chain

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def linkedin_summarizer(name_and_info: str) -> str:
    linkedin_url = linkedin_lookup_agent(name_and_info=name_and_info)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """
            Given the Linkedin information {information} about a {entity} from I want you to create:
            1. A short summary
            2. Two interesting facts about them
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "entity"], template=summary_template
    )

    llm = ChatOllama(model="llama3.1")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data, "entity": "person"})

    return res

if __name__ == "__main__":
    load_dotenv()
    print("LinkedIn Summarizer")

    res = linkedin_summarizer(name_and_info="Shubham Phapale VNIT Nagpur")

    print(res)
