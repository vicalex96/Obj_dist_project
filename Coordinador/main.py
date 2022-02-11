import Pyro4
import socket
from datetime import datetime
from threading import Lock, Thread
import time
from random import choice
from os import remove

global IP_S1, PORT_S1, IP_S2, PORT_S2, IP_coordinador, PORT_coordinador
IP_coordinador = "localhost" # este se puede quedar asi
PORT_coordinador = 8001

IP_S1 = "192.168.1.100" #IP del servidor de replicacion, si es coloca colocar localhost o IP de la maquina
PORT_S1 = 8002
IP_S2 = "192.168.1.100" #IP del servidor de replicacion, si es coloca colocar localhost o IP de la maquina
PORT_S2 = 8003


mutex = Lock()

@Pyro4.expose
class Coordinador(object):
    __fecha_creacion = datetime(1900, 1, 1, 0, 0, 0,0)
    __nombre = ""
    __accion = "---"
    
    def conect_server(self, IP, PORT,file_data):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP,PORT))
        client.send('VOTE_REQUEST'.encode('utf-8'))
        with mutex:
            if(self.__accion == "---" 
            or self.__accion == "GLOBAL_COMMIT"):
                self.__accion = client.recv(1024).decode('utf-8') 
        
        with mutex:
            if(self.__accion == "VOTE_COMMIT"):
                client.send('GLOBAL_COMMIT'.encode('utf-8'))
                client.send(file_data.encode('utf-8'))
                mesage = client.recv(1024).decode('utf-8')
                print(mesage)
   
            elif(self.__accion == "VOTE_ABORT"):
                client.send('GLOBAL_ABORT'.encode('utf-8'))
                print(" uno de los servidores aborto el proceso")
            
        client.close()
    
    def replicar_objetos(self,file_data):
        try:
            t1 = Thread(name="conect_server1",target=self.conect_server, args=(IP_S1,PORT_S1,file_data))
            t2 = Thread(name="conect_server2",target=self.conect_server, args=(IP_S2,PORT_S2,file_data))

            t1.start()
            t2.start()
            t2.join()
            t1.join()
            
            if(self.__accion == "waiting"):
                raise Exception(" el proceso no altero al atributo accion")
            elif(self.__accion == "VOTE_COMMIT"):
                response =  'finished'
            elif(self.__accion == "VOTE_ABORT"):
                response = 'abort'
                
        except Exception as err:
            print(" ❌ Error: ocurrio un error, ", err)
            response = 'error'
        finally:
            self.__accion = "---" 
            return response

    def restaurar_objetos(self):
        print("Vamos a restaurar el objeto")
        file_data = None
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            op1 = (IP_S1, PORT_S1)
            op2 = (IP_S2, PORT_S2)
            op_choosed = choice((op1, op2))
            print(op_choosed)
            client.connect(op_choosed)
            client.send('RESTORE_DATA'.encode('utf-8'))
            file_data = self.recibir_objetos(client)
            
        except Exception as err:
            print(" ❌ Error: ocurrio un error", err)
        finally:
            client.close 
            return file_data
        
    
    def recibir_objetos(self, client):
        file_data = None
        try:
            file_data = client.recv(1024).decode('utf-8')   
            if(file_data):
                print("data recibida")
                client.send('OK'.encode('utf-8'))
                
            else:
                print("no se encontró la data")
                client.send('fail'.encode('utf-8'))
                client.close 
                
        except Exception as err:
            print("❌ Error: ocurrio un error al recibir el archivo", err)
        finally:
            return file_data
        
        
    


if(__name__ == "__main__"):  
    daemon = Pyro4.Daemon(IP_coordinador,PORT_coordinador)
    uri = daemon.register(Coordinador)
    ns = Pyro4.locateNS()
    ns.register('coordinador',uri)
    print(uri)
    daemon.requestLoop()

