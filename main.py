import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from logging import info as info, debug as debug, warning as warning

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

window = tk.Tk()
window.title("점메추")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))


window.geometry("480x640+400+300")
window.resizable(False, False)

########## menu interface label ##########
def update_menu_interface(event=None):
    pass

menu_interface_label = ttk.Label(master=window, width=100)
menu_interface_label.place(x=40,y=20,anchor="center")

########## recommend button ##########
def recommend(event=None):
    logging.info(f'recommend button clicked')

recommend_button = ttk.Button(master=window, text="추천 받기!", width=30, padding=20, command=recommend)
recommend_button.place(x=240, y=320, anchor="center")


########## direct Input box ##########
def direct_input(event=None):
    new_text = entry.get()
    logging.info(f'new input : {new_text}')

direct_input_label = ttk.Label(master=window, text="메뉴 직접 입력하기(Enter)", font=('Consolas',12))
direct_input_label.place(x=20,y=490)

direct_input_box = tk.Frame(master=window, borderwidth=5, width=30, height=10, relief="groove")
entry = ttk.Entry(direct_input_box, font=('Consolas',15))
entry.bind('<Return>', direct_input)
entry.pack()
direct_input_box.place(x=20,y=510)


########## date label ##########
today = datetime.today().strftime("%Y년 %m월 %d일(%a)")
todays_date_label = ttk.Label(master=window, text=today, font=('Consolas', 20))
todays_date_label.place(x=20,y=570)

########## Calendar button ##########
def move_to_calendar(event=None):
    logging.info(f'calendar button clicked')

calendar_image = tk.PhotoImage(file='calendar_icon.png')
calendar_image = calendar_image.subsample(4, 4)

calendar_button = tk.Button(master=window, image=calendar_image, command=move_to_calendar, bg="#F0F0F0", cursor='right_side',borderwidth=0, highlightthickness=0)
calendar_button.place(x=330, y=490)

########## 아/점/저 Radiobutton ##########


window.bind('<Escape>', window.quit())
window.mainloop()