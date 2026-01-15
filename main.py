from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os
from dotenv import dotenv_values


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

from fastapi.responses import HTMLResponse
import html


@app.get("/env", response_class=HTMLResponse)
async def get_env_page():
    # Reuse the same logic safely
    try:
        process_env = dict(os.environ)
    except Exception:
        process_env = {}

    try:
        dotenv_env = dotenv_values(".env") or {}
    except Exception:
        dotenv_env = {}

    def render_dict(title: str, data: dict):
        rows = "".join(
            f"<tr><td>{html.escape(str(k))}</td><td>{html.escape(str(v))}</td></tr>"
            for k, v in sorted(data.items())
        )
        return f"""
        <h2>{title} (count: {len(data)})</h2>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>Key</th><th>Value</th></tr>
            {rows or "<tr><td colspan='2'><i>No variables found</i></td></tr>"}
        </table>
        """

    html_content = f"""
    <html>
        <head>
            <title>Environment Variables</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; margin-bottom: 30px; }}
                th {{ background-color: #f0f0f0; }}
                td, th {{ padding: 6px 10px; text-align: left; }}
            </style>
        </head>
        <body>
            <h1>Environment Variables</h1>
            {render_dict("Process Environment Variables", process_env)}
            {render_dict(".env File Variables", dotenv_env)}
        </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/env/process")
async def get_process_environment():
    """
    Returns all environment variables available to the current process.
    Safe even if no environment variables are present.
    """
    try:
        env_vars = dict(os.environ)
    except Exception:
        env_vars = {}

    return JSONResponse(
        content={
            "env_vars": env_vars,
            "count": len(env_vars),
        },
        status_code=200,
    )


@app.get("/env/dotenv")
async def get_dotenv_environment():
    """
    Returns variables defined in the .env file only.
    Safe if the .env file does not exist or is empty.
    """
    try:
        dotenv_vars = dotenv_values(".env") or {}
    except Exception:
        dotenv_vars = {}

    return JSONResponse(
        content={
            "dotenv_vars": dotenv_vars,
            "count": len(dotenv_vars),
        },
        status_code=200,
    )



