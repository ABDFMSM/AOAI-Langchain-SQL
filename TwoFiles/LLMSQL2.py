import pandas as pd
import sys 
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent import AgentExecutor
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

load_dotenv()

class SQLLoader:    
    def __init__(self, df=None):    
        self.engine = self.create_engine()  
        self.df = df  
  
    def create_engine(self):  
        username = os.getenv('SQL_USERNAME')  
        password = os.getenv('SQL_PASSWORD')  
        server = f"tcp:{os.getenv('SQL_ENDPOINT')}"
        database = os.getenv('SQL_DATABASE')  
        driver = "ODBC Driver 18 for SQL Server"  
        connection_string = f"mssql+pyodbc:///?odbc_connect=DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"  
        engine = create_engine(connection_string)  
        return engine   

    def create_table(self, table_name):  
        # Use SQLAlchemy to generate the table schema from the dataframe  
        self.df.to_sql(table_name, self.engine, if_exists='replace', index=False)  
        print(f"Table {table_name} has been created in the database.")
      
    def insert_data(self, table_name):  
        # Use pandas to_sql method for inserting the data  
        self.df.to_sql(table_name, self.engine, if_exists='append', index=False)  
        print(f"Data has been inserted into {table_name} table.")

    def read_db(self):
        return SQLDatabase(self.engine)

      
# Usage example:  

if len(sys.argv[:]) > 1:
    df = pd.read_csv(sys.argv[1]).fillna(value=0)
    loader = SQLLoader(df)  
    table_name = input("What would you like to call the table?\n")
    loader.create_table(table_name)  
    loader.insert_data(table_name)
else:
    loader = SQLLoader() 

# Configuring the SQL agent: 
sql_db = loader.read_db()
llm = AzureChatOpenAI(deployment_name="AMGPT4Turbo", temperature=0)
toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm) 
context = toolkit.get_context()
tools = toolkit.get_tools()

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are an AI assistance who can access an Azure SQL Database to get answers to customer's questions. 
            You can check the table schema when you get an error from the sql database.
            Answer the question when you get an a non-error response from your sql_db_query.  
            When asked about finding books that talk about a certain subject you can use ProductName column to figure out which books might be related to the query. """
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        MessagesPlaceholder(
            variable_name='agent_scratchpad'
        ),
        HumanMessagePromptTemplate.from_template(
            "{input}"
        ),  # Where the human input will injected
    ]
)
prompt = prompt.partial(**context)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=False,
    memory=memory, 
    max_iterations= 8
)

def main():
    question = input("What do you like to ask?\n")
    while "exit" not in question.lower():  
        answer = agent_executor.invoke({"input": question})
        print(answer['output'])  
        question = input("\nDo you have other queries you would like to know about? if not type exit to end the chat.\n")  

if __name__ == "__main__":
    main()