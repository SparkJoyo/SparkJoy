from fastapi import FastAPI
from app.routes import auth, story, user, health 

app = FastAPI()

# Register routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(story.router)  
app.include_router(health.router) 
