from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition 

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os
import sqlite3
import requests

#***************************Tools**********************************************************************

search_tool = DuckDuckGoSearchRun()

@tool
def get_stock_price(symbol:str) -> dict:
    """ 
    Fetch latest stock price for give symbol (eg: AAPL, TSLA)
    using Alpha Vantage url and api key
    """
    api_key = os.environ.get("Alpha_vantage_api_key")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

tools = [search_tool, get_stock_price]

#***************************************************************************************************8

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
llm_with_tools = llm.bind_tools(tools)

#*********************************************************************************************************

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

#******************************************************************************************************

# Checkpointer
conn = sqlite3.connect(database="chat_db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge ("tools", "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=checkpointer)

def retreive_all_threads():
    all_threads = set()
    for threads in checkpointer.list(None):
        all_threads.add(threads.config['configurable']['thread_id'])
    return list(all_threads)