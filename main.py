from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import  sdfasd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on AWS App Runner"}


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "timestamp": datetime.now().isoformat()},
        status_code=200
    )

