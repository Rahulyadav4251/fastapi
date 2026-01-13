from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return JSONResponse(
        content={"<h1>Hello from FastAPI on AWS App Runner</h1>"},
        media_type="text/html"
    )


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "timestamp": datetime.now().isoformat()},
        status_code=200
    )

