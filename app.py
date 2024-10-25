from os import read
import threading
import wx
import wx.adv
import morse

TRAY_TOOLTIP = "Morse Input"
TRAY_ICON = "icon.ico"


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)

    return item


def start_morse(_, stop_f):
    print("thread start")
    morse.main(stop_f)
    print("thread end")


def serial_through(_, stop_f):
    print("through start")
    import serial
    with serial.Serial(morse.com, morse.bitrate, timeout=0.1) as ser:
        while stop_f():
            ser.read()
    print("through end")


class TaskBarIcon(wx.adv.TaskBarIcon):
    stop_f = [False, False]
    thread_f = False
    thread = None

    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_start_morse)
        self.thread = threading.Thread(
            target=start_morse, args=(None, lambda: self.stop_f[0]))
        self.thread.setDaemon(True)
        self.thread.start()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, "Morse start", self.on_start_morse)
        create_menu_item(menu, "Morse end", self.on_end_morse)
        menu.AppendSeparator()
        create_menu_item(menu, "Exit", self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_start_morse(self, event):
        if self.thread_f == False:
            return 0
        self.thread_f = False
        self.stop_f = [False, False]
        self.thread.join()
        self.thread = threading.Thread(
            target=start_morse, args=(None, lambda: self.stop_f[0]))
        self.thread.setDaemon(True)
        self.thread.start()

    def on_end_morse(self, event):
        if self.thread_f == True:
            return 0
        self.thread_f = True
        self.stop_f = [True, True]
        self.thread.join()
        self.thread = threading.Thread(
            target=serial_through, args=(None, lambda: self.stop_f[1]))
        self.thread.start()

    def on_exit(self, event):
        print("exit")
        self.stop_f = [True, False]
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)

        print("Launch App")
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
