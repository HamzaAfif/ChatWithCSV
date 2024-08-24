import os
import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("file.csv")

print(df.columns.tolist())

engine = create_engine("sqlite:///vulnerabilities.db")
df.to_sql("vulnerabilities", engine, index=False, if_exists='replace')

db = SQLDatabase(engine=engine)   

#print(db.dialect)


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

template = """
You are a cybersecurity expert writing an article about vulnerabilities to your client. Use the data from the table 'vulnerabilities' to provide detailed information in response to the question.

Provide a detailed description of each vulnerability, with clear and informative descriptions.

Question: {question}

Write a detailed and informative article based on the data provided.
"""


userQuestion = input("Please enter your question: ")


prompt = template.format(question=userQuestion)


agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)


response = agent_executor.invoke(prompt)

response_content = response['output'].strip()
print(response_content)

output_file_path = 'response.txt'
with open(output_file_path, 'w') as file:
    file.write(response_content)

print(f"The response has been written to {output_file_path}")