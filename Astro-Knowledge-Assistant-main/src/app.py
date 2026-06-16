import streamlit as st
import pandas as pd
import sqlite3
import os
import subprocess
import uuid
from datetime import datetime, UTC
from retriever import retrieve

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SSGI Space Intelligence",
    page_icon="📡",
    layout="wide"
)

# ---------------- DATABASE ----------------
DB_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/database/ssgi_history.db"
)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            chat_id TEXT,
            username TEXT,
            timestamp TEXT,
            prompt TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_history(chat_id, username, prompt, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO history VALUES (?, ?, ?, ?, ?)",
        (
            chat_id,
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prompt,
            response
        )
    )
    conn.commit()
    conn.close()

def get_user_chats(username):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT chat_id, MIN(timestamp) as start_time
        FROM history
        WHERE username=?
        GROUP BY chat_id
        ORDER BY start_time DESC
        """,
        conn,
        params=(username,)
    )
    conn.close()
    return df

def get_chat_messages(chat_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT timestamp, prompt, response
        FROM history
        WHERE chat_id=?
        ORDER BY timestamp ASC
        """,
        conn,
        params=(chat_id,)
    )
    conn.close()
    return df

def delete_chat(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()

# ---------------- SESSION ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

# ---------------- LOGIN ----------------
if not st.session_state.authenticated:
    st.title("📡 SSGI Intelligence Portal")

    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            if user == "ssgi_admin" and pw == "solar_2026":
                st.session_state.authenticated = True
                st.session_state.username = user
                init_db()
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.image("src/ssgilogo.png", width=100)
st.sidebar.title(f"🛰️ {st.session_state.username}")

st.sidebar.markdown("## 📊 Today's Space Intelligence")

# Load live data
noaa_path = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/noaa_indices_cleaned.csv"
)

try:
    live_data = pd.read_csv(noaa_path).tail(1)
    ssn = int(live_data['sunspot_number'].values[0])
    st.sidebar.metric("☀️ Sunspot Number", ssn)
except:
    st.sidebar.metric("☀️ Sunspot Number", "N/A")

st.sidebar.metric("🔥 Solar Flare", "Moderate")
st.sidebar.metric("🌍 Geomagnetic Storm", "Quiet")

st.sidebar.markdown("---")

# New Chat
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.show_history = False  # ensure chat view
    st.rerun()

# Toggle History
if st.sidebar.button("📜 Chat History"):
    st.session_state.show_history = not st.session_state.show_history

# ---------------- MAIN ----------------
st.title("📡 SSGI Space Intelligence System")

# -------- CHAT VIEW --------
if not st.session_state.show_history:

    # Load messages from DB if empty
    if not st.session_state.messages:
        df = get_chat_messages(st.session_state.chat_id)
        for _, row in df.iterrows():
            st.session_state.messages.append({
                "role": "user",
                "content": row["prompt"]
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": row["response"]
            })

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Enter intelligence query..."):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Processing intelligence..."):

            context = retrieve(prompt)

            full_prompt = f"""
            SYSTEM: You are SSGI Intelligence AI.
            Use this data: {context}
            USER: {prompt}
            """

            result = subprocess.run(
                ["ollama", "run", "llama3", full_prompt],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            response = result.stdout

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # Save to DB
        save_history(
            st.session_state.chat_id,
            st.session_state.username,
            prompt,
            response
        )

# -------- HISTORY VIEW --------
else:
    st.header("📜 Your Chats")

    chats = get_user_chats(st.session_state.username)

    if not chats.empty:
        for i, row in chats.iterrows():
            cols = st.columns([0.7, 0.15, 0.15])

            # Open Chat
            with cols[0]:
                if st.button(f"💬 {row['start_time']}", key=f"chat_{i}"):
                    st.session_state.chat_id = row["chat_id"]
                    st.session_state.messages = []
                    st.session_state.show_history = False

            # Delete Chat
            with cols[1]:
                if st.button("🗑️", key=f"delete_{i}"):
                    delete_chat(row["chat_id"])
                    st.rerun()

    else:
        st.info("No chats found.")