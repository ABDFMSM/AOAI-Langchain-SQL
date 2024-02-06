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
The create_table, insert data will be used to get the data from the loaded csv file and inserting the csv file contents in the database. User can define the name of the created table. 

## Step 4 - Main function: 



