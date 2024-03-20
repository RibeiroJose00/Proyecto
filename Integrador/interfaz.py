from cmd import Cmd
from server import Server
from robot import Robot
from g_compiler import G_compiler
import time

class Interfaz(Cmd):
    prompt = "<0>"
    intro = "\nIngrese un comando o ingrese 'help' para obtener una lista de comandos\nSi desea cerrar el programa y el servidor escriba 'EOF'"
    doc_header = 'Lista de comandos - Ingrese help <comando> para obtener ayuda'
    ruler = '-'

    def __init__(self):
        super(Interfaz, self).__init__()
        self.robot = Robot(0)
        self.compiler = G_compiler(self.robot)
        self.servidor = Server("192.168.111.168", 4000, self.compiler)
        self.conection = 0
        self.compiler.init_log()
        self.compiler.client_connect("Admin", "Admin")
        pass
    
    def do_connect(self, args):
        """connect: Realiza la conexión al robot si nadie esta conectado -
                Ingresar sin argumentos"""
        # Comando de conexion al robot
        res = self.compiler.client_connect_robot("Admin")
        for n in res:
            print(n)
        pass

    def do_disconnect(self, args):
        """disconnect: Desconectarse del robot
                Ingresar sin argumentos"""
        # Comando de salida
        res = self.compiler.client_disconnect_robot("Admin")
        print(res)
        pass
    
    def do_get_specs(self, args):
        """get_specs: Obtiene las especificaciones del robot
                Ingresar sin argumentos"""

        # Comando de obtencion de especificaciones
        
        print("Obteniendo especificaciones...")
        specs = self.robot.get_specs("Admin")
        print("Especificaciones obtenidas: ")
        print("")
        #Mostramos las especificaciones
        print("Altura: " + specs['altura'])
        print("Ancho: " + specs['ancho'])
        print("Largo: " + specs['largo'])
        print("Velocidad lineal maxima: " + specs['VLmax'])
        print("Velocidad angular maxima: " + specs['VAmax'])
        pass
    
    def do_motor_on(self, args):
        """motor_on: Activar motores
                Ingresar sin argumentos"""
        # Comando de activacion de motores
        
        print("Activando motores...")
        res = self.compiler.actmotor("Admin")
        print(res)
        pass
    
    def do_motor_off(self, args):
        """motor_on: Desactivar motores
            Ingresar sin argumentos"""
        # Comando de desactivacion de motores
    
        print("Desactivando motores...")
        res = self.compiler.desmotor("Admin")
        print(res)
        pass
    
    def do_move(self, args):
        """move: Mover el brazo a la posicion deseada
                Se le pedira ingresar las coordenadas a las que desea moverse una por una.
                Ademas, puede ingresar la velocidad lineal a la que desea moverse.
                Si ingresa velocidad 0, se movera a la velocidad media del robot."""
        # Comando de movimiento
    
        print("Comando de movimiento")
        print("Modo de coordenadas: ")
        if self.robot.mode == 0:
            print("Coordenadas absolutas")
        else:
            print("Coordenadas relativas")
        print("Ingrese las coordenadas a las que desea moverse")
        #moverse en x
        print('')
        print("Ingrese la coordenada x(a)[mm]:")
        x = input()
        #moverse en y
        print('')
        print("Ingrese la coordenada y(b)[mm]")
        y = input()
        #moverse en z
        print('')
        print("Ingrese la coordenada z(c)[mm]")
        z = input()
        #velocidad lineal
        print('')
        print("Ingrese la velocidad lineal v(d)[m/s]:")
        print("Si ingresa 0, se movera a una velocidad media")
        v = input()

        res = self.compiler.move(x,y,z,v,"Admin")
        print(res)
        pass
    
    def do_home(self, args):
        """home: Hacer homing - El robot se movera a la posicion de incial predeterminada.
                Ingresar sin argumentos"""
        # Comando de homing
        res = self.compiler.home("Admin")
        for line in res:
            print(line)
        pass
    
    def do_coord_mode(self, args):
        """coordabs: Modo coordenadas absolutas
                Se le pedira ingresar el modo de coordenadas al que desea cambiar.
                0: Coordenadas absolutas
                1: Coordenadas relativas"""
        # Comando de coordenadas absolutas
        
        print("Ingrese el modo de coordenadas al que desea cambiar")
        mode = input()
        res = self.compiler.coordenadas(mode, "Admin")
        for line in res:
            print(line)
        pass
    
    def do_grip(self, args):
        """act: Activar gripper
                Se le pedira ingresar si desea activar o desactivar el gripper.
                0: Desactivar gripper
                1: Activar gripper"""
        # Comando de activar gripper
        
        print('Ingrese la opcion que desea realizar')
        orden = input()
        orden = int(orden)
        res = self.compiler.grip(orden, "Admin")
        str(res)
        print(res)
        pass
    
    def do_report(self, args):
        """rep: Enviar reporte de mode del modo de coordenadas y posicion actual del efector final
                Ingresar sin argumentos"""
        # Comando de reporte
        res = self.compiler.report("Admin")
        for line in res:
            print(line)
        pass
    
    def do_auto(self, args):
        """auto: Modo automatico - El robot realizara la tarea que se le indique en el archivo ingresado
                Se le pedira ingresar el nombre del archivo que contiene la tarea que desea realizar
                (Evite ingresar la extension del archivo)"""
        # Comando de mode automatico
        filename = input("Ingrese el nombre del archivo: ")
        res_list = self.compiler.auto(filename, "Admin")
        for n in res_list:
            print(n)
        pass
    
    def do_learn(self, args):
        """aprender: Activar o desactivar el mode de aprendizaje
                El modo aprendizaje permite que el robot aprenda una tarea y la guarde en un archivo
                Se le pedira ingresar si desea activar o desactivar el mode de aprendizaje
                Al desactivar el mode de aprendizaje, se descarta la tarea aprendida
                Para guardar la tarea aprendida, ingrese el comando 'save_task'"""

        # Comando de generacion de tarea
        print('Si desea activar el mode de aprendizaje, ingrese 1')
        print('Si desea desactivar el mode de aprendizaje, ingrese 0')
        mode = input()
        mode = int(mode)
        self.compiler.learn_mode(mode, "Admin")
        pass

    def do_save_task(self, args):
        """save: Guardar tarea
                Se le pedira ingresar el nombre con el que desea guardar la tarea aprendida
                (Evite ingresar la extension del archivo)"""
        # Comando de guardado de tarea
        filename = input("Ingrese el nombre del archivo: ")
        res = self.compiler.save_task("Admin", filename)
        print(res)
        pass
    
    def do_EOF(self, args):
        """EOF: Cerrar el programa y el servidor
            Equivalente a presionar Ctrl + Z e Intro
            Ingresar sin argumentos"""
        print("Saliendo del programa.")
        self.compiler.end_log()
        return True  # Devuelve True para indicar que el programa debe salir.
    
    
    
        