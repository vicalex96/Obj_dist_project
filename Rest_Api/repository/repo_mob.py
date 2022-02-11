from datetime import datetime
from xml.etree import cElementTree as et
from typing import List
import Pyro4

from model.xml_model import MOBmodel

phonexml = []
xml_file_name = "obj_data.xml"
IP_Pyro4 = 'distributed.ddns.net'
PORT_Pyro4 = 8002

class MOBRepo:
    def create_obj(self, *,new_obj: MOBmodel) -> MOBmodel:
        obj_dict = {}
        obj_dict.update(**new_obj.dict())

        # si existe el archivo xml agrega la inforamcion 
        try:
            doc_xml = et.parse(xml_file_name)
            archivo_xml = doc_xml.getroot()
            
            obj = et.Element('obj')
            for element in obj_dict:
                atribute = et.SubElement(obj,element)
                atribute.text = str(obj_dict[element])
            
            phones_tag = archivo_xml.find('objects')
            phones_tag.insert(0, obj)
      
            doc_xml.write(xml_file_name)  
        # si no existe crea el archivo y agrega la info
        except FileNotFoundError as e:
            
            obj = et.Element('obj')
            for element in obj_dict:
                atribute = et.SubElement(obj,element)
                atribute.text = str(obj_dict[element])
            
            root = et.Element('aplication')
            element = et.SubElement(root,'objects')
            element.append(obj)
            tree = et.ElementTree(root)
            with open(xml_file_name, "wb") as files:
                tree.write(files)
                
        return MOBmodel(**obj_dict) # el ** fuerza a que la clase PhoneInXML obtenga sus valores de los equivalentes en el diccionario
    
    def get_obj(self, *, name:str) -> MOBmodel: 
        tr = et.parse(xml_file_name)
        
        for element in tr.iter(): # tr.iter genera un iterable con las etiquetas del XML
            for subelement in element: # aqui te recorre los elementos internos de la etiqueta superior
                if(subelement.tag == 'obj'): # se busca informacion con la etiqueta obj
                    
                    if(str(subelement.find('nombre').text) == name ): # se busca el objeto por el nombre
                        obj_dict = { # se leen los elementos del objeto
                            "fecha_creacion": subelement.find('fecha_creacion').text ,
                            "nombre": subelement.find('nombre').text
                        }
                        return MOBmodel(**obj_dict)
        return None
          
    def get_all_objs(self) -> List[MOBmodel]:
        data_list = []
        tr = et.parse(xml_file_name)
        
        for element in tr.iter(): # tr.iter genera un iterable con las etiquetas del XML
            for subelement in element: # aqui te recorre los elementos internos de la etiqueta superior
                if(subelement.tag == 'obj'): # se busca informacion con la etiqueta obj
                    obj_dict = { # se leen los elementos del objeto
                        "fecha_creacion": subelement.find('fecha_creacion').text ,
                        "nombre": subelement.find('nombre').text
                    }
                    data_list.append(MOBmodel(**obj_dict))          
        return data_list
        
    def delete_obj(self, *, name:str) -> int:
        tr = et.parse(xml_file_name)
        for element in tr.iter(): # tr.iter genera un iterable con las etiquetas del XML
            for subelement in element: # aqui te recorre los elementos internos de la etiqueta superior
                if(subelement.tag == 'obj'): #se busca informacion con la etiqueta obj
                    if( str(subelement.find('nombre').text) == name ): #se busca el objeto por el nombre
                        element.remove(subelement) # se elimina el objeto
                        tr.write(xml_file_name) #se guardan los cambios
                        return subelement.find('nombre').text
        return None
        
    def replicate_xml(self, *, xml=None) -> str:
        print("")
        ns = Pyro4.locateNS(IP_Pyro4,PORT_Pyro4)
        uri = ns.lookup('coordinador')
        conexion = Pyro4.Proxy(uri)
        
        file = open('obj_data.xml','r')
        file_data = file.read(1024)
        
        resp = conexion.replicar_objetos(file_data)
        response = {
            'fecha_creacion': datetime.now(),
            'nombre': "El proceso de replicacion a terminado satisfactoriamente",
            'accion': resp          
        }
        if (resp == 'finished'):
            response['nombre'] = "La replicacion del xml ha concluido satisfactoriamente"
        elif(resp == 'abort'):
            response['nombre'] = "Uno o ambos servidores rechazaron la replicacion"
        else:
            response['nombre'] = "Ocurrio un error en el proceso de replicacion"
        return MOBmodel(**response)
    
    def restore_xml(self) -> str:
        ns = Pyro4.locateNS(IP_Pyro4,PORT_Pyro4)
        uri = ns.lookup('coordinador')
        conexion = Pyro4.Proxy(uri)
        response = {}
        file_data = conexion.restaurar_objetos()
            
        if(file_data ):
            file = open('obj_data.xml','wb')
            file.write(file_data.encode('utf-8'))
            file.close()
            response = {
                'fecha_creacion': datetime.now(),
                'nombre': "El proceso de replicacion a terminado satisfactoriamente",
                'accion': 'finished'
            }
        else: 
            response = {
                'fecha_creacion': datetime.now(),
                'nombre': "No se a encontrado el resplado o replica del xml",
                'accion': 'error'
            }
        
        return MOBmodel(**response)
    