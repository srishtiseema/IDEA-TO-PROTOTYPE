
import streamlit as st
from groq import Groq
import json
import base64
import os

# ==========================
# GROQ API
# ==========================

client = Groq(api_key="secret id")

# ==========================
# USER DATABASE
# ==========================

def load_users():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f)

users = load_users()

# ==========================
# BACKGROUND IMAGE FUNCTION
# ==========================

def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img = get_base64_image("background.jpg")

# ==========================
# ADVANCED GALAXY BACKGROUND
# ==========================

st.markdown(
f"""
<style>

/* MAIN BACKGROUND */

[data-testid="stAppViewContainer"] {{
background: radial-gradient(circle at top, #0f2027, #203a43, #000000);
background-size: cover;
background-attachment: fixed;
overflow:hidden;
}}

[data-testid="stHeader"] {{
background: transparent;
}}

/* HERO TEXT */

.hero-title {{
font-size:70px;
font-weight:800;
text-align:center;
color:white;
letter-spacing:2px;
}}

.hero-sub {{
font-size:22px;
text-align:center;
color:#cfd9ff;
}}

/* GLASSMORPHISM CARDS */

.card {{
padding:25px;
border-radius:20px;
background:rgba(255,255,255,0.08);
backdrop-filter: blur(15px);
margin:10px;
box-shadow:0 10px 40px rgba(0,0,0,0.6);
text-align:center;
border:1px solid rgba(255,255,255,0.15);
color:white;
transition:0.3s;
}}

.card:hover {{
transform: translateY(-8px);
box-shadow:0 20px 50px rgba(0,0,0,0.8);
}}

/* STAR LAYER */

.stars {{
position: fixed;
top:0;
left:0;
width:100%;
height:100%;
background: transparent;
z-index:-1;
}}

.stars:after {{
content:" ";
position:absolute;
top:0;
left:0;
width:2px;
height:2px;
background:white;
box-shadow:
100px 200px white,
300px 100px white,
500px 400px white,
700px 150px white,
900px 300px white,
200px 600px white,
600px 500px white,
800px 700px white,
1000px 200px white,
1200px 400px white,
1400px 300px white,
1600px 600px white,
1800px 200px white,
1500px 500px white,
400px 700px white,
900px 800px white,
600px 200px white;
animation: animStar 120s linear infinite;
}}

@keyframes animStar {{
from {{transform: translateY(0px);}}
to {{transform: translateY(-2000px);}}
}}

/* BUTTON STYLE */

button[kind="secondary"] {{
background: linear-gradient(45deg,#6a11cb,#2575fc);
color:white;
border:none;
border-radius:30px;
padding:10px 20px;
font-weight:600;
}}

button[kind="secondary"]:hover {{
background: linear-gradient(45deg,#2575fc,#6a11cb);
}}

</style>

<div class="stars"></div>

""",
unsafe_allow_html=True
)

# ==========================
# SESSION STATE
# ==========================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================
# HOME PAGE
# ==========================

if st.session_state.page == "home":

    st.markdown('<div class="hero-title">🚀 Nova AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Build your startup idea using AI</div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("✨ Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        💡 <h3>Idea Generator</h3>
        Turn simple thoughts into powerful startup ideas.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        🤖 <h3>AI Builder</h3>
        Generate product plans and development strategy.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        🚀 <h3>Launch Faster</h3>
        Build MVPs and prototypes instantly.
        </div>
        """, unsafe_allow_html=True)

# ==========================
# LOGIN PAGE
# ==========================

elif st.session_state.page == "login":

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username] == password:

            st.session_state.logged_in = True
            st.session_state.page = "nova"
            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Invalid credentials")

# ==========================
# SIGNUP PAGE
# ==========================

elif st.session_state.page == "signup":

    st.title("Create Account")

    username = st.text_input("Choose Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Create Account"):

        if username in users:
            st.error("User already exists")

        else:

            users[username] = password
            save_users(users)

            st.success("Account created successfully!")
            st.session_state.page = "login"
            st.rerun()

# ==========================
# NOVA AI CHAT
# ==========================

elif st.session_state.page == "nova":

    st.title("Nova AI Startup Builder")

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Describe your startup idea...")

    if prompt:

        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append(
            {"role":"user","content":prompt}
        )

        system_prompt = """
You are Nova, an AI startup mentor.

Generate:
- Startup name
- Product description
- Key features
- Pitch deck outline
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":system_prompt},
                *st.session_state.messages
            ]
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append(
            {"role":"assistant","content":reply}
        )

