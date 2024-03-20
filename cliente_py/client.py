from xmlrpc.client import ServerProxy

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.proxy = ServerProxy(f'http://{host}:{port}/')

    ## Conexion y desconexion al servidor ##

    def connect(self, id):
        ans = self.proxy.connect(id)
        return ans
    
    def disconnect(self):
        ans = self.proxy.disconnect()
        return ans
    
    ## Conexion y desconexion al robot ##
    
    def connect_robot(self):
        ans = self.proxy.connect_robot()
        return ans
    
    def disconnect_robot(self):
        ans = self.proxy.disconnect_robot()
        return ans
    
    ## Comandos de control ##

    def act_motor(self):
        ans = self.proxy.act_motor()
        return ans
    
    def des_motor(self):
        ans = self.proxy.des_motor()
        return ans

    def move(self, x, y, z, speed):
        ans = self.proxy.move(x, y, z, speed)
        return ans
    
    def home(self):
        ans = self.proxy.home()
        return ans
    
    def act_grip(self):
        ans = self.proxy.act_grip()
        return ans
    
    def des_grip(self):
        ans = self.proxy.des_grip()
        return ans
    
    ## Comandos de cambio de modo ##

    def coord_mode(self, mode):
        if mode == 0:
            ans = self.proxy.coord_abs()
        elif mode == 1:
            ans = self.proxy.coord_rel()
        return ans
    
    def auto(self, file):
        ans = self.proxy.auto(file)
        return ans
    
    def learn(self, on_off):
        if on_off == 0:
            ans = self.proxy.learn_off()
        elif on_off == 1:
            ans = self.proxy.learn_on()
        return ans
    
    def save_task(self, filename):
        ans = self.proxy.save_task(filename)
        return ans

    ## Comandos de consulta ##

    def get_log(self):
        ans = self.proxy.get_log()
        return ans
    
    def get_mode(self):
        ans = self.proxy.get_mode()
        return ans
    
    def report(self):
        ans = self.proxy.report()
        return ans
    
    def get_specs(self):
        ans = self.proxy.get_specs()
        return ans

