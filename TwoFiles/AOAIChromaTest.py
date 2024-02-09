from langchain import hub
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores.chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from dotenv import load_dotenv
import os 
import sys

#Load env variable and configure the embedding model
load_dotenv()
embedding_function = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("Embedding_model"),
    openai_api_version="2023-05-15"
    )

# Here we are loading our vector embedding database from the local storage. 
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
retriever = db.as_retriever()
prompt = hub.pull("hwchase17/openai-tools-agent")
llm = AzureChatOpenAI(deployment_name="AMGPT4Turbo", openai_api_version="2023-12-01-preview")

tool = create_retriever_tool(
    retriever,
    "search_norhtWind_insurance",
    "Searches and returns information about the northwind insurance.",
)
tools = [tool]

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

question = input("What do you like to ask?\n")

while "exit" not in question: 
    result = agent_executor.invoke({"input": question})
    print(result['output'])
    question = input("\n")
