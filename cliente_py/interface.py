from cmd import Cmd
from client import Client

class Interface(Cmd):
    def __init__(self, host, port):
        super().__init__()
        self.client = Client(host, port)

    def do_move(self, args):
        x, y, z, speed = map(float, args.split())
        self.client.move(x, y, z, speed)

    def do_quit(self, args):
        return True

    def do_exit(self, args):
        return True

    def do_EOF(self, args):
        return True

    def emptyline(self):
        pass

    def postcmd(self, stop, line):
        print('Command executed')
        return stop

    def postloop(self):
        print('Goodbye!')