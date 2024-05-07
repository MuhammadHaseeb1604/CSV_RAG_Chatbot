import streamlit as st
from engine.dataloader import load_data
from engine.llm import init_llm
from engine.query_pipeline import get_query_pipeline

st.set_page_config(page_title="Chat with CSV", page_icon=":robot:")

init_llm()

df = load_data(path="./data/prosperLoanData.csv")

qp = get_query_pipeline(df)

st.title("Ask about Prosper Data")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = qp.run(query_str=str(prompt))

    response = response.message.content
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})