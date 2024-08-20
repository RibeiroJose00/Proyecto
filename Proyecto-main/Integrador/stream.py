import cv2
import pickle
import struct
import socket
from threading import Thread

class Stream:
    def __init__(self):
        # Inicializamos el stream de video
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        

    def _start_streaming(self):
        # Se crea el socket especifico de la parte de streaming
        try: 
            server_socket = socket.create_server(('localhost', 9000), family=socket.AF_INET, backlog=5)
            client_socket, client_address = server_socket.accept()
            if client_socket:
                print(f"Conexion establecida con {client_address}")

        except socket.error as e:
            print(f"Socket Error: {e}")
    

        # Comando de inicio de video streaming
        cap = cv2.VideoCapture(0)

        # Si no se abre la camara, se muestra un mensaje de error y se finaliza la funcion
        if not cap.isOpened():
            print("Error: no se pudo abrir la camara")
            return

        print("Iniciando video streaming")   
        # Abrimos un bucle para enviar los frames de la camara

        while True:
            try:    
                ret, frame = cap.read()

                if not ret:
                    print("Error: no se pudo obtener el frame")
                    break
                
                data = pickle.dumps(frame)
                message_size = struct.pack("Q", len(data)) + data # Q -> unsigned long long int
                client_socket.sendall(message_size)

            except cv2.error as e:
                print(f"Camara error: {e}")
                break
                
            except socket.error as e:
                print(f"Socket Error: {e}")
                break
        
        # Se cierran la camara y el socket
        cap.release()
        client_socket.close()
        server_socket.close() 

    def start_streaming(self):
        streaming_thread = Thread(target = self._start_streaming, daemon = True)
        streaming_thread.start()



