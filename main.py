from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Get all environment variables
    env_vars = dict(os.environ)
    
    # Create HTML table of environment variables
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Environment Variables</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f2f2f2; font-weight: bold; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .key { font-weight: bold; color: #0066cc; }
            .value { font-family: monospace; word-break: break-all; }
            .sensitive { color: #cc0000; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>📊 Environment Variables</h1>
        <p><strong>Total Variables:</strong> %(count)d</p>
        <table>
            <tr>
                <th>Variable Name</th>
                <th>Value</th>
            </tr>
            %(rows)s
        </table>
    </body>
    </html>
    """
    
    # Create table rows
    rows = []
    sensitive_keys = ['password', 'secret', 'key', 'token', 'auth', 'credential']
    
    for key, value in sorted(env_vars.items()):
        # Check if key might be sensitive
        is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_keys)
        
        row = f"""
        <tr>
            <td class="key">{key}</td>
            <td class="value {'sensitive' if is_sensitive else ''}">
                {value if not is_sensitive else '***** (REDACTED) *****'}
            </td>
        </tr>
        """
        rows.append(row)
    
    html_final = html_content % {
        'count': len(env_vars),
        'rows': '\n'.join(rows)
    }
    
    return HTMLResponse(content=html_final)


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "timestamp": datetime.now().isoformat()},
        status_code=200
    )

