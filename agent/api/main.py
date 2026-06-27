import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from api.routers import agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ FinSight Agent API starting up...")
    yield
    print("FinSight Agent API shutting down...")


app = FastAPI(
    title="FinSight Agent API",
    description="Multi-Agent Financial Analysis Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router, prefix="/agent", tags=["Agent"])


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "FinSight Agent API",
        "agents": ["data", "analysis", "rag", "report", "alert"],
    }
