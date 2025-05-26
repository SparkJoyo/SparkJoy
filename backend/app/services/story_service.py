from app.models.story import StoryRequest, StoryResponse
from app.utils.users import get_user_profile
from app.config import OPENAI_API_KEY
from openai import OpenAI
import logging

client = OpenAI(api_key=OPENAI_API_KEY)

def build_prompt(user_id: str, data: StoryRequest) -> str:
    profile = get_user_profile(user_id) or {}
    name = profile.get("name", "the child")
    likes_list = profile.get("likes", [])
    likes = ", ".join(likes_list)
    personality = profile.get("personality", "kind and curious")
    characters = ", ".join([key.split("/")[-1].split(".")[0] for key in data.character_keys]) if data.character_keys else "magical friends"
    settings = ", ".join([key.split("/")[-1].split(".")[0] for key in data.setting_keys]) if data.setting_keys else "wonderful places"
    likes_part = f" and loves {likes}" if likes else ""
    return (
        f"Write a magical, heartwarming story for a child named {name}. "
        f"The story should feature characters such as {characters} and take place in settings like {settings}. "
        f"{name} is {personality}{likes_part}. "
        f"Make it engaging for a 3 to 6 year old."
    )


def generate_story(user_id: str, data: StoryRequest) -> StoryResponse:
    prompt = build_prompt(user_id, data)
    try:
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
        # Use a regex or more robust extraction for the title
        import re
        match = re.match(r"Title[:\-]?\s*(.+)", story_text, re.IGNORECASE)
        title = match.group(1) if match else "A Special Adventure"
        return StoryResponse(
            title=title,
            story=story_text,
            character_keys=data.character_keys,
            setting_keys=data.setting_keys
        )
    except Exception as e:
        logging.exception("Error generating story")
        return StoryResponse(
            title="Error",
            story="Sorry, we couldn't generate your story right now. Please try again later.",
            character_keys=data.character_keys,
            setting_keys=data.setting_keys
        )