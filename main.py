from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello</h1>"


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "timestamp": datetime.now().isoformat()},
        status_code=200
    )

