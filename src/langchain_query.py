from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import sys
import os
from dotenv import load_dotenv

load_dotenv(".env")

graph = Neo4jGraph(
    url="bolt://localhost:7687", 
    username="neo4j", 
    password="abcd1234"
)

#enhanced_graph = Neo4jGraph(
#    url="bolt://localhost:7687", 
#    username="neo4j", 
#    password="abcd1234",
#    enhanced_schema=True
#)

#graph.refresh_schema()

#print(enhanced_graph.schema)

llm = ChatGroq(model="llama3-70b-8192", temperature=0)

chain = GraphCypherQAChain.from_llm(
    llm, graph=graph, verbose=True
)

chain.invoke({"query": "What hashtags are related to loans."})