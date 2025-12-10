from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

llm = ChatGroq(model='llama-3.1-8b-instant')


# Prompt Template
system_template='Translate the following into {language}:'
prompt=ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

parser=StrOutputParser()

# Chain
chain=prompt|llm|parser

######################################

# App Definition
app=FastAPI(
    title='Langchain Server',
    version='1.0.0',
    description='A simple language translation API'
)

# Chain Routes
add_routes(
    app,
    chain,
    path='/chain'
)


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)

    # Run Server: python serve.py
    # Serve at: 127.0.0.1/8000/docs