from datetime import datetime
from typing import Optional, Text
from pydantic import BaseModel

class MOBBase(BaseModel):
    fecha_creacion: datetime
    nombre: str
    
class MOBmodel(MOBBase):
    accion: Optional[str]
    


    

    