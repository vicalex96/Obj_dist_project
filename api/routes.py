from fastapi import APIRouter, Body, status,HTTPException

from model.xml_model import PhoneCreate, PhoneInXML
from repository.phones_xml import PhoneRepo
router = APIRouter()

""" class PhoneCreate(BaseModel):
    id: int
    nombre: str
    marca: Optional[str]
    fecha_estreno: Optional[datetime]
    ancho_cm: Optional[int]
    alto_cm: Optional[int]
    memoria_gb: Optional[int]
    ram_gb: Optional[int]
    descripcion: Optional[Text]  
    
    PhoneRepo: la clase que contine los formatos
    PhoneCreate: el formato para crear informacion de telefono
    PhoneInXML: el formato para almacenar el telefono en el XML
"""
@router.post("/",response_model= PhoneInXML, status_code= status.HTTP_201_CREATED)
def create_phone( new_phone: PhoneCreate)-> PhoneInXML:
    phone_repo = PhoneRepo()
    return phone_repo.create_phone(new_phone = new_phone)
    
@router.delete("/{id}/")
def delete_phone_by_id(id: int) -> int:
    print('hola')
    phone_repo = PhoneRepo()
    delete_id: int = phone_repo.delete_phone_by_id(id= id)
    if not delete_id:
        print('error')
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    print('respuesta')
    return delete_id

@router.delete("/{nombre}/")
def delete_phone_by_name(nombre: str) -> id:
    phone_repo = PhoneRepo()
    delete_id: int = phone_repo.delete_phone_by_name(nombre = nombre)
    if not delete_id:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return delete_id

@router.get("/data")
def get_data_phone():
    phone_repo = PhoneRepo()
    return phone_repo.get_all_phones()

@router.get("/estructure")
def delete_estructure_phone():
    return "este endpintpermite crear un blog"

@router.post("/replicate")
def replicate_XML():
    return "este endpintpermite crear un blog"

@router.post("/retore")
def restore_XML():
    return "este endpintpermite crear un blog"