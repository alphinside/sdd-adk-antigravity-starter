from fastapi import FastAPI
from restaurant_concierge.reservations import router as reservations_router

app = FastAPI(
    title="Restaurant Concierge API",
    description="Backend API for table reservation system",
    version="1.0.0"
)

app.include_router(reservations_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)