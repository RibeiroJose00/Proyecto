from robot import Robot
from logger import Logger
from client import Client
import random as rand

class G_compiler():
    def __init__(self, robot):
        self.robot = robot
        self.log = Logger()
        self.aprender = 0 #0 = desactivado, 1 = activado
        self.n_client = 0
        self.client_dict = {}
        pass


    def gen_client(self, name, address):
        """Genera un objeto cliente con el nombre y la direccion del cliente"""
        self.n_client += 1
        #Lo agregamos a la lista de clientes
        self.client_dict[address] = Client(name)
        pass

    ##### COMANDOS DE CONEXION #####        

    def client_connect(self, name, address):
        #Comando de conexion de cliente
        #Si existe un objeto cliente con el mismo id, se retorna un mensaje de bienvenida
        if address in self.client_dict:
            client = self.client_dict[address]
            if client.name == name:        
                res = 'Bienvenido de vuelta'
                return res
        else:
            com = "Conectar al servidor"
            #Si no existe, se crea el objeto cliente
            self.gen_client(name, address)
            res = 'Bienvenido ' + str(name)
            self.log.register(0, com, res)
            return res
        
    def client_disconnect(self, address):
        #Comando de desconexion de cliente
        if address in self.client_dict:
            com = "Desconectar del servidor"
            res = "Desconectado"
            if self.robot.get_estado() == 1:
                self.client_disconnect_robot(address)
            del self.client_dict[address]
            self.log.register(0, com, res)
            return res
        else:
            res = "No existe el cliente"
            return res
        
    def client_connect_robot(self, address):
        com = "Conectar"
        if  self.check(address) == 0:
            self.robot.set_estado(1)
            self.client_dict[address].set_connection_state(1)
            res = self.robot.get_intro_msg()
            self.log.register(0, com, res)
            return res
        elif self.check(address) == 1:
            res = "El robot ya esta siendo utilizado por otro cliente"
            return res
        elif self.check(address) == None:
            res = "Ud. ya esta conectado al robot"
            return res
        elif self.check(address) == 404:
            res = "No existe el cliente"
            return res
    
    def client_disconnect_robot(self, address):
        com = "Desconectar"
        if self.check(address) == None:
            self.robot.set_estado(0)
            self.desmotor(address)
            self.learn_mode(0, address)
            self.client_dict[address].set_connection_state(0)
            res = 'Desconectado del robot'
            self.log.register(0, com, res)
            return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res         
            
        
    ##### COMANDOS DE MODO #####

    def coordenadas(self, orden, address):
        orden = int(orden)
        mode = self.robot.get_mode()
        if self.check(address) == None:
        #Comando de coordenadas absolutas
            if orden == mode:
                res = 'El robot ya esta en ese modo'
                return res
            elif orden == 0:
                com = "G90"
                res = self.robot.send_command(com)
                self.robot.set_mode(0)
                self.log.register(self.aprender, com, res)
                return res
            elif orden == 1:
                com = "G91"
                res = self.robot.send_command(com)
                self.robot.set_mode(1)
                self.log.register(self.aprender, com, res)
                return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        
    def auto(self, filename, address):
        #Comando de modo automatico
        if self.check(address) == None:
            filename = filename + '.txt'
            command = "Auto: " + filename
            answer = "Ejecutando"
            self.log.register(0, command, answer)
            command_list = self.log.read_file(filename)
            res_list = []
            res_list = self.robot.send_command_list(command_list)
            new_res_list = []
            for i in range(len(command_list)):
                com = command_list[i]
                for j in range(len(res_list[i])):
                    res = res_list[i][j]
                    new_res_list.append(res)
                    self.log.register(self.aprender, com, res)
            command = "Auto: " + filename
            answer = "Finalizado"
            self.log.register(0, command, answer)
            return new_res_list
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res

    def learn_mode(self, modo, address):
        com = "Aprender: " + str(modo)
        actual = self.aprender
        if self.check(address) == None:
            if actual == modo:
                res = 'El robot ya esta en modo aprender'
                return res
            elif modo == 0 and actual == 1:
                self.aprender = 0
                res = 'Modo aprender desactivado'
                random_n = rand.randint(0, 100)
                self.log.save_task("Descarte " + str(random_n))
                self.log.register(0, com, res)
                return res
            elif modo == 1 and actual == 0:
                self.aprender = 1
                res = 'Modo aprender activado'
                self.log.register(1, com, res)
                return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        
    def save_task(self, address, filename):
        #Comando de generacion de tarea
        if self.aprender == 0:
            res = 'El robot no esta en modo aprender'
            return res
        elif self.aprender == 1:
            self.log.save_task(filename)
            res = 'Tarea ' + filename +  ' guardada'
            return res
        self.learn_mode(0, address)
        self.log.save_task(filename)
        pass

    ##### COMANDOS DE CONTROL #####

    def actmotor(self, address):
        #Comando de activar motores
        if self.check(address) == None:
            motores = self.robot.get_motor_state()
            if motores == 1:
                res = 'Los motores ya estan activados'
                return res
            elif motores == 0:
                com = "M17"
                res = self.robot.send_command(com)
                res = 'Motores Activados'
                self.log.register(self.aprender, com, res)
                self.robot.set_motor_state(1)
                return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        pass
    
    def desmotor(self, address):
        if self.check(address) == None:
            #Comando de desactivar motores
            motores = self.robot.get_motor_state()
            if motores == 0:
                res = 'Los motores ya estan desactivados'
                return res
            elif motores == 1:
                com = "M18"
                res = self.robot.send_command(com)
                res = 'Motores Desactivados'
                self.log.register(self.aprender, com, res)
                self.robot.set_motor_state(0)
                return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        pass
    
    def move(self, x, y, z, v, address):
        if self.check(address) == None:
            #Comando de movimiento
            #Si los siguientes tres caracteres son numeros, es un comando de movimiento
            #Escribir en formato Gcode
            motores = self.robot.get_motor_state()
            if motores == 1:
                if v == 0:
                    vmax = self.robot.VLmax
                    v = vmax/2
                com = "G1 X" + x + " Y" + y + " Z" + z + " F" + v
                res = self.robot.send_command(com)
                self.log.register(self.aprender, com, res)
                return res
            else: 
                res = 'Los motores estan desactivados'
                return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        
    def home(self, address):
        if self.check(address) == None:
            #Comando de homing
            com = "G28"
            res = self.robot.send_command(com)
            self.log.register(self.aprender, com, res)
            return res
        elif self.check(address) is not None:
            res = 'Ud no esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        
    def grip(self, orden, address):
        if self.check(address) == None:
            #Comando de activar gripper
            if orden == 0:
                com = "M5"
                res = self.robot.send_command(com)
                self.log.register(self.aprender, com, res)
                return res
            elif orden == 1:
                com = "M3"
                res = self.robot.send_command(com)
                self.log.register(self.aprender, com, res)
                return res
        elif self.check(address) is not None:
            res = 'No esta conectado al robot'
            return res
        elif self.check(address) == 404:
            res = 'No existe el cliente'
            return res
        
    ##### COMANDOS DE REPORTES #####

    def init_log(self):
        #Se genera el log
        self.log.log_init()
        pass

    def end_log(self):
        #Se finaliza el log
        self.log.log_end()
        pass
    
    def get_log(self):
        #Se obtiene el log
        log = self.log.get_log()
        return log
    
    def report(self, address):
        if address in self.client_dict:
            #Comando de reporte
            com = "M114"
            res = self.robot.send_command(com)
            for j in range(len(res[1])):
                if res[1][j] == "X":
                    pos_end = res[1].find(" ", j+1)
                    x = res[1][j+2:pos_end]
                elif res[1][j] == "Y":
                    pos_end = res[1].find(" ", j+1)
                    y = res[1][j+2:pos_end]
                elif res[1][j] == "Z":
                    pos_end = res[1].find(" ", j+1)
                    z = res[1][j+2:pos_end]
                elif res[1][j] == "E":
                    pos_end = res[1].find(" ", j+1)
                    e = res[1][j+2:pos_end]
            
            robot_posicion = "X: " + x + " Y: " + y + " Z: " + z + " E: " + e + '\n'
            connect_status = self.robot.get_estado()
            self.log.register(self.aprender, com, robot_posicion)
            report_list = self.log.report(connect_status, robot_posicion)
            return report_list
        else:
            res = "No existe el cliente"
            return res

    def get_specs(self, address):
        if address in self.client_dict:
            #Hacemos un diccionario con los atributos del robot
            com = "Especificaciones"
            altura = str(self.robot.altura)
            ancho = str(self.robot.ancho)
            largo = str(self.robot.largo)
            VLmax = str(self.robot.VLmax)
            VAmax = str(self.robot.VAmax)
            specs = ["Altura: " + altura + " mm", "Ancho: " + ancho +
                     " mm", "Largo: " + largo + " mm", "Velocidad Lineal Maxima: " +
                     VLmax + " mm/min", "Velocidad Angular Maxima: " + VAmax + " mm/min"]
            
            #Retornamos el diccionario
            res = "Enviadas"
            self.log.register(0, com, res)
            return specs
        else:
            res = "No existe el cliente"
            return res
    
    def get_mode(self):
        #Comando de obtencion de modo
        mode = self.robot.get_mode()
        return mode
    
    def get_client_dict(self):
        #Comando de obtencion de lista de clientes
        client_dict = self.client_dict
        return client_dict
    # Podemos hacer una funcion get_task que devuelva el contenido de la respuesta #
    
    ##### COMANDO DE CHECK #####
    
    def check(self, address):
        #Comando de check
        #Primero checkea si existe el cliente
        if address in self.client_dict:
            #Si existe, se verifica si el robot esta siendo utilizado por otro cliente
            client_connection = self.client_dict[address].get_connection_state()
            robot_connection = self.robot.get_estado()
            if client_connection == 1:
                res = None #None = cliente conectado
            elif client_connection == 0 and robot_connection == 1:
                res = 1 #1 = robot conectado a otro cliente
            elif client_connection == 0 or robot_connection == 0:
                res = 0 #0 = robot desconectado
            return res
        else:
            res = 404 #404 = cliente no existe
            return res
        
        
    
