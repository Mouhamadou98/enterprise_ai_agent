# Import necessary libraries
from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="ACME Logistics AI Agent",
    description="Entreprise AI Agent for CRM, ERP, and Knowledge Management",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "ACME Logistics AI Agent is running!"}

