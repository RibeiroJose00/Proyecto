
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket
from threading import Thread
import time



class RequestHandler(SimpleXMLRPCRequestHandler):
    # Reescribo el parametro path para que el servidor solo responda a
    # las llamadas a http://direccion/POO
    rpc_paths = ('/', '/RPC2', '/POO')


class Server:

    def __init__(self, direccion, puerto: int, compiler):
        self.direccion = direccion
        self.puerto = puerto
        self.compiler = compiler
        try:
            self.servidor = SimpleXMLRPCServer((self.direccion, self.puerto), logRequests=True,
                                            requestHandler=RequestHandler)
        except socket.error:
            print("Socket Error")
            pass
    
        # Se registran todas las funciones definidas aca abajo
        self.register()
        
        self.thread = Thread(target = self.listen_connection, daemon = True)
        self.thread.start()
        
        self.msg = "Servidor iniciado en el puerto {}".format(self.puerto)
        print(self.msg)
        
    def listen_connection(self):
        self.servidor.serve_forever()

    def stop_listen(self):
        self.servidor.shutdown()
        self.thread.join()

    def get_state(self):
        return self.thread.is_alive()

    def register(self):
        ##### Funciones del servidor #####
        ### Funciones de conexion ###
        self.servidor.register_function(self.connect)
        self.servidor.register_function(self.disconnect)
        self.servidor.register_function(self.connect_robot)
        self.servidor.register_function(self.disconnect_robot)
        ### Funciones de modo ###
        self.servidor.register_function(self.get_mode)
        self.servidor.register_function(self.coord_abs)
        self.servidor.register_function(self.coord_rel)
        self.servidor.register_function(self.learn_on)
        self.servidor.register_function(self.learn_off)
        self.servidor.register_function(self.save_task)
        self.servidor.register_function(self.auto)
        ### Funciones de control ###
        self.servidor.register_function(self.act_motor)
        self.servidor.register_function(self.des_motor)
        self.servidor.register_function(self.move)
        self.servidor.register_function(self.home)
        self.servidor.register_function(self.act_grip)
        self.servidor.register_function(self.des_grip)
        ### Funciones de reporte ###
        self.servidor.register_function(self.get_specs)
        self.servidor.register_function(self.report)
        #self.servidor.register_function(self.get_task)
        self.servidor.register_function(self.get_log)
        ### Registro de la instancia del compilador ###
        self.servidor.register_instance(self.compiler)
        ### Funciones de introspeccion (libreria) ###
        self.servidor.register_introspection_functions()
    

    ##### DEFINICION DE COMANDOS DE CONEXION #####
        
    def connect(self, name):
        # Comando de conexion al robot
        client_name = name
        client_thread = self.thread.name
        if client_name == None:
            ans = "Ingrese un nombre valido"
        else:
            ans = self.compiler.client_connect(client_name, client_thread)
        return ans
    
    def disconnect(self):
        # Comando de desconexion al robot
        client_thread = self.thread.name
        ans = self.compiler.client_disconnect(client_thread)
        return ans
    
    def connect_robot(self):
        # Comando de conexion al robot
        client_thread = self.thread.name
        ans = self.compiler.client_connect_robot(client_thread)
        return ans
    
    def disconnect_robot(self):
        # Comando de desconexion al robot
        client_thread = self.thread.name
        ans = self.compiler.client_disconnect_robot(client_thread)
        return ans
    
    ##### DEFINICION DE COMANDOS DE CONTROL #####

    def act_motor(self):
        # Comando de activacion de motores
        client_thread = self.thread.name
        ans = self.compiler.actmotor(client_thread)
        return ans      
        
    def des_motor(self):
        # Comando de desactivacion de motores
        client_thread = self.thread.name
        ans = self.compiler.desmotor(client_thread)
        return ans
    
    def move(self, x, y, z, v):
        # Comando de movimiento
        client_thread = self.thread.name
        ans = self.compiler.move(x,y,z,v,client_thread)
        return ans
        
    def home(self):
        # Comando de homing
        client_thread = self.thread.name
        ans = self.compiler.home(client_thread)
        return ans
        
    def act_grip(self):
        """act: Activar gripper"""
        # Comando de activar gripper
        client_thread = self.thread.name
        ans = self.compiler.grip(1,client_thread)
        return ans
    
    def des_grip(self):
        """des: Desactivar gripper"""
        # Comando de desactivar gripper
        client_thread = self.thread.name
        ans = self.compiler.grip(0,client_thread)
        return ans

    ##### DEFINICION DE COMANDOS DE MODO #####

    def coord_abs(self):
        """coordabs: Modo coordenadas absolutas"""
        # Comando de coordenadas absolutas
        client_thread = self.thread.name
        ans = self.compiler.coordenadas(0, client_thread)
        return ans
       
    def coord_rel(self):
        """coordrel: Modo coordenadas relativas"""
        # Comando de coordenadas relativas
        client_thread = self.thread.name
        ans = self.compiler.coordenadas(1, client_thread)
        return ans
       
    def auto(self, filename):
        """auto: Modo automatico"""
        # Comando de modo automatico
        client_thread = self.thread.name
        ans = self.compiler.auto(filename, client_thread)
        return ans
       
    def learn_on(self):
        """aprender: Activar o desactivar el modo de aprendizaje"""
        # Comando de generacion de tarea
        client_thread = self.thread.name
        ans = self.compiler.set_aprender(1, client_thread)
        return ans
    
    def learn_off(self):
        """aprender: Activar o desactivar el modo de aprendizaje"""
        # Comando de generacion de tarea
        client_thread = self.thread.name
        ans = self.compiler.set_aprender(0, client_thread)
        return ans
    
    def save_task(self, filename):
        """save: Guardar tarea"""
        # Comando de guardado de tarea
        client_thread = self.thread.name
        ans = self.compiler.save_task(client_thread, filename)
        return ans
    
    ##### DEFINICION DE COMANDOS DE REPORTES #####
    def get_log(self):
        """log: Obtener log"""
        # Comando de obtencion de log
        ans = self.compiler.get_log()
        return ans

    def get_mode(self):
        modo = self.compiler.get_mode()
        if modo == 0:
            ans = "Modo coordenadas absolutas"
            return ans
        else:
            ans = "Modo coordenadas relativas"
            return ans
    
    def report(self):
        """rep: Enviar reporte de modo de coordenadas y posicion"""
        # Comando de reporte
        client_thread = self.thread.name
        report = self.compiler.report(client_thread)
        return report
    
    def get_specs(self):
            # Comando de obtencion de especificaciones
        client_thread = self.thread.name
        
        specs = self.compiler.get_specs(client_thread)
        return specs

    
        