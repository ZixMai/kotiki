from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifespan import lifespan
from app.api.routers import kotiki


app = FastAPI(lifespan=lifespan, root_path="/api")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(kotiki.router, prefix="/v1/files", tags=["files"])

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}