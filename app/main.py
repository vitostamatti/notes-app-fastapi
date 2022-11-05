from fastapi import FastAPI
from app.routers import notes, notes_groups, user, login
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME
    )
app.include_router(
    login.router, 
    prefix=settings.API_PREFIX,
    tags=["login"]
)
app.include_router(
    user.router, 
    prefix=f"{settings.API_PREFIX}/user", 
    tags=["user"]
)
app.include_router(
    notes_groups.router, 
    prefix=f"{settings.API_PREFIX}/user",
    tags=["notes_groups"]
)
app.include_router(
    notes.router, 
    prefix=f"{settings.API_PREFIX}/user",
    tags=["notes"]
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/docs")
