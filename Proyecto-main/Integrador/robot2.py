
class Robot:
    
    def __init__(self, estado):
        self.estado = estado # 0: libre, 1: ocupado
        self.altura = 100
        self.ancho = 50
        self.largo = 50
        self.VLmax = 3
        self.VAmax = 250
        self.mode = 0 # 0: coordenadas absolutas, 1: coordenadas relativas
        self.motor_state = 0 # 0: motores desactivados, 1: motores activados      
        pass

    def start_serial(self):
        if self.estado == 1:
            #Abrimos el puerto serie
            #self.ser = serial.Serial('COM3', 115200, timeout=1, write_timeout=1) # Configura el puerto serie
            #Mandamos el comando por el puerto serie
            #self.ser.write_terminator = b'\r\n'  # Carácter de retorno de carro (CR) y nueva línea (NL)
            #Leemos la respuesta del robot
            #res = self.ser.readline().decode()
            #Retornamos la respuesta
            res = "respuesta del puerto serie"
            return res
        elif self.estado == 0:
            pass
        pass
        
        
    def send_command(self, command):
        if self.estado == 1:
            #Tomamos el comando del atributo
            data = command
            #Escibimos el comando en el puerto serie
            print(data)
            if command == "M114":
                res = "posicion: X4 Y5 Z6"
            #Leemos la respuesta del robot
            else:
                res = "respuesta del puerto serie"
            #Retornamos la respuesta
            return res
        elif self.estado == 0:
            pass
    pass

    def send_command_list(self, command_list):
        response_list = []
        for com in command_list:
            response_list[com] = self.send_command(com) 
        return response_list
    
    def get_mode(self):
        return self.mode
    
    def set_mode(self, mode):
        self.mode = mode
        pass
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self, estado):
        self.estado = estado
        pass

    def get_motor_state(self):
        return self.motor_state
    
    def set_motor_state(self, estado):
        self.motor_state = estado
        pass
    
    def get_specs(self):
        #Hacemos un diccionario con los atributos del robot
        altura = str(self.altura)
        ancho = str(self.ancho)
        largo = str(self.largo)
        VLmax = str(self.VLmax)
        VAmax = str(self.VAmax)
        
        specs = {'altura': altura, 'ancho': ancho, 'largo': largo, 'VLmax': VLmax, 'VAmax': VAmax}
        #Retornamos el diccionario
        return specs
    
    def get_pos(self):
        self.ser.write_terminator = b'\r\n'  # Carácter de retorno de carro (CR) y nueva línea (NL)
        if self.estado == 1:
            #Tomamos el comando del atributo
            data = "M114"
            #Escibimos el comando en el puerto serie
            print("Escribiendo en puerto serie")
            #Leemos la respuesta del robot
            pos = "posicion"
            #Guardamos la respuesta en el atributo
            self.pos = pos
            #Retornamos la respuesta
            return self.pos
        elif self.estado == 0:
            pass
        pass
    
"""def do_client_disconnect(self, args):
        client_disconnect: Desconectar a un cliente del robot
        # Comando de salida
        if self.conection == 0 and self.robot.estado == 0:
            print("No hay clientes conectados")
        elif self.conection == 0 and self.robot.estado == 1:
            print("Desconectando cliente...")
            client_dict = self.compiler.get_client_dict()
            for n in client_dict:
                if client_dict[n].get_connection_state() == 1:
                    client_dict[n].set_connection_state(0)
                    self.robot.set_estado(0)
                    self.compiler.desmotor("Admin")
                    self.compiler.log.register(0, "Desconectar cliente", "Cliente desconectado")
                    print("Cliente desconectado")
        else: 
            print("Ud. esta conectado al robot")            
        pass"""
    