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


########## window ##########
window = tk.Tk()
window.title("점메추")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))

window.geometry("480x640+400+300")
window.resizable(False, False)


########## Global Variables ##########


########## menu interface label ##########
def update_menu_interface(event=None):
    pass

menu_interface_label = ttk.Label(master=window, width=100)
menu_interface_label.place(x=40, y=20, anchor="center")


########## direct Input box ##########
def direct_input(event=None):
    new_text = entry.get()
    logging.info(f'new input : {new_text}')

direct_input_label = ttk.Label(master=window, text="메뉴 직접 입력하기(Enter)", font=('Consolas',12))
direct_input_label.place(x=20, y=490)

direct_input_box = tk.Frame(master=window, borderwidth=5, width=30, height=10, relief="groove")
entry = ttk.Entry(direct_input_box, font=('Consolas',15))
entry.bind('<Return>', direct_input)
entry.pack()
direct_input_box.place(x=20, y=510)


########## date label ##########
today = datetime.today().strftime("%Y년 %m월 %d일(%a)")
todays_date_label = ttk.Label(master=window, text=today, font=('Consolas', 20))
todays_date_label.place(x=20,y=570)


########## Calendar button ##########
class CalendarButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.image = tk.PhotoImage(file='calendar_icon.png')
        self.image = self.image.subsample(4,4)
        self['image'] = self.image
        self['bg'] = "#F0F0F0"
        self['cursor'] = 'right_side'
        self['borderwidth'] = 0
        self['highlightthickness'] = 0
        self['command'] = self.clicked
        self.place(x=330, y=490)

    def clicked(self):
        logging.info(f'calendar button clicked')




########## 아/점/저 Radiobutton ##########
class BreakfastButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.image = tk.PhotoImage(file='breakfast_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.place(x=95, y=370)
        self['command'] = self.clicked

    def clicked(self):
        logging.info('breakfast_button_clicked')
        BLD_index.change('breakfast')
        recommend_button.update_text(BLD_index.index)
        self.image = tk.PhotoImage(file='breakfast_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()

        lunch_button.off()
        dinner_button.off()

    def off(self):
        self.image = tk.PhotoImage(file='breakfast_icon_b.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()


class LunchButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.image = tk.PhotoImage(file='lunch_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.place(x=195, y=370)
        self['command'] = self.clicked

    def clicked(self):
        logging.info('Lunch_button_clicked')
        BLD_index.change('lunch')
        recommend_button.update_text(BLD_index.index)
        self.image = tk.PhotoImage(file='lunch_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()

        dinner_button.off()
        breakfast_button.off()

    def off(self):
        self.image = tk.PhotoImage(file='lunch_icon_b.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()


class DinnerButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.image = tk.PhotoImage(file='dinner_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.place(x=295, y=370)
        self['command'] = self.clicked

    def clicked(self):
        logging.info('Dinner_button_clicked')
        BLD_index.change('dinner')
        recommend_button.update_text(BLD_index.index)
        self.image = tk.PhotoImage(file='dinner_icon.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()

        lunch_button.off()
        breakfast_button.off()

    def off(self):
        self.image = tk.PhotoImage(file='dinner_icon_b.png')
        self.image = self.image.subsample(6, 6)
        self['image'] = self.image
        self.update()


########## BLD index ##########
class BLDIndex():
    def __init__(self):
        current_time = datetime.now().time()
        hour = current_time.hour

        if 6 <= hour < 11:
            self.index = "breakfast"
        elif 11 <= hour < 17:
            self.index = "lunch"
        else:
            self.index = "dinner"

    def change(self, s):
        self.index = s
        logging.info(f'BLD_index changed - {self.index}')




########## recommend button ##########
class RecommendButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.init_recommendation()  # 초기 텍스트 업데이트
        self.place(x=240, y=320, anchor="center")
        self['width'] = 30
        self['padding'] = 20
        self['command'] = self.clicked

    def init_recommendation(self):
        now = datetime.now().time()
        hour = now.hour
        if 6 <= hour < 11:
            self.config(text="아침 추천 받기!")
        elif 11 <= hour < 17:
            self.config(text="점심 추천 받기!")
        else:
            self.config(text="저녁 추천 받기!")

    def update_text(self, s):
        if s == "breakfast":
            self.config(text="아침 추천 받기!")
        elif s == "lunch":
            self.config(text="점심 추천 받기!")
        else:
            self.config(text="저녁 추천 받기!")
        self.update()

    def clicked(self):
        logging.info(f'recommend button clicked')


########## main ##########
BLD_index = BLDIndex()
recommend_button = RecommendButton()
calendar_button = CalendarButton()

breakfast_button = BreakfastButton()
lunch_button = LunchButton()
dinner_button = DinnerButton()

window.bind('<Escape>', lambda event: window.quit())
window.mainloop()