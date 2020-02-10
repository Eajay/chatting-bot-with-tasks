import interface
import ctypes
from tkinter import *
if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.geometry("2500x1600")
    my_name = "Smartest Guy"
    ai_name = "Machine"
    chatting_window = interface.ChatWindow(master=root, my_nick=my_name, timestamp="%H:%M:%S", ai_nick=ai_name)
    root.mainloop()
