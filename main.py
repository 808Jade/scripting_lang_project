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

def stop(event=None):
    window.quit()

window.geometry("480x640+0+0")
window.resizable(False, False)


window.bind('<Escape>', stop) # tikinter page에 가면 알 수 있다.
window.mainloop()