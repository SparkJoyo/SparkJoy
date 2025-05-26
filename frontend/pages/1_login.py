import streamlit as st
import datetime
from utils.api import login

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Login to Yoyo Story Time")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.user_id = None

with st.form("login_form"):
    user_id = st.text_input("User ID", value="user123")
    birthdate = st.date_input("Birthdate", value=datetime.date(2018, 6, 15))
    submitted = st.form_submit_button("Login")

    if submitted:
        token = login(user_id, birthdate.isoformat())
        if token:
            st.session_state.token = token
            st.session_state.user_id = user_id

            st.success(f"✅ Welcome back, {user_id}!")
            st.markdown("[➡️ Go to Profile Page](./2_Profile)")
            st.stop()
        else:
            print("Login failed", token)
            st.error("❌ Login failed. Please check your credentials.")