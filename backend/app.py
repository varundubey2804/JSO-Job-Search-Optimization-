from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import logging
from dotenv import load_dotenv
import os
from dotenv import find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="JSO Agent Backend API",
    description="Backend for Job Search Optimization AI Agent",
    version="1.0.0"
)

# CORS middleware for Node Gateway interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for prototype, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "status": "ok",
        "service": "JSO Agent Backend",
        "version": "1.0.0"
    }

# Run server
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting server at http://{host}:{port}")

    uvicorn.run("app:app", host=host, port=port, reload=True)