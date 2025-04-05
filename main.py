import streamlit as st
from backen import generateResponse

st.set_page_config(layout="wide", page_title="ChatBot", page_icon="💬")

# ======= Custom CSS =======
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
        min-height: 100vh;
        position: relative;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        flex-direction: column;
    }

    .main {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding-bottom: 120px;
        position: relative;
    }

    .chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 1rem 2rem;
        position: relative;
        scroll-behavior: smooth;
        height: calc(100vh - 200px);
    }

    .chat-bubble {
        padding: 1rem 1.5rem;
        border-radius: 1.2rem;
        margin: 0.8rem 0;
        max-width: 85%;
        background-color: #1e1e1e;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-in-out;
    }

    .user-bubble {
        background: linear-gradient(135deg, #4caf50, #45a049);
        margin-left: auto;
        border-bottom-right-radius: 0.3rem;
    }

    .bot-bubble {
        background: linear-gradient(135deg, #333333, #2d2d2d);
        margin-right: auto;
        border-bottom-left-radius: 0.3rem;
    }

    .chatgpt-input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1e1e1e;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        box-shadow: 0 -2px 15px rgba(0,0,0,0.2);
    }

    .input-container {
        max-width: 800px;
        width: 100%;
        display: flex;
        align-items: center;
        background-color: #2d2d2d;
        border-radius: 15px;
        padding: 8px 16px;
        position: relative;
    }

    .stTextInput > div > input {
        background: transparent;
        border: none;
        color: white;
        font-size: 16px;
        padding: 12px 8px;
        width: 100%;
        min-height: 40px;
        outline: none;
        resize: none;
        line-height: 1.5;
    }

    .stTextInput > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }

    .stButton > button {
        background: linear-gradient(135deg, #4caf50, #45a049);
        border: none;
        color: white;
        padding: 8px 12px;
        margin-left: 10px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 16px;
        min-width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049, #3d8b40);
    }

    .stButton > button:disabled {
        background: #666;
        cursor: not-allowed;
        box-shadow: none;
    }

    .reset-button-container {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
        z-index: 1000;
    }

    .reset-button {
        background: linear-gradient(135deg, #ff4b4b, #ff3333);
        color: white;
        padding: 0.8rem 1.5rem;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(255, 75, 75, 0.3);
        opacity: 1;
        transition: none;
    }

    .reset-button:hover {
        opacity: 1;
        background: linear-gradient(135deg, #ff4b4b, #ff3333);
    }

    /* Hide scrollbar for Chrome, Safari and Opera */
    .chat-container::-webkit-scrollbar {
        display: none;
    }
    
    /* Hide scrollbar for IE, Edge and Firefox */
    .chat-container {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Title styling */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #4caf50, #45a049);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(76, 175, 80, 0.2);
    }

    /* Loading spinner styling */
    .stSpinner > div {
        border-top-color: #4caf50 !important;
    }

    /* Character count indicator */
    .char-count {
        position: absolute;
        right: 60px;
        bottom: 8px;
        font-size: 12px;
        color: rgba(255, 255, 255, 0.5);
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# ======= Session State =======
if "history" not in st.session_state:
    st.session_state.history = []

# ======= Title =======
st.markdown("<h1 style='text-align: center;'>🤖 Interactive ChatBot</h1>", unsafe_allow_html=True)

# ======= Chat Display =======
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
for user_msg, bot_msg in st.session_state.history:
    st.markdown(f'<div class="chat-bubble user-bubble">{user_msg}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble bot-bubble">{bot_msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ======= Scroll to Bottom =======
st.markdown("""
<script>
var chatContainer = document.getElementById('chat-container');
if (chatContainer) {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
</script>
""", unsafe_allow_html=True)

# ======= Input Bar =======
st.markdown('<div class="chatgpt-input-bar">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([9, 1])

with col1:
    user_input = st.text_input(
        "",
        placeholder="Type your message... (Press Enter to send)",
        label_visibility="collapsed",
        key="user_input"
    )
    # Add character count
    if user_input:
        st.markdown(f'<div class="char-count">{len(user_input)} characters</div>', unsafe_allow_html=True)

with col2:
    send_clicked = st.button("➤", key="send_btn", disabled=not user_input.strip())

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ======= JS for Enter Key to Trigger Button =======
st.markdown("""
<script>
const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
input.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const btn = window.parent.document.querySelector('button[kind="secondary"]');
        if (btn && !btn.disabled) btn.click();
    }
});
</script>
""", unsafe_allow_html=True)

# ======= Handle Send =======
if send_clicked and user_input.strip():
    with st.spinner("SMW is typing..."):
        try:
            response_text = generateResponse(user_input.strip())
        except Exception as e:
            response_text = f"⚠️ Error generating response: {e}"
    st.session_state.history.append((user_input.strip(), response_text))
    st.rerun()  # Clears input on rerun

# ======= Reset Button =======
st.markdown('<div class="reset-button-container">', unsafe_allow_html=True)
if st.button("🔄 Reset Chat", key="reset_button", help="Clear all messages"):
    st.session_state.history = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
