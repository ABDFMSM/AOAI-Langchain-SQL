from sqlalchemy import create_engine, engine
from langchain.sql_database import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain.agents.agent_types import AgentType
import os 
from dotenv import load_dotenv

load_dotenv()

# Configuration to connect to Azure SQL DB
db_config = {
    'drivername': 'mssql+pyodbc', 
    'username': os.getenv('SQL_USERNAME') + '@' + os.getenv('SQL_ENDPOINT'), 
    'password': os.getenv('SQL_PASSWORD'), 
    'host': os.getenv('SQL_ENDPOINT'),
    'port': 1433, 
    'database': os.getenv('SQL_DATABASE'),
    'query': dict(driver='ODBC Driver 18 for SQL Server')
}

db_url = engine.URL.create(**db_config)
db = SQLDatabase.from_uri(db_url)

llm = AzureChatOpenAI(deployment_name="AMGPT4Turbo", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm) 

agent_executor = create_sql_agent(
    llm=llm, 
    toolkit=toolkit, 
    verbose=False, 
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
)

question = input("What do you like to ask?\n")
while "exit" not in question: 
    answer = agent_executor.run(question)
    print(answer)
    question = input("Do you have other queries you would like to know about?\n")




