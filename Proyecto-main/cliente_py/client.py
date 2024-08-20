from xmlrpc.client import ServerProxy
import struct
import pickle
import cv2
import socket
from threading import Thread

class Client:
    def __init__(self, host, port, update_image_callback):
        self.host = host
        self.port = port
        self.proxy = ServerProxy(f'http://{host}:{port}/')
        self.update_image_callback = update_image_callback
        self.connection_state = False

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
    
    ## Comandos de video ##

    def connect_to_video_stream(self):
        self.connection_state = True
        self.video_thread = Thread(target=self._connect_video_stream, daemon=True)
        self.video_thread.start()

    def _connect_video_stream(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 9000))

            data = b""
            payload_size = struct.calcsize("Q")

            while self.connection_state:

                while len(data) < payload_size:

                    packet = self.client_socket.recv(2*1024)
                    if not packet: 
                        print("Error: no packet")
                        break

                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.client_socket.recv(2*1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.update_image_callback(frame)

            self.update_image_callback(None)

        except socket.error as e:
            print(f"Failed to connect to video streaming server: {e}")
        
        except cv2.error as e:
            print(f"Failed to show frame: {e}")
            