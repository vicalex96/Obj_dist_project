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
    
    
    
    def get_all_phones(self) -> List[PhoneInXML]:
        
        return phonexml
    
    def delete_phone_by_id(self, id: int):
        tr = et.parse(xml_file_name)
        for element in tr.iter():
            for subelement in element:
                if(subelement.tag == 'phone' and int(subelement.find('id').text) == id):
                    element.remove(subelement)
                    tr.write(xml_file_name)
                    return id
        return None

    def delete_phone_by_name(self, nombre: str):

        return 1
        
    