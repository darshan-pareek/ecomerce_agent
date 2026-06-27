import streamlit as st
import os
from dotenv import load_dotenv

# Load environment configs
load_dotenv()

st.title("🛍️ Store Assistant")
st.caption("Ask me about your orders or find products")

# Stop rendering if the api key is missing
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY not set. Please add it to your .env file.")
    st.stop()

from agent import run_agent

# Show example questions as clickable buttons to help user get started
st.markdown("**Try asking:**")
examples = [
    "Where is my order ORD-1002?",
    "Do you have cheaper shoes?",
    "Tell me about your laptops"
]

# Set session state if user clicks any example button
for example in examples:
    if st.button(example):
        st.session_state["question"] = example

# Text input matches session state question value if set
question = st.text_input(
    "Your question:", 
    value=st.session_state.get("question", "")
)

from tools import get_tool_calls

# Submit button triggers graph compilation and execution
if st.button("Ask") and question.strip():
    with st.spinner("Looking that up for you..."):
        response = run_agent(question)
        
    # Retrieve and show any tools that were executed during the request
    tool_calls = get_tool_calls()
    if tool_calls:
        st.markdown("### 🛠️ Tool Executions")
        for idx, call in enumerate(tool_calls, 1):
            with st.expander(f"Tool {idx}: `{call['name']}`", expanded=True):
                st.write(f"**Arguments:** `{call['args']}`")
                st.write("**Returned Result:**")
                st.json(call["result"])
                
    st.markdown("### 💬 Response")
    st.success(response)

