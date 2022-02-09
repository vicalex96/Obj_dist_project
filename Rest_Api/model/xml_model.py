from datetime import datetime
from typing import Optional, Text
from pydantic import BaseModel

class PhoneCreate(BaseModel):
    nombre: str
    marca: Optional[str]
    fecha_estreno: Optional[datetime]
    ancho_cm: Optional[int]
    alto_cm: Optional[int]
    memoria_gb: Optional[int]
    ram_gb: Optional[int]
    descripcion: Optional[Text]  
    
class PhoneInXML(BaseModel):
    id: int
    nombre: str
    marca: str
    fecha_estreno: datetime
    ancho_cm: int
    alto_cm: int
    memoria_gb: int
    ram_gb: int
    descripcion: Text 
    fecha_registro: datetime
    publicado: bool
   
  
  
class MOBBase(BaseModel):
    fecha_creacion: datetime
    nombre: str
    
class MOBmodel(MOBBase):
    accion: Optional[str]


    

    