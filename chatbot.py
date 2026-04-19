import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="AI Mode Chatbot", page_icon="🤖")

st.title("🤖 AI Mode Chatbot")

# Model
model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

# Mode selection
mode_option = st.selectbox(
    "Choose your AI mode",
    ("Funny mode", "Sad mode", "Angry mode")
)

if mode_option == "Funny mode":
    mode = "You are an Funny assistant.Reply in a funny way."
elif mode_option == "Sad mode":
    mode = "You are an Sad assistant.Reply in a sad way."
else:
    mode = "You are an Angry assistant.Reply in an angry way."

# Reset button
if st.button("Reset Chat"):
    st.session_state.messages = [SystemMessage(content=mode)]
    st.session_state.chat_history = []

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=mode)]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get response
    response = model.invoke(st.session_state.messages)

    # Show bot response
    with st.chat_message("assistant"):
        st.markdown(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})
