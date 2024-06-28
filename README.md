# MetaCrawler
![MetaCrawler Cover](metacrawler_cover.jpeg)

## Introduction

MetaCrawler is designed to crawl over file systems and networks to create semantic meta tags, enabling agents to navigate and structure our growing collection of files. This project focuses on document classification and relevance, leveraging AI to handle the otherwise impossible task of organizing vast amounts of data. Our current prototype not only summarises documents but also generates hashtags to enrich semantic search capabilities. 

The ultimate goal is to add more meta tags, functioning as a type of a Search Engine Optimisation for future AI agents to retrieve accurate information. 




## Installation
### Neo4j
1. Download the latest version of [Neo4j](https://neo4j.com/download/).
2. Create a new database called "MetaCrawler" 
```
uri = "bolt://localhost:7687"
username = "neo4j"
password = "abcd1234"
```
3. Install APOC Plugin for Neo4j
### Azure AI Document Intelligence
1. Create a new resource in the [Azure Portal](https://portal.azure.com/).
2. Search for "Azure AI Document Intelligence" and create a new resource.
3. Instructions: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/create-document-intelligence-resource?view=doc-intel-4.0.0

### Poetry 
```angular2html
pip install poetry@1.8.2
```

```bash
# Fix the lock file (optionally fix)
poetry lock --no-update
```
```bash
# Install all the py packages via poetry
poetry install
```
If you are not inside a virtual env i.e.
```bash
poetry shell
```
### Final Steps
Copy the `.env.example` and relabel it to `.env`.
To speed through and get something working, use the following settings instead.

<u>Project Directory needs to be updated with full path</u>
```env
LANGCHAIN_TRACING_V2="false"
LANGCHAIN_API_KEY="" # Not needed 
LANGCHAIN_TRACING_V2 = "false"
LANGCHAIN_PROJECT = "MetaCrawler"
OPENAI_API_KEY = "<REQUIRED>" 
PROJECT_DIRECTORY = "MetaCrawler/metacrawler"
AZURE_DOC_KEY="<REQUIRED>"
TEST="True"
```
Amend "root_directory" to the full path of the directory you wish to crawl.

main.py
```
root_dir='.../MetaCrawler/tests/Test_Drive'
```
### Start MetaCrawler
Run this on the root directory (so at /MetaCrawler directory)
```bash
poetry run py metacrawler/main.py
```
![MetaCrawler](MetaCrawler.jpeg)