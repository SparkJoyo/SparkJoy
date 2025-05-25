
# 🧸 Yoyo Story Time

Yoyo Story Time is a fun, AI-powered web app that lets users create personalized bedtime stories.

---

## ✨ Features

- 🧑‍💻 User login via AWS Cognito
- 📝 Story generation with OpenAI API
- 💾 Save & view your own stories
---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Auth**: AWS Cognito
- **Storage**: AWS S3 / DynamoDB
- **AI**: OpenAI GPT-4

---

## 🚀 Getting Started

```bash
cd infra/docker
docker-compose up --build
```

This will start:
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

## 📁 Project Layout

```
yoyo-story-time/
├── frontend/      # Streamlit app
├── backend/       # FastAPI backend
└── infra/         # Docker, Terraform, etc.
```

---


## 🎯 Release Milestones

| Version | Target Features                                          | Status       |
|---------|----------------------------------------------------------|--------------|
| `v0.1`  | ✅ User login<br>✅ profile creation ✅ Story generation<br>| In Progress  |
| `v0.2`  | 🔊 Add narration<br>🖼️ Add illustrations | Planned      |
| `v1.0`  | 🧪 Full test coverage<br>🚀 Production deployment<br>👨‍👩‍👧 Polished UI and UX | Planned      |

Each version is tagged and released on GitHub once stable. Use tags like `v0.1`, `v0.2`, etc. to track milestones.

"""

## 🪪 License

MIT
