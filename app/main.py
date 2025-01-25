from fastapi import FastAPI
from app.endpoints import router

app = FastAPI(
    title="FinGhadi API",
    description="Backend for activity suggestions based on weather and location.",
    version="1.0.0",
)

# Include the endpoints
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome Mohammed to FinGhadi API"}
