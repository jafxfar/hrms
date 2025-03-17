import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.router import router as user_router
from .routes.hr_router import router as hr_router
from .database import init_db
from .models import models

# Initialize database (creates tables if they don't exist)
init_db()

app = FastAPI(
    title="HR Management System",
    description="System for managing employee data and HR processes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(user_router, tags=["Users"])
app.include_router(hr_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}