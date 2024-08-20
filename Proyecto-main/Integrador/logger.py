import time
import os

class Logger():
    def __init__(self):
        self.server_init = time.time()
        self.server_end = 0
        self.connect_init = 0
        self.order_list = []
        self.answer_list = []
        self.time_list = []
        self.n_order = 0
        self.n_conecction = 0
        self.n_report = 0
        pass
        
    def log_init(self):
        format_server_init = self.format_time(self.server_init)
        with open("log.txt", 'w') as log:
            log.write("Log del servidor" + '\n')
            log.write(format_server_init + " : Inicio Servidor" + '\n')
        pass
    
    def log_end(self):
        self.server_end = time.time()
        format_server_end = self.format_time(self.server_end)
        with open("log.txt", 'a') as log:
            log.write('\n' + format_server_end + " : Fin Servidor")
        with open("G_task.txt", 'w') as task:
            #borramos g_task
            task.write("")
        pass
    
    def get_log(self):
        log_list = self.read_file("log.txt")
        return log_list

    def register(self, aprender, order, answer):
        self.n_order += 1
        if order == "Conectar":
            self.connect_init = time.time()
            self.n_conecction = self.n_order
        order_time = self.format_time(time.time())
        self.time_list.append(order_time)
        self.order_list.append(order)
        self.answer_list.append(answer)
        
        if type(answer) == list:
            with open("log.txt", 'a') as log:
                for n in answer:
                    log.write('\n' + order_time + " : " + order + ' : ' + n)
        else: 
            with open("log.txt", 'a') as log:
                log.write('\n' + order_time + " : " + order + ' : ' + answer)
        
        if aprender == 1:
            self.task()
        pass
    
    def task(self):
        with open("G_task.txt", 'a') as file:
            n = self.n_order - 1
            if self.order_list[n][0] == "M" or self.order_list[n][0] == "G":
                file.write(self.order_list[n] + '\n')
            else:
                pass
        pass
    
    def save_task(self, filename):
        os.rename("G_task.txt", str(filename) + ".txt")
        res = 'Guardado exitoso'
        return res
    
    def get_task(self, filename):
        with open(filename, 'r') as file:
            task_list = file.readlines()
        return task_list

    def read_file(self, filename):
        path = os.getcwd() + "\\" + filename
        line_list = []
        #Se abre el archivo
        with open(path, 'r') as file:
            #Se lee linea por linea
            for line in file:
                #Se agrega la linea a la lista
                line_list.append(line)
        #Se cierra el archivo
        file.close()
        return line_list
    
    def report(self, connect_status, robot_posicion):
        #Tiempo de conexion
        self.n_report += 1
        format_connect_init = self.format_time(self.connect_init)
        #Se abre el archivo
        name = "report" + str(self.n_report) + ".txt"
        with open(name, 'w') as report:
        #Se escribe el reporte
            if connect_status == 0:
                report.write("El robot esta desconectado" + '\n')
                report.write("Posicion del robot: " + robot_posicion + '\n')
                report.write("Actividad: En espera" + '\n')
                report.write("Inicio de la ultima conexion: " + format_connect_init + '\n')
                report.write("Lista de ordenes:" + '\n')
                for n in range(self.n_conecction, self.n_order):
                    report.write('comando: ' + self.order_list[n] + '\n' + 'respuesta: ' + self.answer_list[n] + '\n')
                pass
            elif connect_status == 1:
                report.write("El robot esta conectado" + '\n')
                report.write("Posicion del robot: " + robot_posicion + '\n')
                report.write("Actividad: " + self.order_list[self.n_order - 1] +  '\n')
                report.write("Inicio de conexion: " + format_connect_init + '\n')
                report.write("Lista de ordenes:" + '\n')
                for n in range(self.n_conecction, self.n_order):
                    report.write('com: ' + self.order_list[n] + '\n')
                    report.write('res: ' + self.answer_list[n] + '\n')
                pass
        report_list = self.read_file(name)
        return report_list
        
    def format_time(self, p_time):
        struct_time = time.localtime(p_time)
        format = "%H:%M:%S"
        format_time = time.strftime(format, struct_time)
        return format_time