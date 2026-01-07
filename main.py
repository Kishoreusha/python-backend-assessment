from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import Base, engine
from api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GitHub Repository Tracker",
    description="Python Backend Engineer Take Home Assessment",
    version="1.0.0"
)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

app.include_router(router)