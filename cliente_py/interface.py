### Sin usar

import wx
import wx.media

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent=parent, title=title, size=(1280, 720))
        # Crear panel principal
        self.panel1 = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel1, style=wx.TE_MULTILINE)

        # Crear panel de servidor
        self.panel2 = wx.Panel(self.panel1, name="Server")
        self.button1 = wx.Button(self.panel2, -1, label="Log In", size=(100,-1))
        self.button2 = wx.Button(self.panel2, -1, label="Log out", size=(100,-1))

        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2.Add(self.button1, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer2.Add(self.button2, 0, wx.EXPAND|wx.ALL, 5)
        self.panel2.SetSizer(self.sizer2)

        # Crear panel de robot
        self.panel3 = wx.Panel(self.panel1, name="Robot")
        self.button3 = wx.Button(self.panel3, -1, label="Connect", size=(100,-1))
        self.button4 = wx.Button(self.panel3, -1, label="Disconnect", size=(100,-1))

        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer3.Add(self.button3, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer3.Add(self.button4, 0, wx.EXPAND|wx.ALL, 5)
        self.panel3.SetSizer(self.sizer3)

            # Creamos un sub_sizer para los paneles server y robot
        self.sub_sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer1.Add(self.panel2, 16, wx.EXPAND|wx.ALL, 5)
        self.sub_sizer1.Add(self.panel3, 16, wx.EXPAND|wx.ALL, 5)

        # Crear panel de comandos
        self.panel4 = wx.Panel(self.panel1, name="Commands")
        self.button5 = wx.Button(self.panel4, -1, label="Motor: ON", size=(100,-1))
        self.button6 = wx.Button(self.panel4, -1, label="Motor: OFF", size=(100,-1))
        self.button7 = wx.Button(self.panel4, -1, label="Home", size=(100,-1))
        self.button8 = wx.Button(self.panel4, -1, label="Grip: ON", size=(100,-1))
        self.button9 = wx.Button(self.panel4, -1, label="Grip: OFF", size=(100,-1))
        self.button10 = wx.Button(self.panel4, -1, label="Absolute", size=(100,-1))
        self.button11 = wx.Button(self.panel4, -1, label="Relative", size=(100,-1))
        self.button12 = wx.Button(self.panel4, -1, label="Learn mode: ON", size=(100,-1))
        self.button13 = wx.Button(self.panel4, -1, label="Learn mode: OFF", size=(100,-1))


            # Comando mover
        self.text1 = wx.TextCtrl(self.panel4, name='x', size=(20,-1))
        self.text2 = wx.TextCtrl(self.panel4, name='y', size=(20,-1))
        self.text3 = wx.TextCtrl(self.panel4, name='z', size=(20,-1))
        self.text4 = wx.TextCtrl(self.panel4, name='v', size=(20,-1))
        self.button14 = wx.Button(self.panel4, -1, label="Send", size=(100,-1))

        self.text1.SetHint("x")
        self.text2.SetHint("y")
        self.text3.SetHint("z")
        self.text4.SetHint("v")

        self.sub_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer2.Add(self.text1, 0, wx.EXPAND|wx.ALL, 5)
        self.sub_sizer2.Add(self.text2, 0, wx.EXPAND|wx.ALL, 5)
        self.sub_sizer2.Add(self.text3, 0, wx.EXPAND|wx.ALL, 5)
        self.sub_sizer2.Add(self.text4, 0, wx.EXPAND|wx.ALL, 5)
        self.sub_sizer2.Add(self.button14, 0, wx.EXPAND|wx.ALL, 5)

        self.sizer4 = wx.BoxSizer(wx.VERTICAL)
        self.sizer4.Add(self.button5, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button6, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button7, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button8, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button9, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button10, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button11, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button12, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.button13, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer4.Add(self.sub_sizer2, 0, wx.EXPAND|wx.ALL, 5)
        self.panel4.SetSizer(self.sizer4)

        # Ventana de streaming
        self.panel5 = wx.Panel(self.panel1, name="Streaming")
        self.media_ctrl = wx.media.MediaCtrl(self.panel5)

        self.sub_sizer1.Add(self.panel5, 66, wx.EXPAND|wx.ALL, 5)




        # Crear sizer principal
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sub_sizer1, 1, wx.EXPAND|wx.ALL, 5)
        # self.sizer.Add(self.panel2, 1, wx.EXPAND|wx.ALL, 5)
        # self.sizer.Add(self.panel3, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.panel4, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)


        
        self.Bind(wx.EVT_BUTTON, self.ButtonPressed)


        self.panel1.SetSizer(self.sizer)
        self.Show()

    def ButtonPressed(self, event):
        label = event.GetEventObject().GetLabel()
        self.text.AppendText(f'Button {label} pressed\n')
        if label == "Log In":
            self.media_ctrl.Load('http://path/to/streaming/video')
            self.media_ctrl.Play()
            pass
