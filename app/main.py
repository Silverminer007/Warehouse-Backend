from fastapi import FastAPI
from app.api.v1 import packliste, root

def create_app():
    app = FastAPI(title="Packliste API")

    app.include_router(root.router)  # root ohne prefix für "/"
    app.include_router(packliste.router, prefix="/api/v1/packliste", tags=["Packliste"])

    return app

app = create_app()
