from app.models.story import StoryRequest, StoryResponse
from app.utils.users import get_user_profile
from app.config import OPENAI_API_KEY
from openai import OpenAI
import logging

client = OpenAI(api_key=OPENAI_API_KEY)

def build_prompt(user_id: str, data: StoryRequest) -> str:
    print("\n🔍 Building story prompt...")
    print(f"📝 Input data: {data}")
    
    profile = get_user_profile(user_id) or {}
    name = profile.get("name", "the child")
    print(f"👤 User profile: {profile}")
    
    # Build prompt based on available inputs
    prompt_parts = []
    
    # Add user profile context
    likes_list = profile.get("likes", [])
    likes = ", ".join(likes_list)
    personality = profile.get("personality", "kind and curious")
    likes_part = f" and loves {likes}" if likes else ""
    profile_prompt = f"Write a story for a child named {name} who is {personality}{likes_part}."
    prompt_parts.append(profile_prompt)
    print(f"👤 Profile prompt part: {profile_prompt}")
    
    # Add image context if available
    if data.image_keys:
        image_descriptions = ", ".join([key.split("/")[-1].split(".")[0] for key in data.image_keys])
        image_prompt = f"Include these elements in the story: {image_descriptions}."
        prompt_parts.append(image_prompt)
        print(f"🖼 Image prompt part: {image_prompt}")
    
    # Add text instructions if available
    if data.instructions:
        instruction_prompt = f"Follow these instructions: {data.instructions}"
        prompt_parts.append(instruction_prompt)
        print(f"📋 Instruction prompt part: {instruction_prompt}")
    
    # Add length requirement
    length_map = {
        "Short": "Make it brief, about 2-3 paragraphs.",
        "Medium": "Make it a medium-length story, about 4-5 paragraphs.",
        "Long": "Make it a longer story, about 6-8 paragraphs."
    }
    length_prompt = length_map.get(data.length, "Make it a medium-length story.")
    prompt_parts.append(length_prompt)
    print(f"📏 Length prompt part: {length_prompt}")
    
    # Add age-appropriate requirement
    age_prompt = "Make it engaging for a 3 to 6 year old."
    prompt_parts.append(age_prompt)
    print(f"👶 Age prompt part: {age_prompt}")
    
    final_prompt = " ".join(prompt_parts)
    print(f"\n✨ Final prompt:\n{final_prompt}\n")
    
    return final_prompt


def generate_story(user_id: str, data: StoryRequest) -> StoryResponse:
    prompt = build_prompt(user_id, data)
    try:
        print("🤖 Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly bedtime storyteller for young children."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.85
        )
        story_text = response.choices[0].message.content.strip()
        print(f"📖 Generated story:\n{story_text}\n")
        
        # Use a regex or more robust extraction for the title
        import re
        match = re.match(r"Title[:\-]?\s*(.+)", story_text, re.IGNORECASE)
        title = match.group(1) if match else "A Special Adventure"
        print(f"📌 Extracted title: {title}")
        
        return StoryResponse(
            title=title,
            story=story_text,
            image_keys=data.image_keys
        )
    except Exception as e:
        logging.exception("Error generating story")
        print(f"❌ Error generating story: {e}")
        return StoryResponse(
            title="Error",
            story="Sorry, we couldn't generate your story right now. Please try again later.",
            image_keys=data.image_keys
        )