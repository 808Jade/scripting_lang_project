import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from logging import info as info, debug as debug, warning as warning

from tkinter import*
from tkinter.ttk import*
from tkinter.scrolledtext import ScrolledText

window = Tk()
window.title("점메추")
window.iconphoto(True, PhotoImage(file="icon.png"))


window.geometry("480x640+400+300")
window.resizable(False, False)


menu_interface = Frame(master=window)
menu_interface.pack()


window.bind('<Escape>', window.quit())
window.mainloop()