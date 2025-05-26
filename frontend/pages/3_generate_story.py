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

st.subheader("🎭 Character Images (Optional)")
selected_characters = st.multiselect("Choose character image keys", character_keys)

st.subheader("🌍 Setting Images (Optional)")
selected_settings = st.multiselect("Choose setting image keys", setting_keys)

# Generate story
if st.button("✨ Generate Story"):
    with st.spinner("Generating your story..."):
        # Use default character "Elsa" if no characters are selected
        if not selected_characters:
            selected_characters = ["Elsa"]
            
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
