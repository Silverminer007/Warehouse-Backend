from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.packliste_service import generiere_packliste_pdf

router = APIRouter()

@router.get("/{packliste_id}", response_class=FileResponse)
async def packliste_herunterladen(packliste_id: int):
    pfad = await generiere_packliste_pdf(packliste_id)
    if pfad is None:
        raise HTTPException(status_code=404, detail="Packliste nicht gefunden")
    return FileResponse(pfad, filename=f"packliste_{packliste_id}.pdf")
