
from datetime import datetime
import random 
import socket
from os.path import exists

# es la direccion usada para iniciar el servidor TCP
IP = "192.168.1.100" #colocar IP_local o la IP publica de la PC
server_num = int(input("Indique cual es este server (1 o 2):"))
if(server_num == 1):
    PORT = 8002
elif(server_num == 2):
    PORT = 8003
    
class Replicator(object):
    __fecha_creacion = datetime(1900, 1, 1, 0, 0, 0,0) #cuando se creó la replica por ultima vez
    __nombre = "replicador"
    __accion = "---"
    
    def replicate_service(self, client):
        self.execute_vote(client)
        return self.execute_commit(client)
        
    def execute_vote(self, client):
        self.__accion = random.choice(('COMMIT', 'COMMIT', 'ABORT'))
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
            print("esta leyendo el archivo")
            if( exists("./obj_data.xml")):
                file = open('obj_data.xml','r')
                file_data = file.read(1024)
                if(file_data):
                    print("\nleido archivo:")
                    
                client.send(file_data.encode('utf-8'))
                mesage = client.recv(1024).decode('utf-8')
                
                if(mesage == "OK"):
                    self.__fecha_creacion = datetime.now()
                    print("el objeto fue enviado")
                    return "OK"
                
                elif(mesage == "fail"):
                    self.__fecha_creacion = datetime.now()
                    print("el archivo no fue recibido")
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
                client.send("el mensaje no puede ser procesado".encode('utf-8'))   
                
            client.close()
            
        except ConnectionError:
            print(" /!\ Error: ¡cliente se desconecto repentinamente o no se pudo entablar comunicacion! \n \n")
            client.close()