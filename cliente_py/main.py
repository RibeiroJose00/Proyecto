import wx

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent=parent, title=title, size=(1280, 720))
        self.panel1 = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel1, style=wx.TE_MULTILINE)

        self.panel2 = wx.Panel(self.panel1, name="Server")
        self.button1 = wx.Button(self.panel2, -1, label="Log In", size=(100,-1))
        self.button2 = wx.Button(self.panel2, -1, label="Log out", size=(100,-1))

        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2.Add(self.button1, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer2.Add(self.button2, 0, wx.EXPAND|wx.ALL, 5)
        self.panel2.SetSizer(self.sizer2)

        self.panel3 = wx.Panel(self.panel1, name="Robot")
        self.button3 = wx.Button(self.panel3, -1, label="Connect", size=(100,-1))
        self.button4 = wx.Button(self.panel3, -1, label="Disconnect", size=(100,-1))

        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer3.Add(self.panel3, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer3.Add(self.button3, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer3.Add(self.button4, 0, wx.EXPAND|wx.ALL, 5)
        self.panel3.SetSizer(self.sizer3)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.panel2, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.panel3, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)

        
        self.Bind(wx.EVT_BUTTON, self.ButtonPressed)


        self.panel1.SetSizer(self.sizer)
        self.Show()

    def ButtonPressed(self, event):
        label = event.GetEventObject().GetLabel()
        self.text.AppendText(f'Button {label} pressed\n')

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, "Cliente")
    app.MainLoop()