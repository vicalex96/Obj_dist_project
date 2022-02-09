from datetime import datetime
from xml.etree import cElementTree as et
from typing import List

from model.xml_model import PhoneCreate, PhoneInXML


phonexml = []
xml_file_name = "phones_data.xml"

class PhoneRepo:
    def create_phone(self, *,new_phone: PhoneCreate) -> PhoneInXML:
        phone_dict = {}
        phone_dict['id'] = 0
        phone_dict.update(**new_phone.dict())
        phone_dict["fecha_registro"] = datetime.now()
        phone_dict["publicado"] = True
             
        # si existe el archivo xml agrega la inforamcion 
        try:
            doc_xml = et.parse(xml_file_name)
            archivo_xml = doc_xml.getroot()
            len_phones = len(archivo_xml.findall('phones/phone'))
            last_phone = archivo_xml.find('phones/phone')
            if(len_phones > 0):
                phone_dict["id"] = int(last_phone.find('id').text) + 1
            else:
                phone_dict["id"] = 0
            phone = et.Element('phone')
            for element in phone_dict:
                atribute = et.SubElement(phone,element)
                atribute.text = str(phone_dict[element])
            
            phones_tag = archivo_xml.find('phones')
            phones_tag.insert(0, phone)

                    
            doc_xml.write(xml_file_name)  
        # si no existe crea el archivo y agrega la info
        except FileNotFoundError as e:
            
            phone = et.Element('phone')
            for element in phone_dict:
                atribute = et.SubElement(phone,element)
                atribute.text = str(phone_dict[element])
            
            
            root = et.Element('aplication')
            element = et.SubElement(root,'phones')
            element.append(phone)
            tree = et.ElementTree(root)
            with open(xml_file_name, "wb") as files:
                tree.write(files)
                
            
        phonexml.append(phone_dict)
        return PhoneInXML(**phonexml[-1]) # el ** fuerza a que la clase PhoneInXML obtenga sus valores de los equivalentes en el diccionario
    
    def get_phone(self, *,id:int = None, name:str = None) -> PhoneInXML:
        phone_dict = {
            "nombre": "",
            "marca": "",
            "fecha_estreno": "",
            "ancho_cm": 0,
             "alto_cm": 0,
            "memoria_gb": 0,
            "ram_gb": 0,
             "descripcion": ""
        }
        
        if(id != None and name != None ):
            raise Exception("get_phone: ambos argumentos no pueden contener informacion")
        if(id == None and name == None ):
            raise Exception("get_phone: algun argumento tiene que tener un valor asignado")
        
        tr = et.parse(xml_file_name)
        for element in tr.iter():
            for subelement in element:
                if(subelement.tag == 'phone'):
                    
                    if(int(subelement.find('id').text) == id or
                       str(subelement.find('nombre').text) == name ):
                        
                        print("objeto encontrado id:",subelement.find('id').text)
                        phone_dict['id'] = subelement.find('id').text
                        phone_dict['nombre'] = subelement.find('nombre').text
                        phone_dict['fecha_estreno'] = subelement.find('fecha_estreno').text
                        phone_dict['ancho_cm'] = subelement.find('ancho_cm').text
                        phone_dict['alto_cm'] = subelement.find('alto_cm').text
                        phone_dict['memoria_gb'] = subelement.find('memoria_gb').text
                        phone_dict['ram_gb'] = subelement.find('ram_gb').text
                        phone_dict['descripcion'] = subelement.find('descripcion').text
                        phone_dict['fecha_registro'] = subelement.find('fecha_registro').text
                        phone_dict['publicado'] = subelement.find('publicado').text
                        return PhoneInXML(**phone_dict)
        return None
        
    
    def get_all_phones(self) -> List[PhoneInXML]:
        return phonexml
    
    def delete_phone(self, *, id:int = None, name:str = None) -> int:
        if(id != None and name != None ):
            raise Exception("delete_phone: ambos argumentos no pueden contener informacion")
        if(id == None and name == None ):
            raise Exception("delete_phone: algun argumento tiene que tener un valor asignado")
        
        tr = et.parse(xml_file_name)
        for element in tr.iter():
            for subelement in element:
                if(subelement.tag == 'phone'):
                    if( int(subelement.find('id').text) == id or
                        str(subelement.find('nombre').text) == name ):
                        element.remove(subelement)
                        tr.write(xml_file_name)
                        return int(subelement.find('id').text)
        return None
        
    