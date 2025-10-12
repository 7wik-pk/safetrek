from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api import stats_trends

load_dotenv(".env")  # Load variables from .env file

from typing import List

from config import settings

# --- FastAPI app ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    # allow all origins (temporary)
    allow_credentials=False,
    
    # to disallow all origins later
    # allow_credentials=True,

    allow_origins = (settings.allowed_origins or ["*"]),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Registering endpoints from different modules/groups of endpoints
from api import basic_data, stats_trends, factors_dry as factors, blackspot_corridor

app.include_router(basic_data.app)
app.include_router(stats_trends.app)
app.include_router(factors.app)
app.include_router(blackspot_corridor.router)

