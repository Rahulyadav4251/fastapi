from datetime import datetime
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
async def read_root():
    # Simple HTML with button to /env
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            .button {
                display: inline-block;
                padding: 15px 30px;
                font-size: 18px;
                background-color: #0066cc;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #0052a3;
            }
            .info {
                margin-top: 20px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FastAPI Application</h1>
            <p>Click below to view all environment variables:</p>
            <a href="/env" class="button">View Environment Variables</a>
            <div class="info">
                <p>App: <strong>%(app_name)s</strong></p>
                <p>Client: <strong>%(client_id)s</strong></p>
                <p>Environment: <strong>%(env)s</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Fill in the template with environment variables
    html_final = html_content % {
        'app_name': os.getenv('APP_NAME', 'FastAPI App'),
        'client_id': os.getenv('CLIENT_ID', 'Unknown'),
        'env': os.getenv('APP_ENV', 'development')
    }
    
    return HTMLResponse(content=html_final)


@app.get("/env")
async def show_environment():
    """Show all environment variables in a nice HTML page"""
    env_vars = dict(os.environ)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Environment Variables</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .header {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
            }
            .back-button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #666;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .back-button:hover {
                background-color: #555;
            }
            .stats {
                background: white;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            table {
                border-collapse: collapse;
                width: 100%%;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #0066cc;
                color: white;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f0f0f0;
            }
            .key {
                font-weight: bold;
                color: #0066cc;
                font-family: monospace;
            }
            .value {
                font-family: monospace;
                word-break: break-all;
            }
            .sensitive {
                color: #cc0000;
                font-style: italic;
            }
            .copy-btn {
                padding: 5px 10px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                margin-left: 10px;
            }
            .copy-btn:hover {
                background-color: #218838;
            }
        </style>
        <script>
            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('Copied to clipboard!');
                }, function(err) {
                    console.error('Could not copy text: ', err);
                });
            }
            
            function toggleSensitive() {
                const rows = document.querySelectorAll('.sensitive-row');
                rows.forEach(row => {
                    const isHidden = row.querySelector('.value').textContent.includes('***REDACTED***');
                    if (isHidden) {
                        row.querySelector('.value').textContent = row.dataset.originalValue;
                    } else {
                        row.querySelector('.value').textContent = '***REDACTED***';
                    }
                });
            }
        </script>
    </head>
    <body>
        <div class="header">
            <a href="/" class="back-button">← Back to Home</a>
            <h1>📊 Environment Variables</h1>
            <div class="stats">
                <p><strong>Total Variables:</strong> %(count)d</p>
                <p><strong>App:</strong> %(app_name)s | <strong>Client:</strong> %(client_id)s | <strong>Environment:</strong> %(env)s</p>
                <button onclick="toggleSensitive()" style="padding: 8px 15px; background: #ffc107; border: none; border-radius: 3px; cursor: pointer;">
                    Toggle Sensitive Data
                </button>
            </div>
        </div>
        
        <table>
            <tr>
                <th>Variable Name</th>
                <th>Value <small>(Click to copy)</small></th>
            </tr>
            %(rows)s
        </table>
    </body>
    </html>
    """
    
    # Create table rows
    rows = []
    sensitive_keys = ['password', 'secret', 'key', 'token', 'auth', 'credential', 'pass']
    
    for key, value in sorted(env_vars.items()):
        # Check if key might be sensitive
        is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_keys)
        
        # Prepare display value
        display_value = value if not is_sensitive else '***REDACTED***'
        
        row = f"""
        <tr class="{'sensitive-row' if is_sensitive else ''}" {'data-original-value="' + value + '"' if is_sensitive else ''}>
            <td class="key">{key}</td>
            <td class="value {'sensitive' if is_sensitive else ''}">
                {display_value}
                <button class="copy-btn" onclick="copyToClipboard('{key}={value}')">Copy</button>
            </td>
        </tr>
        """
        rows.append(row)
    
    # Use double %% for percentage signs in Python string formatting
    html_content_escaped = html_content.replace('%%', '%')
    
    html_final = html_content_escaped % {
        'count': len(env_vars),
        'app_name': os.getenv('APP_NAME', 'FastAPI App'),
        'client_id': os.getenv('CLIENT_ID', 'Unknown'),
        'env': os.getenv('APP_ENV', 'development'),
        'rows': '\n'.join(rows)
    }
    
    return HTMLResponse(content=html_final)


@app.get("/env/json")
async def get_environment_json():
    """API endpoint to get environment variables as JSON"""
    env_vars = dict(os.environ)
    
    # Filter out sensitive data
    sensitive_keys = ['password', 'secret', 'key', 'token', 'auth', 'credential', 'pass']
    filtered_vars = {}
    
    for key, value in env_vars.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            filtered_vars[key] = "***REDACTED***"
        else:
            filtered_vars[key] = value
    
    return JSONResponse(
        content={
            "environment_variables": filtered_vars,
            "count": len(env_vars),
            "app_name": os.getenv('APP_NAME', 'FastAPI App'),
            "client_id": os.getenv('CLIENT_ID', 'Unknown'),
            "environment": os.getenv('APP_ENV', 'development'),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/env/{variable_name}")
async def get_specific_env(variable_name: str):
    """Get specific environment variable"""
    value = os.getenv(variable_name)
    
    if value is None:
        return JSONResponse(
            content={"error": f"Variable '{variable_name}' not found"},
            status_code=404
        )
    
    # Check if sensitive
    sensitive_keys = ['password', 'secret', 'key', 'token', 'auth', 'credential', 'pass']
    is_sensitive = any(sensitive in variable_name.lower() for sensitive in sensitive_keys)
    
    return JSONResponse(
        content={
            "variable": variable_name,
            "value": "***REDACTED***" if is_sensitive else value,
            "sensitive": is_sensitive,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "app_name": os.getenv("APP_NAME", "Not set"),
            "client_id": os.getenv("CLIENT_ID", "Not set"),
            "environment": os.getenv("APP_ENV", "Not set"),
            "port": os.getenv("APP_PORT", "8000")
        },
        status_code=200
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)