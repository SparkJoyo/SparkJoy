import streamlit as st
from utils.api import generate_story

st.set_page_config(page_title="Generate Story", page_icon="📝")

st.title("📝 Generate Your Personalized Story")

# Check login
if "token" not in st.session_state or st.session_state.token is None:
    st.warning("🔒 Please log in first.")
    st.stop()

token = st.session_state.token
profile = st.session_state.get("profile", {})

# Select images from profile or enter manually
character_keys = profile.get("image_keys", [])
setting_keys = profile.get("image_keys", [])  # reuse for now or customize

st.subheader("🎭 Character Images")
selected_characters = st.multiselect("Choose character image keys", character_keys)

st.subheader("🌍 Setting Images")
selected_settings = st.multiselect("Choose setting image keys", setting_keys)

# Generate story
if st.button("✨ Generate Story"):
    if not selected_characters or not selected_settings:
        st.error("Please select at least one character and one setting.")
    else:
        with st.spinner("Generating your story..."):
            data = {
                "character_keys": selected_characters,
                "setting_keys": selected_settings
            }
            result = generate_story(token, data)

            if result:
                st.success(f"✅ Story: {result['title']}")
                st.write(result['story'])
            else:
                st.error("❌ Failed to generate story.")
