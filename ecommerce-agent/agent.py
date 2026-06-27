
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated
import operator
import os
from dotenv import load_dotenv
from tools import get_order, search_products, get_product, clear_tool_calls

# Load local API keys and environment configurations
load_dotenv()

# The set of tools the agent can request execution for
TOOLS = [get_order, search_products, get_product]

# AgentState is the shared memory that flows through the graph.
# Every node reads from this and writes back to this.
# messages uses operator.add so new messages are appended, not overwritten.
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# Initialize the Gemini model. It will fall back to GOOGLE_API_KEY environment var if needed.
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
# bind_tools tells LangChain which tools Gemini can request
llm_with_tools = llm.bind_tools(TOOLS)

# NODE 1: call_llm
# Sends the current message history to Gemini.
# Gemini either responds with text (done) or requests a tool call (continue looping).
def call_llm(state: AgentState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    # Wrap response in a list because AgentState uses operator.add
    return {"messages": [response]}

# NODE 2: ToolNode (built-in LangGraph node)
# Reads the tool_calls from the last AI message,
# executes the actual Python tool functions,
# and returns results as ToolMessages.
tool_node = ToolNode(TOOLS)

# ROUTING FUNCTION
# After the LLM responds, we check: did it ask for a tool?
# If yes -> go to tools node. If no -> we're done, go to END.
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# BUILD THE GRAPH
# This defines the flow: llm -> check -> tools -> llm -> check -> ...
def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    
    # Register our nodes
    graph.add_node("llm", call_llm)
    graph.add_node("tools", tool_node)
    
    # Always start at the llm node
    graph.set_entry_point("llm")
    
    # After llm responds, route based on should_continue
    graph.add_conditional_edges(
        "llm",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # After tools run, always go back to llm so Gemini can process the tool results
    graph.add_edge("tools", "llm")
    
    return graph.compile()

# The compiled graph - reuse this across calls
agent_graph = build_graph()

# Standard prompt context instructions
SYSTEM_MESSAGE = """You are a helpful customer support assistant 
for an online store. Use the available tools to look up real 
order and product data. Never make up order statuses, prices, 
or product details. Always respond in a warm, friendly tone."""

def run_agent(question: str) -> str:
    """Invokes the compiled LangGraph loop with the user question and returns final output."""
    # Clear any tool logs from the previous execution
    clear_tool_calls()
    
    # Build initial state with system context + user question
    initial_state = {
        "messages": [
            HumanMessage(content=SYSTEM_MESSAGE + "\n\nCustomer: " + question)
        ]
    }
    
    # Run the graph - it loops automatically until END
    final_state = agent_graph.invoke(initial_state)
    
    # Extract response content from the final message
    content = final_state["messages"][-1].content
    
    # If the model output is structured as a list of content blocks (common in Gemini API responses),
    # extract and concatenate the text parts.
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)
        return "\n".join(text_parts)
        
    return str(content)

