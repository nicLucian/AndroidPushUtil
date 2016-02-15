#coding utf8
import wx
import sys

from handler.PushHandler import PushHandler
from handler.RebootHandler import RebootHandler
from handler.RefreshHandler import RefreshHandler

reload(sys)
sys.setdefaultencoding("utf-8")

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, listctrl, frame):
        wx.FileDropTarget.__init__(self)
        self.listctrl = listctrl
        self.frame = frame
        self.files_existed = []

    def OnDropFiles(self, x, y, file_names):
        for file in file_names:
            if file not in self.files_existed:
                tokens = str(file).decode('utf-8', 'ignore').split('/')
                length = len(tokens)
                file_name = tokens[length-1]
                if file_name.endswith(".apk"):
                    pos = self.listctrl.InsertStringItem(0, file_name)
                    self.listctrl.SetStringItem(pos, 1, file)
                    self.files_existed.append(file)
                else:
                    errorDlg = wx.MessageDialog(self.frame, "you can only push apks", "Hint", wx.OK)
                    errorDlg.ShowModal()


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
        mfdt = FileDropTarget(listctrl, self)
        listctrl.SetDropTarget(mfdt)
        return listctrl

    def append_devices_listctrl(self):
        devices_list = wx.ListCtrl(self,
                                   wx.NewId(),
                                   style=wx.LC_REPORT)
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
        button_delete = wx.Button(self, wx.ID_ANY, label="remove")

        self.Bind(wx.EVT_BUTTON, self.onPush, button_push)
        self.Bind(wx.EVT_BUTTON, self.onReboot, button_reboot)
        self.Bind(wx.EVT_BUTTON, self.onRefresh, button_refresh)
        self.Bind(wx.EVT_BUTTON, self.onDelete, button_delete)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(button_push, 2, wx.EXPAND)
        buttons_sizer.Add(button_delete, 2, wx.EXPAND)
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

    def onPush(self, event):
        push_handler = PushHandler(self)
        push_handler.exec_command(self)

    def onReboot(self, event):
        handler = RebootHandler(self)
        handler.exec_command(self)

    def onDelete(self, event):
        ids = self._get_selected_items_id(self.file_listctrl)
        if len(ids) <= 0:
            errorDlg = wx.MessageDialog(self, "you have not chosen any file yet", "Hint", wx.OK)
            errorDlg.ShowModal()
        for id in ids:
            self.file_listctrl.DeleteItem(id)

    def onRefresh(self, event):
        self.devices_listctrl.DeleteAllItems()
        handler = RefreshHandler()
        handler.exec_command(self)

    def get_selected_filepaths(self):
        selected_files = self._get_selected_items(self.file_listctrl, 1)
        return selected_files

    def get_selected_devices(self):
        devices = self._get_selected_items(self.devices_listctrl)
        return devices

    def show_dialog(self, message, title):
        errorDlg = wx.MessageDialog(self, message, title, wx.OK)
        errorDlg.ShowModal()


    def _get_selected_items_id(self, listctlr):
        ids = []
        lastFound = -1
        while True:
            index = listctlr.GetNextItem(
                lastFound,
                wx.LIST_NEXT_ALL,
                wx.LIST_STATE_SELECTED,
            )
            if index == -1:
                break
            else:
                lastFound = index
                ids.append(index)
        return ids

    def _get_selected_items(self, listctlr, column_id = 0):
        items = []
        ids = self._get_selected_items_id(listctlr)
        for id in ids:
            items.append(listctlr.GetItem(id, column_id).GetText())
        return items

    def set_status(self, message):
        for x in message:
            self.text_status.AppendText(str(x))

    def add_device(self, device_name):
        self.devices_listctrl.InsertStringItem(0, device_name)
        pass


app = wx.App(False)
frame = MainFrame(None, "Android Push Util")
app.MainLoop()
