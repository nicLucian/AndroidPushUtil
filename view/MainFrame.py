import wx


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, listctrl):
        wx.FileDropTarget.__init__(self)
        self.listctrl = listctrl

    def OnDropFiles(self, x, y, file_names):
        for file in file_names:
            tokens = str(file).split('/')
            length = len(tokens)
            pos = self.listctrl.InsertStringItem(0, tokens[length-1])
            self.listctrl.SetStringItem(pos, 1, file)


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        self.init_frame(parent, title)
        self.text_status = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.append_menus()
        self.file_listctrl = self.append_file_listctrl()
        self.devices_listctrl = self.append_devices_listctrl()
        self.lists_in_sizer = self.size_listctrls(self.file_listctrl, self.devices_listctrl)
        self.buttons_in_sizer = self.size_buttons()
        self.size_sizers()
        self.Show()

    def init_frame(self, parent, title):
        window_density = wx.DisplaySize()
        wx.Frame.__init__(self, parent, title=title,
                          size=(window_density[0], window_density[1]))

    def append_menus(self):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Input your command", "input your command")
        menu.AppendSeparator()
        menu.Append(wx.ID_ABOUT, "About", "About this program")
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "Exit", "Quit the program")
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "Menu")
        self.SetMenuBar(menu_bar)

    def append_file_listctrl(self):
        listctrl = wx.ListCtrl(self, wx.NewId(), style=wx.LC_REPORT)
        listctrl.InsertColumn(0, "FileName", width=200)
        listctrl.InsertColumn(1, "Directory", width=500)
        mfdt = FileDropTarget(listctrl)
        listctrl.SetDropTarget(mfdt)
        return listctrl

    def append_devices_listctrl(self):
        devices_list = wx.ListCtrl(self,
                                   wx.NewId(),
                                   style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        devices_list.InsertColumn(0, "DeviceName", width=200)
        return devices_list

    def size_listctrls(self, file_list_ctrl, devices_ctrl):
        listctrls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        listctrls_sizer.Add(self.file_listctrl, 2, wx.EXPAND)
        listctrls_sizer.AddSpacer(10)
        listctrls_sizer.Add(self.devices_listctrl, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        return listctrls_sizer

    def size_buttons(self):
        button_push = wx.Button(self, wx.ID_ANY, label="push")
        button_reboot = wx.Button(self, wx.ID_ANY, label="reboot")
        button_refresh = wx.Button(self, wx.ID_ANY, label="refresh devices")

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(button_push, 4, wx.EXPAND)
        buttons_sizer.AddSpacer(10)
        buttons_sizer.Add(button_reboot, 1, wx.EXPAND)
        buttons_sizer.Add(button_refresh, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        return buttons_sizer

    def size_sizers(self):
        sizers_sizer = wx.BoxSizer(wx.VERTICAL)
        sizers_sizer.Add(self.lists_in_sizer, 6, wx.EXPAND)
        sizers_sizer.AddSpacer(5)
        sizers_sizer.Add(self.buttons_in_sizer, 1, wx.EXPAND)
        sizers_sizer.AddSpacer(5)
        sizers_sizer.Add(self.text_status, 2, wx.EXPAND)
        self.SetSizer(sizers_sizer)
        self.SetAutoLayout(True)

    def get_selected_filepaths(self):

        pass

    def get_selected_devices(self):

        pass



app = wx.App(False)
frame = MainFrame(None, "Android Push Util")
app.MainLoop()
