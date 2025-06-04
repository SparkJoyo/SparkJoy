prompt = "I need a story for my 4-year-old, Sam, about a curious monkey exploring the jungle. He loves it when I ask him questions as we read. Could you weave in 2-3 simple questions within the story that I can ask Sam?"

# %%
from together import Together
from dotenv import load_dotenv
# %%
# Load environment variables from .env file
load_dotenv()

# %%
client = Together() # auth defaults to os.environ.get("TOGETHER_API_KEY")
# %%
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[
      {
        "role": "user",
        "content": "What are some fun things to do in New York?"
      }
    ]
)
print(response.choices[0].message.content)

