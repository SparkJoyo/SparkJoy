import streamlit as st
from utils.api import generate_story, upload_file

st.set_page_config(page_title="Generate Story", page_icon="📝")

st.title("📝 Generate Your Personalized Story")

# Check login
if "token" not in st.session_state or st.session_state.token is None:
    st.warning("🔒 Please log in first.")
    st.stop()

token = st.session_state.token
profile = st.session_state.get("profile", {})

# Image upload section
st.subheader("📤 Upload Images (Optional)")
st.caption("Upload up to 5 images to inspire your story. If no images are provided, we'll use Elsa as the default character.")

uploaded_files = st.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
image_keys = []

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("❌ Please upload a maximum of 5 images.")
    else:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                s3_key = upload_file(token, uploaded_file)
                if s3_key:
                    st.success(f"Uploaded as `{s3_key}`")
                    image_keys.append(s3_key)
                else:
                    st.error(f"❌ Failed to upload {uploaded_file.name}")

# Text instructions section
st.subheader("✍️ Story Instructions (Optional)")
st.caption("Describe your story idea. You can include theme, setting, characters, or any other details you'd like!")

story_instructions = st.text_area(
    "Story Instructions",
    placeholder="Example: A magical adventure in an enchanted forest with a brave knight and a friendly dragon..."
)

story_length = st.select_slider(
    "Story Length",
    options=["Short", "Medium", "Long"],
    value="Medium"
)

# Generate story button
if st.button("✨ Generate Story"):
    with st.spinner("Generating your story..."):
        # Prepare data based on what's provided
        data = {
            "image_keys": image_keys,
            "instructions": story_instructions,
            "length": story_length
        }
        
        # Remove empty fields
        data = {k: v for k, v in data.items() if v}
        
        # If no images and no instructions, use Elsa as default
        if not image_keys and not story_instructions:
            data["instructions"] = "A story about Elsa"
        
        result = generate_story(token, data)
        if result:
            st.success(f"✅ Story: {result['title']}")
            st.write(result['story'])
        else:
            st.error("❌ Failed to generate story.")
