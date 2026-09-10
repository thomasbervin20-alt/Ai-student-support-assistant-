import streamlit as st
import uuid
from agent import create_agent

# Initialize page configuration
st.set_page_config(page_title="AI Student Support", page_icon="🎓")
st.title("🎓 AI Student Support Assistant")

# Initialize session state for LangGraph memory Thread ID
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Initialize session state for Streamlit UI message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Student Support Assistant. How can I help you today?"}
    ]

# Sidebar for session management
with st.sidebar:
    st.header("Session Management")
    st.write(f"**Current Session ID:**\n`{st.session_state.thread_id}`")
    
    # Button to generate a new thread ID (clears memory for a fresh start)
    if st.button("Start New Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Student Support Assistant. How can I help you today?"}
        ]
        st.rerun()

# Render previous chat messages from Streamlit session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capture user input
if prompt := st.chat_input("Ask a question about the university..."):
    # 1. Display user message in the UI instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Save user message to Streamlit UI history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Process the AI response
    with st.spinner("Thinking..."):
        try:
            # Initialize agent
            agent = create_agent(st.session_state.thread_id)
            
            # Pass ONLY the new prompt to LangGraph.
            # LangGraph handles the history automatically via its SQLite checkpointer.
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            response = agent.invoke(
                {"messages": [("user", prompt)]}, 
                config=config
            )
            
            # Extract the AI's final response content
            ai_response = response["messages"][-1].content
            
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"
    
    # 4. Display AI response in the UI
    with st.chat_message("assistant"):
        st.markdown(ai_response)
        
    # 5. Save AI response to Streamlit UI history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
