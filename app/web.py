from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .main import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="dashboard")
