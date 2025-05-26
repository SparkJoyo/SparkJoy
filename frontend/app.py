import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv() 

API_BASE = os.getenv("API_BASE")

st.set_page_config(page_title="Yoyo Story Time", page_icon="📚")
st.title("🧠 Joyo Story Time")

def check_backend():
    try:
        r = requests.get(f"{API_BASE}/ping")
        return r.status_code == 200
    except Exception as e:
        print(f"Backend connection failed: {e}")
        return False

if check_backend():
    st.success(f"✅ Backend connected: {API_BASE}")
else:
    st.error("❌ Cannot connect to backend. Please make sure your backend is running.")

st.markdown("Welcome to Yoyo Story Time! Start by logging in using the sidebar.")


