import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🤖",
    layout="centered"
)


def initialize_state():
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = {
            "messages": [],
            "intent": "",
            "name": "",
            "email": "",
            "platform": "",
            "lead_captured": False,
            "lead_stage": ""
        }

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I’m the AutoStream AI Agent. "
                    "I can help you with pricing, features, refunds, and sign-up."
                )
            }
        ]


def reset_chat():
    st.session_state.agent_state = {
        "messages": [],
        "intent": "",
        "name": "",
        "email": "",
        "platform": "",
        "lead_captured": False,
        "lead_stage": ""
    }
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hi! I’m the AutoStream AI Agent. "
                "I can help you with pricing, features, refunds, and sign-up."
            )
        }
    ]


initialize_state()

st.title("🤖 AutoStream AI Agent")
st.caption("Conversational AI for product queries, lead qualification, and lead capture.")

with st.sidebar:
    st.header("Session Info")

    st.write("**Current Intent:**", st.session_state.agent_state.get("intent", "") or "Not detected yet")
    st.write("**Name:**", st.session_state.agent_state.get("name", "") or "Not provided")
    st.write("**Email:**", st.session_state.agent_state.get("email", "") or "Not provided")
    st.write("**Platform:**", st.session_state.agent_state.get("platform", "") or "Not provided")
    st.write("**Lead Stage:**", st.session_state.agent_state.get("lead_stage", "") or "Not started")
    st.write(
        "**Lead Captured:**",
        "Yes ✅" if st.session_state.agent_state.get("lead_captured", False) else "No ❌"
    )

    st.divider()

    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = process_message(st.session_state.agent_state, user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

        if st.session_state.agent_state.get("lead_captured", False):
            st.success("Lead captured successfully.")

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_message})

        with st.chat_message("assistant"):
            st.error(error_message)