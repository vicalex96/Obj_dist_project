from typing import  List
from fastapi import APIRouter, Body, status,HTTPException

from model.xml_model import MOBmodel, MOBBase
from repository.repo_mob import MOBRepo
router = APIRouter()

@router.post("/create",response_model= MOBmodel, status_code= status.HTTP_201_CREATED)
def create( new_obj: MOBBase)-> MOBmodel:
    """ Permite un objeto
    **Returns**:
    - **JSON**: el objeto creado
    """
    mob_repo = MOBRepo()
    return mob_repo.create_obj(new_obj = new_obj)
    
@router.delete("/delete/{name}/",status_code=status.HTTP_200_OK)
def delete(name: str) -> str:
    """ Elimina el objeto indicado del xml
    **Returns**:
    - **str**: status de culminacion
    """
    mob_repo = MOBRepo()
    deleted_obj: int = mob_repo.delete_obj(name = name)
    if not deleted_obj:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return " elimiando el objeto de id: " + str(deleted_obj)

@router.get("/consult/data/{name}/",response_model= MOBmodel, status_code= status.HTTP_200_OK)
def get_data(name:str) -> MOBmodel:
    """ Permite obtener la informacion de un objeto según su nombre
    **Returns**:
    - **JSON**: objeto objeto objetnido
    """
    mob_repo = MOBRepo()
    obj = mob_repo.get_obj(name = name)
    if not obj:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return obj

@router.get("/consult/estructure",response_model= List[MOBmodel], status_code= status.HTTP_200_OK)
def get_structure():
    """ Endpoint que para pedir la estructura del objeto en XML
    **Returns**:
    - **json**: informacion de la estructura del objeto
    """
    mob_repo = MOBRepo()
    objects = mob_repo.get_all_objs()
    if not objects:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return objects

@router.post("/replicate", response_model = MOBmodel, status_code= status.HTTP_200_OK)
def replicate():
    """Solicita la replicación del xml
    **Returns**:
    - **str**: mensaje de status de la replicación 
    """
    mob_repo = MOBRepo()
    resp =  mob_repo.replicate_xml()
    if not resp or resp.accion == "abort" or resp.accion == "error":
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return resp

@router.post("/restore", response_model = MOBmodel, status_code= status.HTTP_200_OK)
def restore():
    """
    Solicita los datos de XML de la ultima replica

    **Returns**:
    
    - **str**: mensaje de status de rescuperacion del xml
    """
    mob_repo = MOBRepo()
    resp =  mob_repo.restore_xml()
    print(resp)
    if not resp or resp.accion == "abort" or resp.accion == "error":
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    return resp