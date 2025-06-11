from pydantic import BaseModel

class PacklisteItem(BaseModel):
    raum: str
    regal: str
    kiste: str
