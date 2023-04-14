import pydantic

class Aviso(pydantic.BaseModel):
    numero: int
    titulo: str
    body: str
    
    