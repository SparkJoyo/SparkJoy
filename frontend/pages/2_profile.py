import streamlit as st
from utils.api import get_profile, update_profile, upload_file
import io

st.set_page_config(page_title="Profile", page_icon="👤")
st.title("👤 Edit Your Profile")

# ✅ Check login
if "token" not in st.session_state or st.session_state.token is None:
    st.warning("🔒 Please log in first.")
    st.stop()

token = st.session_state.token

# ✅ Load profile once
if "profile" not in st.session_state:
    st.session_state.profile = get_profile(token) or {}

profile = st.session_state.profile

# ✅ Profile form
with st.form("profile_form"):
    name = st.text_input("Name", value=profile.get("name", ""))
    bio = st.text_area("Bio", value=profile.get("bio", ""))
    favorite_color = st.text_input("Favorite Color", value=profile.get("favorite_color", ""))
    likes = st.text_input("Likes (comma-separated)", value=",".join(profile.get("likes", [])))

    # Editable keys
    image_keys = profile.get("image_keys", [])
    st.markdown("### 🖼 Character Image Keys")
    st.write(image_keys)

    # ✅ Upload new character image
    uploaded_file = st.file_uploader("Upload new character image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        with st.spinner("Uploading image..."):
            s3_key = upload_file(token, uploaded_file)
            if s3_key:
                st.success(f"Uploaded as `{s3_key}`")
                image_keys.append(s3_key)
            else:
                st.error("❌ Upload failed.")

    # ✅ Save form
    submitted = st.form_submit_button("💾 Save Profile")
    if submitted:
        updated_profile = {
            "name": name,
            "bio": bio,
            "favorite_color": favorite_color,
            "likes": [x.strip() for x in likes.split(",") if x.strip()],
            "image_keys": image_keys,
            "audio_keys": profile.get("audio_keys", []),
            "video_keys": profile.get("video_keys", [])
        }

        success = update_profile(token, updated_profile)
        if success:
            st.success("✅ Profile updated!")
            st.session_state.profile = updated_profile
        else:
            st.error("❌ Failed to update profile.")
