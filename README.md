# AOAI-Langchain-SQL

# Table of contents:
- [Step 1 - Installing the Requirements and Gettings Things Ready]


## Step 1 - Installing the Requirements and Gettings Things Ready

1. Initally, we would need to install the necessary python libraries for Azure OpenAI, dotenv, langchain, panadas, and sqlalchemy. 
Run the following command to install all required libraries: 
```
pip install -r requirements.text
```
2. You need to create .env file that will contain all the information related to your Azure OpenAI models.  
You can get the information related to the SQL database from the connection string tab for the SQL database on Azure portal as shown below:
![Sql_information](Images/SQL_Info.png).
From the above image you can find a link to download the necceary driver for the ODBC servce. This driver will allow you to connect to the Azure SQL database. 
Be sure to download the **ODBC Driver 18** 

4. Fill out your .env details as shown below:  
![Environment Variables](Images/EnvVariables.png)

## Step 2 - ChatHistory Class: 
I have created a class to keep track of the chat hisotry where we can define how many past messages to be included in context when querying the database. 
In the add_message function we can see how the ChatHistory will remove the earliest message when exceeding the max_messages to be included in the conversation. 
``` python
class ChatHistory:  
    def __init__(self, max_messages=5):  
        self.max_messages = max_messages  
        self.messages = []  
  
    def add_message(self, message):  
        self.messages.append(message)  
        if len(self.messages) > self.max_messages:  
            # Remove the oldest message to maintain the history size  
            self.messages.pop(1)  
  
    def get_history(self):  
        return " ".join(self.messages)
```
When creating a copy of the class we can define the maximum number of messages to include by using the max_messages parameter.


## Step 3 - SQLLoader Class: 
This class will be used to create table, insert data, and load data from the SQL database. 
1. The create_engine() is the first function in the class that is used to create the connection to the Azure SQL database as shown belwo: 
``` python
def create_engine(self):  
        username = os.getenv('SQL_USERNAME')  
        password = os.getenv('SQL_PASSWORD')  
        server = f"tcp:{os.getenv('SQL_ENDPOINT')}"
        database = os.getenv('SQL_DATABASE')  
        driver = "ODBC Driver 18 for SQL Server"  
        connection_string = f"mssql+pyodbc:///?odbc_connect=DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"  
        engine = create_engine(connection_string)  
        return engine
```

2. The create_table(), insert data() functions will be used to get the data from the loaded csv file and inserting the csv file contents in the database. User can define the name of the created table.
``` python
    def create_table(self, table_name):  
        # Use SQLAlchemy to generate the table schema from the dataframe  
        self.df.to_sql(table_name, self.engine, if_exists='replace', index=False)  
        print(f"Table {table_name} has been created in the database.")
      
    def insert_data(self, table_name):  
        # Use pandas to_sql method for inserting the data  
        self.df.to_sql(table_name, self.engine, if_exists='append', index=False)  
        print(f"Data has been inserted into {table_name} table.")
```
3. The read_db() function will be used to return an SQLDatabase from the engine connection so that it can be used as an sql database in the sql_agent:
``` python
def read_db(self):
        return SQLDatabase(self.engine)
``` 

## Step 4 - Main function: 



