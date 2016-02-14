import wx


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, listctrl):
        wx.FileDropTarget.__init__(self)
        self.listctrl = listctrl

    def OnDropFiles(self, x, y, file_names):
        for file in file_names:
            pos = self.listctrl.InsertStringItem(0, file)
            self.listctrl.SetStringItem(pos, 1, file)


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        self.init_frame(parent, title)
        self.append_menus()
        self.append_listctrl()
        self.Show()

    def init_frame(self, parent, title):
        window_density = wx.DisplaySize()
        wx.Frame.__init__(self, parent, title=title,
                          size=(window_density[0], window_density[1]))

    def append_menus(self):
        self.menu = wx.Menu()
        self.menu.Append(wx.ID_ANY, "Input your command", "input your command")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_ABOUT, "About", "About this program")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, "Exit", "Quit the program")
        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu, "Menu")
        self.SetMenuBar(self.menu_bar)

    def append_listctrl(self):
        self.listctrl = wx.ListCtrl(self, wx.NewId(), style=wx.LC_REPORT)
        self.listctrl.InsertColumn(0, "FileName")
        self.listctrl.InsertColumn(1, "Directory")
        self.mfdt = FileDropTarget(self.listctrl)
        self.listctrl.SetDropTarget(self.mfdt)




app = wx.App(False)
frame = MainFrame(None, "Android Push Util")
app.MainLoop()
