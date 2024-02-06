import pandas as pd
import sys 
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain.agents.agent_types import AgentType

load_dotenv()

class ChatHistory:  
    def __init__(self, max_messages=5):  
        self.max_messages = max_messages  
        self.messages = []  
  
    def add_message(self, message):  
        self.messages.append(message)  
        if len(self.messages) > self.max_messages:  
            # Remove the oldest message to maintain the history size  
            self.messages.pop(0)  
  
    def get_history(self):  
        return " ".join(self.messages) 

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
llm = AzureChatOpenAI(deployment_name=os.getenv('Completion_model'), temperature=0)
toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm) 

agent_executor = create_sql_agent(
    llm=llm, 
    toolkit=toolkit, 
    verbose=False, 
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
)

chat_history = ChatHistory(max_messages=10)  # Set the number of past messages to include  

def main():
    question = input("What do you like to ask?\n")
    while "exit" not in question.lower(): 
        # Prepend chat history to the question  
        question_with_history = chat_history.get_history() + question  
        answer = agent_executor.run(question_with_history)  
        print(answer)  
    
        # Update chat history with the latest exchange  
        chat_history.add_message(f"Q: {question} A: {answer}")  
    
        question = input("Do you have other queries you would like to know about?\n")  

if __name__ == "__main__":
    main()
