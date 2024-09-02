import serial
import time

class Robot:
    
    def __init__(self, estado):
        self.estado = estado # 0: libre, 1: ocupado
        self.altura = 238
        self.ancho = 514
        self.largo = 257
        self.VLmax = 50
        self.VAmax = 0.5
        self.Rmin= 90
        self.mode = 0 # 0: coordenadas absolutas, 1: coordenadas relativas
        self.motor_state = 0 # 0: motores desactivados, 1: motores activados      
        self.ser = None
        self.intro_msg = self.start_serial()
        pass
    
    def get_mode(self):
        return self.mode
    
    def set_mode(self, mode):
        self.mode = mode
        pass
    
    def get_intro_msg(self):
        return self.intro_msg
    
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

    def start_serial(self):
        try:
            self.ser = serial.Serial('COM3', 115200, timeout=1, write_timeout=1) # Configura el puerto serie
            res = "Puerto serie abierto - Puerto: " + self.ser.name + " - Baudrate: " + str(self.ser.baudrate)
        except serial.SerialException:
            res = "El puerto ya esta abierto o no existe"
            return res
        
        if self.ser.is_open:
            response_lines = []
            #self.ser.write_terminator = b'\r\n'  # Carácter de retorno de carro (CR) y nueva línea (NL)
            #Mandamos el comando por el puerto serie
            time.sleep(1)
            while True:
                line = self.ser.readline().decode('utf-8')
                if not line:
                    break  # Stop when no more lines are received
                response_lines.append(line.strip())  # Append each line to the list
        return response_lines
    
    def send_command(self, command):
        if self.estado == 1:
            if self.ser.is_open:  
                response_lines = []
                #self.ser.write_terminator = b'\r\n'  # Carácter de retorno de carro (CR) y nueva línea (NL)
                #Mandamos el comando por el puerto serie
                data = command
                data += "\r\n"
                self.ser.write(data.encode('utf-8'))
                time.sleep(1)
                while True:
                    line = self.ser.readline().decode()
                    if not line:
                        break  # Stop when no more lines are received
                    response_lines.append(line.strip())  # Append each line to the list
            return response_lines
        elif self.estado == 0:
            ans = "Nadie esta usando el robot en este momento"
            return ans
         
    def send_command_list(self, command_list):
        response_list = []
        for com in command_list:
            response = self.send_command(com)
            response_list.append(response)
        return response_list
    
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
    
    def serial_close(self):
        self.ser.close()
        pass
