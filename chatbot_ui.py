import streamlit as st
import re
from database import (
    signup_user, login_user, save_message, get_chat_dates,
    get_history_by_date, delete_history, close_connection
)

st.set_page_config(page_title="Smart Chatbot", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #8a2be2 !important;
            color: white !important;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        input[type="text"], input[type="email"], input[type="password"], textarea {
            background-color: #d4edda !important;
            color: black !important;
            border-radius: 8px !important;
            padding: 10px !important;
            border: 2px solid #28a745 !important;
        }

        div.stButton > button {
            background-color: #007bff !important;
            color: white !important;
            font-size: 16px !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }

        input[type="password"] + div svg {
            color: white !important;
            stroke: white !important;
            fill: white !important;
        }
    </style>
""", unsafe_allow_html=True)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# --- SIDEBAR AUTH + HISTORY ---
with st.sidebar:
    st.title("User Auth")

    if "user_email" in st.session_state:
        st.subheader(f"Welcome, {st.session_state.user_email}")

        if st.button("Logout"):
            del st.session_state.user_email
            st.success("Logged out.")
            st.rerun()

    else:
        auth_option = st.radio("Choose", ["Login", "Sign Up"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if auth_option == "Sign Up":
            if st.button("Create Account"):
                if not email or not password:
                    st.warning("Please enter email and password.")
                elif not is_valid_email(email):
                    st.warning("Enter a valid email address.")
                elif signup_user(email, password):
                    st.success("Account created! Please log in.")
                else:
                    st.error("User already exists.")
        else:
            if st.button("Login"):
                if login_user(email, password):
                    st.session_state.user_email = email
                    st.success(f"Logged in as {email}")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    if "user_email" in st.session_state:
        st.subheader("📅 Chat History")
        dates = get_chat_dates(st.session_state.user_email)
        if dates:
            selected_date = st.selectbox("Select Date", dates, key="date_selector")
            if st.button("View History"):
                st.session_state.viewing_history = True
                st.session_state.selected_date = selected_date
                st.rerun()
        else:
            st.info("No chat history available.")

        if st.button("Chatbox"):
            st.session_state.viewing_history = False
            st.rerun()

        if st.button("Delete History"):
            delete_history(st.session_state.user_email)
            st.success("Chat history deleted.")
            st.rerun()

# --- MAIN CHAT UI ---
if "user_email" in st.session_state:
    user_email = st.session_state.user_email
    st.title("🤖 Smart Chatbot Assistant")

    if "chat_stage" not in st.session_state:
        st.session_state.chat_stage = "start"
    if "user_choice" not in st.session_state:
        st.session_state.user_choice = None

    if st.session_state.get("viewing_history", False):
        st.subheader(f"Chat from {st.session_state.selected_date}")
        chat_history = get_history_by_date(user_email, st.session_state.selected_date)
        for role, message, timestamp in chat_history:
            time = timestamp.split(" ")[1][:5]
            st.write(f"**{role} ({time})**: {message}")
    else:
        st.write("🤖 How can I assist you today?")
        options = [
            "Smart home app crashes with older thermostat.",
            "Project data not syncing between devices.",
            "App says 'no internet', but Wi-Fi works.",
            "API rejects payment gateway with SSL error.",
            "Update fails at 75% with unknown error.",
        ]

        def handle_followup(response_text, key):
            followup = st.text_input("Your response:", key=key)
            if followup:
                save_message(user_email, "User", followup)
                save_message(user_email, "Bot", response_text)
                st.write(f"🤖 Chatbot: {response_text}")
                st.session_state.chat_stage = "end"

        if st.session_state.chat_stage == "start":
            choice = st.radio("Choose an issue:", options)

            if st.button("Submit"):
                st.session_state.user_choice = choice
                save_message(user_email, "User", choice)
                st.session_state.chat_stage = "response"
                st.rerun()

        if st.session_state.chat_stage == "response":
            choice = st.session_state.user_choice

            if choice == options[0]:
                st.write("🤖 Confirm phone model and app version?")
                resp = st.text_input("Your response:", key="q1")
                if resp:
                    save_message(user_email, "User", resp)
                    save_message(user_email, "Bot", "Unsupported thermostat. We can roll back or offer a discount.")
                    st.write("🤖 Chatbot: Unsupported thermostat. We can roll back or offer a discount.")
                    handle_followup("Thanks for your patience!", "followup1")

            elif choice == options[1]:
                st.write("🤖 Are both devices logged in with same account?")
                resp = st.text_input("Your response:", key="q2")
                if resp:
                    save_message(user_email, "User", resp)
                    save_message(user_email, "Bot", "Try Force Full Sync in settings.")
                    st.write("🤖 Chatbot: Try Force Full Sync in settings.")
                    handle_followup("A patch will fix this next week.", "followup2")

        if st.session_state.chat_stage == "end":
            if st.button("Start new chat"):
                st.session_state.chat_stage = "start"
                st.session_state.user_choice = None
                st.rerun()
