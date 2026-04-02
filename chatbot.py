import streamlit as st
from groq import Groq
import json
import os
import hashlib

API_KEY = "your_actual_api_key_here"
client = Groq(api_key=API_KEY)
USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user(email, password):
    users = load_users()
    users[email] = hash_password(password)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def verify_user(email, password):
    users = load_users()
    if email in users:
        return users[email] == hash_password(password)
    return False

def user_exists(email):
    users = load_users()
    return email in users

st.set_page_config(
    page_title="ToolsAI - ML Study Helper",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0533 25%, #0d1b4b 50%, #0a2444 75%, #0a0a0f 100%) !important;
        color: #ffffff;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem !important;}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12012a 0%, #0d1b4b 100%) !important;
        border-right: 1px solid rgba(168,85,247,0.3) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(168,85,247,0.1) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(168,85,247,0.2) !important;
        text-align: left !important;
        width: 100% !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        font-size: 13px !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(168,85,247,0.3) !important;
        border-color: #a855f7 !important;
        color: #ffffff !important;
    }
    .stChatInput input {
        background: rgba(255,255,255,0.9) !important;
        color: #1a1a2e !important;
        border-radius: 16px !important;
        border: 1px solid rgba(168,85,247,0.4) !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] ol,
    [data-testid="stChatMessage"] ul { color: #f0e6ff !important; }
    h1, h2, h3 { color: #ffffff !important; }
    .stTextInput input {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border-radius: 10px !important;
        border: 1px solid rgba(168,85,247,0.4) !important;
        font-size: 15px !important;
    }
    .stTextInput label { color: #e2e8f0 !important; }
    .stButton button {
        background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #6d28d9, #2563eb) !important;
        box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
    }
    .logo-text {
        font-size: 56px;
        font-weight: 900;
        background: linear-gradient(90deg, #a855f7, #3b82f6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 3px;
    }
    .logo-sub {
        color: #94a3b8;
        font-size: 15px;
        text-align: center;
        margin-top: 8px;
        letter-spacing: 1px;
    }
    .center-logo {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    .top-bar {
        position: fixed;
        top: 0;
        right: 0;
        padding: 10px 24px;
        display: flex;
        align-items: center;
        gap: 8px;
        z-index: 999;
        background: rgba(10,10,15,0.8);
        backdrop-filter: blur(10px);
        border-bottom-left-radius: 12px;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def show_login():
    st.markdown("""
    <div class='center-logo'>
        <div class='logo-text'>🤖 ToolsAI</div>
        <div class='logo-sub'>✨ Your Personal AI & Machine Learning Study Helper</div>
        <br>
        <div style='display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:24px;'>
            <span style='background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.4); color:#c084fc; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🧠 Machine Learning</span>
            <span style='background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.4); color:#60a5fa; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🤖 Deep Learning</span>
            <span style='background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); color:#34d399; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600;'>💬 NLP & LLMs</span>
            <span style='background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.4); color:#fbbf24; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600;'>🐍 Python & Data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffffff;'>👋 Welcome back</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:14px;'>Sign in to continue learning AI & ML</p>", unsafe_allow_html=True)
            login_email = st.text_input("📧 Email", placeholder="you@example.com", key="login_email")
            login_password = st.text_input("🔒 Password", type="password", placeholder="Your password", key="login_pass")
            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                if not login_email or not login_password:
                    st.error("❌ Please fill in all fields!")
                elif not user_exists(login_email):
                    st.error("❌ Email not found! Please sign up first.")
                elif verify_user(login_email, login_password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = login_email
                    st.session_state.messages = []
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Wrong password! Try again.")
            st.markdown("<p style='color:#555; font-size:12px; text-align:center; margin-top:12px;'>Don't have an account? Click Sign Up above!</p>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffffff;'>🚀 Create Account</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:14px;'>Join ToolsAI and start learning!</p>", unsafe_allow_html=True)
            signup_name = st.text_input("👤 Full Name", placeholder="Nithin Raj Kumar", key="signup_name")
            signup_email = st.text_input("📧 Email", placeholder="you@example.com", key="signup_email")
            signup_password = st.text_input("🔒 Password", type="password", placeholder="Min 6 characters", key="signup_pass")
            signup_confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat password", key="signup_confirm")
            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                if not signup_name or not signup_email or not signup_password or not signup_confirm:
                    st.error("❌ Please fill in all fields!")
                elif len(signup_password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                elif signup_password != signup_confirm:
                    st.error("❌ Passwords do not match!")
                elif user_exists(signup_email):
                    st.error("❌ Email already registered! Please sign in.")
                elif "@" not in signup_email:
                    st.error("❌ Please enter a valid email!")
                else:
                    save_user(signup_email, signup_password)
                    st.success(f"✅ Account created! Welcome {signup_name}! Now sign in.")
                    st.balloons()

def show_chat():
    with st.sidebar:
        st.markdown("""
        <div style='display:flex; align-items:center; gap:10px; padding:8px 0 16px;'>
            <div style='font-size:28px;'>🤖</div>
            <div style='font-size:20px; font-weight:800; background:linear-gradient(90deg,#a855f7,#3b82f6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>ToolsAI</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='color:#94a3b8; font-size:12px; margin-bottom:12px;'>👤 {st.session_state.user_email}</p>", unsafe_allow_html=True)
        if st.button("➕  New chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.markdown("<p style='color:#94a3b8; font-size:12px; font-weight:600; letter-spacing:1px;'>RECENT CHATS</p>", unsafe_allow_html=True)
        if len(st.session_state.messages) == 0:
            st.markdown("<p style='color:#555; font-size:12px;'>No chats yet. Start asking!</p>", unsafe_allow_html=True)
        else:
            user_messages = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
            for msg in reversed(user_messages[-6:]):
                short = msg[:30] + "..." if len(msg) > 30 else msg
                st.markdown(f"""
                <div style='background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.15); border-radius:8px; padding:8px 12px; margin-bottom:6px; color:#c084fc; font-size:12px;'>
                    💬 {short}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("❓  Help", use_container_width=True):
            st.info("Ask me anything about AI/ML!")
        st.markdown("---")
        if st.button("🚪  Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.messages = []
            st.rerun()
        st.markdown("<p style='color:#444; font-size:11px; margin-top:16px;'>Powered by Groq + Llama 3<br>Built by Nithin Raj Kumar</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class='top-bar'>
        <span style='font-size:20px;'>🤖</span>
        <span style='font-size:16px; font-weight:800; background:linear-gradient(90deg,#a855f7,#3b82f6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>ToolsAI</span>
    </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class='center-logo'>
            <div style='font-size:80px;'>🤖</div>
            <div class='logo-text'>ToolsAI</div>
            <div class='logo-sub'>Your Personal AI & Machine Learning Study Helper</div>
            <br>
            <div style='display:flex; gap:16px; justify-content:center; flex-wrap:wrap;'>
                <div style='background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.3); padding:16px 24px; border-radius:12px; color:#c084fc; font-size:14px;'>🌲 Machine Learning</div>
                <div style='background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); padding:16px 24px; border-radius:12px; color:#60a5fa; font-size:14px;'>🧠 Deep Learning</div>
                <div style='background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); padding:16px 24px; border-radius:12px; color:#34d399; font-size:14px;'>💬 NLP & LLMs</div>
                <div style='background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); padding:16px 24px; border-radius:12px; color:#fbbf24; font-size:14px;'>🐍 Python & Data</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about AI/ML..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner(""):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert AI and ML tutor named ToolsAI. Answer questions about ML, Deep Learning, NLP, Python and Data Science clearly with simple examples."},
                        *st.session_state.messages
                    ]
                )
                answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.logged_in:
    show_chat()
else:
    show_login()