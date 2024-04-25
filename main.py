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
def init_bld_index():
    current_time = datetime.now().time()
    hour = current_time.hour

    if 6 <= hour < 11:
        return 1  # 아침 시간
    elif 11 <= hour < 17:
        return 2  # 점심 시간
    else:
        return 3  # 저녁 시간

BLD_index = init_bld_index()

def breakfast_button_clicked(event=None):
    global BLD_index
    BLD_index = 1
    logging.info(f'breakfast_button_clicked / index - {BLD_index}')

breakfast_image = tk.PhotoImage(file='breakfast_icon.png')
breakfast_image = breakfast_image.subsample(6,6)
breakfast_button = tk.Button(master=window, image=breakfast_image, command=breakfast_button_clicked)
breakfast_button.place(x=95,y=370)

def lunch_button_clicked(event=None):
    global BLD_index
    BLD_index = 2
    logging.info(f'lunch_button_clicked / index - {BLD_index}')

lunch_image = tk.PhotoImage(file='lunch_icon.png')
lunch_image = lunch_image.subsample(6,6)
lunch_button = tk.Button(master=window, image=lunch_image, command=lunch_button_clicked)
lunch_button.place(x=195,y=370)

def dinner_button_clicked(event=None):
    global BLD_index
    BLD_index = 3
    logging.info(f'dinner_button_clicked / index - {BLD_index}')

dinner_image = tk.PhotoImage(file='dinner_icon.png')
dinner_image = dinner_image.subsample(6,6)
dinner_button = tk.Button(master=window, image=dinner_image, command=dinner_button_clicked)
dinner_button.place(x=295,y=370)


window.bind('<Escape>', lambda event: window.quit())
window.mainloop()