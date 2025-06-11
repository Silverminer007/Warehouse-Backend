from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8" />
        <title>Willkommen bei Packliste API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0; padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #005587, #00a2ff);
                color: white;
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 0.2em;
            }
            p {
                font-size: 1.3em;
                margin-top: 0;
            }
            a {
                color: #ffdd57;
                text-decoration: none;
                font-weight: bold;
                margin-top: 1em;
                display: inline-block;
                font-size: 1.2em;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Willkommen bei der Packliste API</h1>
        <p>Nutze die API über die Endpunkte unter <code>/api/v1/packliste/{packliste_id}</code></p>
        <a href="/docs">Zur API-Dokumentation (Swagger UI)</a>
    </body>
    </html>
    """
    return html_content
