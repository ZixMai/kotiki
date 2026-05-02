import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        reload=True,
        host="0.0.0.0",
        port=8080,
        log_level="warning",
    )