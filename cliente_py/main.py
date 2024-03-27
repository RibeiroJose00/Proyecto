import wx
import wx.media
from client import Client

class MainFrame(wx.Frame):
    def __init__(self, parent, title, client):
        super(MainFrame, self).__init__(parent=parent, title=title, size=(1280, 720))
        # Crear panel principal
        self.panel_ppal = wx.Panel(self)

        # Crear panel de servidor
        self.panel_server = wx.Panel(self.panel_ppal, name="Server")

        self.button1 = wx.Button(self.panel_server, -1, label="Log In", size=(100,-1))
        self.button2 = wx.Button(self.panel_server, -1, label="Log out", size=(100,-1))

        self.sizer_server = wx.BoxSizer(wx.VERTICAL)
        self.sizer_server.Add(self.button1, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_server.Add(self.button2, 0, wx.EXPAND|wx.ALL, 5)
        self.panel_server.SetSizer(self.sizer_server)

        # Crear panel de robot
        self.panel_robot = wx.Panel(self.panel_ppal, name="Robot")

        self.button3 = wx.Button(self.panel_robot, -1, label="Connect", size=(100,-1))
        self.button4 = wx.Button(self.panel_robot, -1, label="Disconnect", size=(100,-1))

        self.sizer_robot = wx.BoxSizer(wx.VERTICAL)
        self.sizer_robot.Add(self.button3, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_robot.Add(self.button4, 0, wx.EXPAND|wx.ALL, 5)
        self.panel_robot.SetSizer(self.sizer_robot)

            # Creamos un sub_sizer para los paneles server y robot
        self.sizer_RSMedia = wx.BoxSizer(wx.VERTICAL)
        self.sizer_RSMedia.Add(self.panel_server, 16, wx.EXPAND|wx.ALL, 5)
        self.sizer_RSMedia.Add(self.panel_robot, 16, wx.EXPAND|wx.ALL, 5)

        # Crear panel de comandos
        self.panel_command = wx.Panel(self.panel_ppal, name="Commands")

        self.button5 = wx.Button(self.panel_command, -1, label="Motor: ON", size=(100,-1))
        self.button6 = wx.Button(self.panel_command, -1, label="Motor: OFF", size=(100,-1))

        self.sizer_motor = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_motor.Add(self.button5, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_motor.Add(self.button6, 0, wx.EXPAND|wx.ALL, 5)

        self.button8 = wx.Button(self.panel_command, -1, label="Grip: ON", size=(100,-1))
        self.button9 = wx.Button(self.panel_command, -1, label="Grip: OFF", size=(100,-1))

        self.sizer_grip = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_grip.Add(self.button8, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_grip.Add(self.button9, 0, wx.EXPAND|wx.ALL, 5)

        self.button10 = wx.Button(self.panel_command, -1, label="Absolute", size=(100,-1))
        self.button11 = wx.Button(self.panel_command, -1, label="Relative", size=(100,-1))

        self.sizer_coord = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_coord.Add(self.button10, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_coord.Add(self.button11, 0, wx.EXPAND|wx.ALL, 5)

        self.button12 = wx.Button(self.panel_command, -1, label="Learn mode: ON", size=(100,-1))
        self.button13 = wx.Button(self.panel_command, -1, label="Learn mode: OFF", size=(100,-1))

        self.sizer_learn = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_learn.Add(self.button12, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_learn.Add(self.button13, 0, wx.EXPAND|wx.ALL, 5)

        self.text_console = wx.TextCtrl(self.panel_command, style=wx.TE_READONLY|wx.TE_MULTILINE)

            # Comando mover
        self.text1 = wx.TextCtrl(self.panel_command, name='x', size=(30,-1))
        self.text2 = wx.TextCtrl(self.panel_command, name='y', size=(30,-1))
        self.text3 = wx.TextCtrl(self.panel_command, name='z', size=(30,-1))
        self.text4 = wx.TextCtrl(self.panel_command, name='v', size=(30,-1))
        self.button7 = wx.Button(self.panel_command, -1, label="Home", size=(100,-1))
        self.button14 = wx.Button(self.panel_command, -1, label="Send", size=(100,-1))

        self.text1.SetHint("x")
        self.text2.SetHint("y")
        self.text3.SetHint("z")
        self.text4.SetHint("v")

        self.sizer_move = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_move.Add(self.text1, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_move.Add(self.text2, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_move.Add(self.text3, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_move.Add(self.text4, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer_move.Add(self.button14, 0, wx.EXPAND|wx.ALL, 5)

        self.sizer_command = wx.BoxSizer(wx.VERTICAL)
        self.sizer_command.Add(self.sizer_motor, 0, 5)
        self.sizer_command.Add(self.sizer_grip, 0, 5)
        self.sizer_command.Add(self.sizer_coord, 0, 5)
        self.sizer_command.Add(self.sizer_learn, 0, 5)
        self.sizer_command.Add(self.button7, 0, 5)
        self.sizer_command.Add(self.sizer_move, 0, 5)
        self.sizer_command.Add(self.text_console, 1, wx.EXPAND|wx.ALL, 5)
        self.panel_command.SetSizer(self.sizer_command)

        # Ventana de streaming
        self.panel_media = wx.Panel(self.panel_ppal, name="Streaming")
        self.media_ctrl = wx.media.MediaCtrl(self.panel_media)

        self.sizer_RSMedia.Add(self.panel_media, 66, wx.EXPAND|wx.ALL, 5)

        # Crear sizer principal
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer_RSMedia, 1, wx.EXPAND|wx.ALL, 5)
        # self.sizer.Add(self.panel_server, 1, wx.EXPAND|wx.ALL, 5)
        # self.sizer.Add(self.panel_robot, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.panel_command, 1, wx.EXPAND|wx.ALL, 5)

        # Vinculamos los botones del apartado Server
        self.Bind(wx.EVT_BUTTON, self.ServerButton, self.button1)
        self.Bind(wx.EVT_BUTTON, self.ServerButton, self.button2)

        # Vinculamos los botones del apartado Robot
        self.Bind(wx.EVT_BUTTON, self.RobotButton, self.button3)
        self.Bind(wx.EVT_BUTTON, self.RobotButton, self.button4)

        # Vinculamos los botones del apartado Commands
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button5)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button6)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button8)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button9)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button10)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button11)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button12)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button13)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button14)
        self.Bind(wx.EVT_BUTTON, self.CommandButton, self.button7)

        # Organizar el sizer principal
        self.panel_ppal.SetSizer(self.sizer)
        self.Show()

    def ServerButton(self, event):
        label = event.GetEventObject().GetLabel()
        self.text_console.AppendText(f'<< Button {label} pressed\n')
        if label == "Log In":
            res = client.connect(1)
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Log out":
            res = client.disconnect()
            self.text_console.AppendText(f'>> {res}\n')
            pass
    
    def RobotButton(self, event):
        label = event.GetEventObject().GetLabel()
        self.text_console.AppendText(f'<< Button {label} pressed\n')
        if label == "Connect":
            res = client.connect_robot()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Disconnect":
            res = client.disconnect_robot()
            self.text_console.AppendText(f'>> {res}\n')
            pass

    def CommandButton(self, event):
        label = event.GetEventObject().GetLabel()
        self.text_console.AppendText(f'<< Button {label} pressed\n')
        if label == "Motor: ON":
            res = client.act_motor()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Motor: OFF":
            res = client.des_motor()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Grip: ON":
            res = client.act_grip()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Grip: OFF":
            res = client.des_grip()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Absolute":
            res = client.coord_mode(0)
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Relative":
            res = client.coord_mode(1)
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Learn mode: ON":
            res = client.learn(1)
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Learn mode: OFF":
            res = client.learn(0)
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Home":
            res = client.home()
            self.text_console.AppendText(f'>> {res}\n')
            pass
        elif label == "Send":
            x = self.text1.GetValue()
            y = self.text2.GetValue()
            z = self.text3.GetValue()
            v = self.text4.GetValue()
            self.text_console.AppendText(f'<< x= {x}, y= {y}, z= {z}, v= {v}\n')
            res = client.move(x, y, z, v)
            self.text_console.AppendText(f'>> {res}\n')
            self.text1.Clear()
            self.text2.Clear()
            self.text3.Clear()
            self.text4.Clear()
            pass


if __name__ == '__main__':
    app = wx.App()
    client = Client("localhost", 8000)
    frame = MainFrame(None, "Cliente", client)
    app.MainLoop()