import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="💬",
    layout="wide"
)

# =========================
# 🎨 MODERN LIGHT THEME
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #eef6ff, #f8fbff);
    color: #1e293b;
}

/* Header */
header[data-testid="stHeader"] {
    background: white !important;
    border-bottom: 1px solid #e2e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f1f5f9;
    border-right: 1px solid #e2e8f0;
}

/* Sidebar title */
.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Sidebar cards */
.info-card {
    background: white;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
    border: 1px solid #e2e8f0;
    font-size: 14px;
}

/* Hero section */
.hero {
    text-align: center;
    padding: 20px;
    background: white;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
}

/* Quick buttons */
.stButton > button {
    border-radius: 20px;
    padding: 6px 16px;
    border: 1px solid #cbd5f5;
    background: white;
    color: #1e293b;
}

.stButton > button:hover {
    background: #3b82f6;
    color: white;
}

/* Chat bubbles */
.user-bubble {
    background: #3b82f6;
    color: white;
    padding: 12px;
    border-radius: 14px;
    margin: 8px 0;
    max-width: 70%;
    margin-left: auto;
}

.bot-bubble {
    background: #e2e8f0;
    color: #1e293b;
    padding: 12px;
    border-radius: 14px;
    margin: 8px 0;
    max-width: 70%;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
    border-radius: 14px !important;
    border: 1px solid #cbd5f5 !important;
}

div[data-testid="stChatInput"] button {
    background: #3b82f6 !important;
    color: white !important;
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 🔁 STATE INIT
# =========================
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
                "content": "Hi! I’m the AutoStream AI Agent. I can help you with pricing, features, refunds, and sign-up."
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
            "content": "Hi! I’m the AutoStream AI Agent. I can help you with pricing, features, refunds, and sign-up."
        }
    ]


initialize_state()


# =========================
# 📊 SIDEBAR
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Session Info</div>', unsafe_allow_html=True)

    def box(label, value):
        st.markdown(f"""
        <div class="info-card">
            <b>{label}:</b><br>{value}
        </div>
        """, unsafe_allow_html=True)

    state = st.session_state.agent_state

    box("Intent", state.get("intent") or "Not detected")
    box("Name", state.get("name") or "Not provided")
    box("Email", state.get("email") or "Not provided")
    box("Platform", state.get("platform") or "Not provided")
    box("Lead Stage", state.get("lead_stage") or "Not started")
    box("Lead", "Captured ✅" if state.get("lead_captured") else "Not yet")

    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()


# =========================
# 🧠 HERO HEADER (CENTERED)
# =========================
st.markdown("""
<div class="hero">
    <h1>AutoStream AI Agent</h1>
    <p style="color:#64748b;">
        Conversational AI for product queries and lead capture
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# ⚡ QUICK ACTIONS
# =========================
st.markdown("### Quick Actions")

col1, col2, col3, col4 = st.columns(4)

if col1.button("Pricing"):
    st.session_state.chat_history.append({"role": "user", "content": "pricing"})
if col2.button("Features"):
    st.session_state.chat_history.append({"role": "user", "content": "features"})
if col3.button("Refund"):
    st.session_state.chat_history.append({"role": "user", "content": "refund"})
if col4.button("Start"):
    st.session_state.chat_history.append({"role": "user", "content": "start"})


# =========================
# 💬 CHAT DISPLAY
# =========================
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)


# =========================
# 🧾 INPUT
# =========================
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = process_message(st.session_state.agent_state, user_input)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.rerun()


# =========================
# 🔽 AUTO SCROLL
# =========================
st.markdown(
    """
    <script>
        const scrollToBottom = () => {
            const parent = window.parent.document;
            const chatContainer = parent.querySelector('[data-testid="stChatInput"]');
            if (chatContainer) {
                chatContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        };
        setTimeout(scrollToBottom, 200);
    </script>
    """,
    unsafe_allow_html=True
)