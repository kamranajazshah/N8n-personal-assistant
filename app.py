import streamlit as st
import requests

# Title
st.title("🤝 Your Personal Assistant")

# Subheader
st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics.
2. Arrange Calendar events and meetings.
3. Read your emails and send replies, can even summarize them for you.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

st.subheader("💬 Chat with your assistant")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_message = st.chat_input()

# When user sends a message
if user_message:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Send message to n8n webhook
    response = requests.post(
        "http://localhost:5678/webhook/28ee0993-cefd-4eb6-a368-eb888d96bb70",
        json={"message": user_message}
    )

    # Convert response to JSON
    data = response.json()

    # n8n usually returns a list
    if isinstance(data, list):
        ai_response = data[0].get("output", "No response from assistant")
    else:
        ai_response = data.get("output", "No response from assistant")

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })