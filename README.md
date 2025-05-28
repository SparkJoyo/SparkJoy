# 🧸 Joyo Story Time

Joyo Story Time is a fun, AI-powered web app that lets users create personalized bedtime stories.

---

## ✨ Features

- 🧑‍💻 User login 
- 📝 Story generation 
- 🎨 Visuals and illustrations generated from your images
- 🎵 AI-generated background music
- 🔄 **Synchronized story experience:** Text, visuals, and music are presented together, page by page
- 💾 Save & view your own stories

---

## 🚩 MVP Goal

Allow a parent to:
1. Upload 0–5 images or provide text instructions.
2. Generate a personalized story inspired by the images.
3. Create visuals (illustrations) and background music that incorporate the uploaded images.
4. **Present the story in a synchronized, read-along/watch-along format** suitable for toddlers (ages 3–5), where text, visuals, and music are in sync.

---

## 🛠️ MVP Feature List

- **Image Upload**: Upload 1–5 images (drag & drop or file picker).
- **Text Instruction**: Or provide text instruction on how to generate a story
- **Story Generation**: AI generates a short, age-appropriate story using the images as inspiration.
- **Visuals Generation**: AI creates illustrations or animates the uploaded images to match the story.
- **Music Generation**: AI generates simple, soothing background music.
- **Synchronized Story Presentation**: Interactive storybook format with:
  - Pages/slides for each part of the story
  - **Synchronized display of generated visuals, text, and music** (see [Story Synchronization](#-story-synchronization))
  - Play/pause for background music
  - Large, readable text for toddlers and parents to read along

---

## 🏗️ MVP Architecture

### Frontend (UI)
- **Framework**: Streamlit (for rapid prototyping) or React (for more custom UI)
- **Pages**:
  1. Home / Login
  2. Image Upload
  3. Story Generation Progress
  4. **Synchronized Storybook Viewer** (read/watch along, see [Story Synchronization](#-story-synchronization))

### Backend (API)
- **Framework**: FastAPI
- **Endpoints**:
  - `/upload-images`: Accepts image uploads
  - `/generate-story`: Accepts image references, returns story text
  - `/generate-visuals`: Accepts images/story, returns illustrations/animations
  - `/generate-music`: Returns music file/stream
  - `/save-story` (optional): Save story to user profile
  - **All endpoints work together to generate and synchronize assets for each story segment/page**

### AI/ML Services
- **Story Generation**: OpenAI GPT-4 (prompted with image descriptions)
- **Visuals Generation**: DALL-E, Stable Diffusion, or similar (using uploaded images as input/context)
- **Music Generation**: Simple AI music generator (e.g., Google Magenta, Suno, or a 3rd-party API)
- **Image Analysis**: Use CLIP or similar to describe images for story context
- **Synchronization Logic**: Backend returns a structured response with text, visual, and music for each segment (see [Story Synchronization](#-story-synchronization))

### Storage
- **Images**: AWS S3
- **Stories/Metadata**: DynamoDB or simple database

---

## 🗂️ Project Structure

```
yoyo-story-time/
├── frontend/      # Streamlit or React app
│   ├── pages/
│   ├── components/
│   │   └── storybook_player.py  # Handles sync of text, image, music
│   └── ...
├── backend/       # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   │   ├── story_generator.py
│   │   │   ├── visual_generator.py
│   │   │   └── music_generator.py
│   │   └── models/
│   └── ...
├── infra/         # Docker, Terraform, etc.
└── README.md
```

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Auth**: AWS Cognito
- **Storage**: AWS S3 / DynamoDB
- **AI**: OpenAI GPT-4

---

## 🚀 Getting Started

### Setting up Virtual Environment

1. Create a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

### Running the Application

- FastAPI backend on `http://localhost:8000`
- Streamlit frontend on `http://localhost:8501`

---

## 🧪 Development Mode

Run frontend and backend separately for faster iteration.

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Streamlit)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
---

## 🎯 Release Milestones

| Version | Milestone Features                                                                 | Status        |
|---------|-------------------------------------------------------------------------------------|---------------|
| v0.1    | - User login/signup<br>- Image upload (1-5 images)<br>- Story generation (text only)<br>- Basic storybook UI (text only)<br> | In Progress   |
| v0.2    | - Visuals generation per story segment<br>- Synchronized storybook: text + visuals<br>- Improved UI for page-by-page navigation<br> | Planned       |
| v0.3    | - Music generation (background or per segment)<br>- Full synchronization: text, visuals, music<br>- Play/pause music controls<br> | Planned       |
| v0.4    | - Save/read/share stories<br>- User profile & story library<br>- Polished, accessible UI/UX<br> | Planned       |
| v1.0    | - Optional narration (AI or parent-recorded)<br>- Full test coverage<br>- Production deployment<br>- Feedback & analytics<br> | Planned       |

**Notes:**
- Each version builds on the previous, with a focus on seamless synchronization of story text, visuals, and music starting in v0.3.
- See the [Story Synchronization](#-story-synchronization) section for technical details on how assets are kept in sync.
- Milestones may be adjusted based on user feedback and technical feasibility.

## 🪪 License

MIT

## 🧩 Story Synchronization

To create a seamless, engaging experience for toddlers and parents, the app synchronizes story text, visuals, and music on a per-page (or per-segment) basis.

### Synchronization Strategy
- **Story Segmentation:** The generated story is split into logical segments or pages (e.g., 1–2 sentences per page).
- **Asset Generation:** For each segment, the backend generates:
  - Story text
  - A corresponding visual (illustration or image, often referencing the uploaded images)
  - (Optionally) A music clip, or a single background music track for the whole story
- **Pre-generation:** All assets are generated before the storybook is presented, ensuring smooth navigation and playback.

### Backend Responsibilities
- Accept uploaded images and generate a story, splitting it into segments.
- For each segment, generate a visual and (optionally) a music clip.
- Return a structured response containing all assets for each segment.

#### Sample API Response
```json
{
  "story_segments": [
    {
      "text": "Once upon a time, a little bear found a shiny red ball.",
      "image_url": "https://s3.amazonaws.com/yourbucket/story123/page1.png",
      "music_url": "https://s3.amazonaws.com/yourbucket/story123/page1.mp3"
    },
    {
      "text": "The bear rolled the ball to his friend, the puppy.",
      "image_url": "https://s3.amazonaws.com/yourbucket/story123/page2.png",
      "music_url": "https://s3.amazonaws.com/yourbucket/story123/page2.mp3"
    }
    // ... more segments
  ],
  "background_music_url": "https://s3.amazonaws.com/yourbucket/story123/bg.mp3" // optional
}
```

### Frontend Responsibilities
- Fetch the structured story from the backend.
- Present the story in a page-by-page format, displaying the text and visual for the current segment.
- Play the corresponding music clip for each page, or a continuous background track.
- Update all elements in sync as the user navigates between pages.

#### Pseudocode Example
```python
story_segments = [
    {"text": "...", "image_url": "...", "music_url": "..."},
    # ...
]
current_page = 0
background_music_url = "..."

def on_page_change(new_page):
    display(story_segments[new_page]["text"])
    display_image(story_segments[new_page]["image_url"])
    play_music(story_segments[new_page].get("music_url", background_music_url))
```

### Key Points
- All assets are pre-generated for a smooth, interactive experience.
- Synchronization is handled by updating the text, visual, and music together as the user navigates through the story.
- This approach ensures that each page is engaging and cohesive for young children and their parents.

---
=======
