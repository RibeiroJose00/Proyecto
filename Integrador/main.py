from interfaz import Interfaz

def main():
    print("Bienvenido al programa de control de robots")
    print("Por favor, si encuentra el robot ocupado, sea paciente y espere a que sea desocupado")
    cli = Interfaz()
    cli.cmdloop()
    
main()
    