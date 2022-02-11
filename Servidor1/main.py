import Pyro4
from datetime import datetime
import random 
import socket
from os.path import exists

IP = "192.168.0.136" #ip de refernecia, no se usa en el codigo de este servidor, pero lo usa para que se usa para que se conecten a el
PORT = 8002  #puerto de referencia, no se usa en el codigo de este servidor, pero lo usa para que se usa para que se conecten a el     

# necesario para enviar el xml al coordinador 
IP_Pyro4 = "192.168.1.100"
PORT_Pyro4 = 8001

class Replicator(object):
    __fecha_creacion = datetime(1900, 1, 1, 0, 0, 0,0) #cuando se creó la replica por ultima vez
    __nombre = "replicador"
    __accion = "---"
    
    def replicate_service(self, client):
        self.execute_vote(client)
        return self.execute_commit(client)
        
    def execute_vote(self, client):
        self.__accion = random.choice(('COMMIT', 'ABORT'))
        #self.__accion = 'COMMIT' #borrar !!!#-----------------------------------------------------------
        print(self.__accion)
        client.send(('VOTE_' + self.__accion).encode('utf-8'))
        
    def execute_commit(self, client):
        mensaje = client.recv(1024).decode('utf-8')
       
        if(mensaje == "GLOBAL_COMMIT"):
            self.save_data_xml(client)
            client.send('SAVED'.encode('utf-8'))
            self.__fecha_creacion = datetime.now()
            print("datos replicados ", self.__fecha_creacion)
        
        elif(mensaje == "GLOBAL_ABORT"):
            print("ejecucion de replicacion abortada")
            client.close()
            
        self.__accion = "---"
    
    def save_data_xml(self, client):
        file = open('obj_data.xml','wb')
        file_data = client.recv(1024)
        file.write(file_data)
        file.close()

class Restorer(object):
    __fecha_creacion = datetime(1900, 1, 1, 0, 0, 0,0) #cuando se restauro por ultima vez
    __nombre = "restaurador"
    __accion = "---"
    
    def restore_data_service(self, client):
        try:
            print("se esta conectado por pyro4")
            ns = Pyro4.locateNS(IP_Pyro4,PORT_Pyro4) # IP_Pyro4 = "IP para conectarse con el coordinador" PORT_Pyro4 = 8001
            uri = ns.lookup('coordinador')
            conexion = Pyro4.Proxy(uri)
            
            print("esta leyendo el archivo")
            if( exists("./obj_data.xml")):
                file = open('obj_data.xml','r')
                file_data = file.read(1024)
                response = conexion.recibir_objetos(file_data)
                print("respues = ", response)
                if(response == "sent"):
                    self.__fecha_creacion = datetime.now()
                    print("el objeto fue enviado")
                    return "sent"
            else:
                raise FileNotFoundError()
        except FileNotFoundError as err:
            print("archivo no encontrado")
            return "error"
        except Exception:
            print("❌ Error: ocurrio un error al recibir el archivo")
            return "error"
        
        return "error"
    

if( __name__ == "__main__" ):
    #ejecutar el servidor TCP por sockets
    global replicate, restore
    replicate = Replicator()
    restore = Restorer()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen()

    while True: 
        try:
            client, direccion = server.accept() 
            mensaje = client.recv(1024).decode('utf-8')
            
            if(mensaje == "VOTE_REQUEST"):
                replicate.replicate_service(client)
                
            elif(mensaje == "RESTORE_DATA"):
                print("ejecutando restore_data_service")
                response = restore.restore_data_service(client)
                client.send(response.encode('utf-8')) 
            
            else:
                client.send("el mensjae no puede ser procesado".encode('utf-8'))   
                
            client.close()
            
        except ConnectionError:
            print(" /!\ Error: ¡cliente se desconecto repentinamente o no se pudo entablar comunicacion! \n \n")
            client.close()

    

