import calendar
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from logging import info as info, debug as debug, warning as warning

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import random
import requests
import json

########## Global Variables ##########

maker_name = ""
food_name = "f"
current_kcal = 3
current_carbohydrate = 3
current_protein = 3
current_fat = 3

global_rgb = ""

# [일, 시간, rgb]
global_data = []

arr = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# 초기 설정
def direct_food_founder(string):
    base_url = "http://openapi.foodsafetykorea.go.kr/api/sample/I2790/json/"
    start_node = 1
    node_limit = 1000
    found_food = False

    while not found_food:
        if start_node > 12500:
            messagebox.showinfo("검색 실패","검색하신 음식이 없습니다.")
            break

        url = f"{base_url}{start_node}/{start_node + node_limit - 1}/DESC_KOR={string}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'RESULT' in data and data['RESULT']['CODE'] == 'INFO-200':
                print("더 이상 데이터가 없습니다.")
                break

            # 'row' 키가 있는지 확인하여 데이터가 있는지 확인
            if 'row' in data['I2790']:
                foods = data['I2790']['row']
                for food in foods:
                    if food['DESC_KOR'] == string:
                        print("찾은 음식:", food)
                        found_food = True

                        global food_name, current_kcal, current_carbohydrate, current_protein, current_fat, maker_name
                        food_name = food['DESC_KOR']
                        if food['MAKER_NAME'] == '':
                            maker_name = ""
                        else:
                            maker_name = food['MAKER_NAME']
                        if food['NUTR_CONT1'] == '':
                            current_kcal = 0
                        else:
                            current_kcal = round(float(food['NUTR_CONT1']))
                        if food['NUTR_CONT2'] == '':
                            current_carbohydrate = 0
                        else:
                            current_carbohydrate = round(float(food['NUTR_CONT2']))
                        if food['NUTR_CONT3'] == '':
                            current_protein = 0
                        else:
                            current_protein = round(float(food['NUTR_CONT3']))
                        if food['NUTR_CONT4'] == '':
                            current_fat = 0
                        else:
                            current_fat = round(float(food['NUTR_CONT4']))

                        nutrient_label.init_current_nutrient()
                        menu_interface_button.insert_new_text()
                        color_label.set_color()
                        break
        else:
            print("API에 액세스하는 데 문제가 발생했습니다. 상태 코드:", response.status_code)

        # 다음 요청을 위해 시작 노드 업데이트
        start_node += node_limit


def food_founder():
    global data_node
    data_node = "D" + str(random.randint(0, 3000)).zfill(6)

    base_url = "http://openapi.foodsafetykorea.go.kr/api/sample/I2790/json/"
    food_cd = data_node
    start_node = 1
    node_limit = 1000
    found_food = False

    while not found_food:
        if start_node > 12500:
            data_node = "D" + str(random.randint(0, 3000)).zfill(6)
            food_cd = data_node
            print("검색 결과 존재하지 않는 food_cd입니다. 재검색합니다.")
        # 요청 URL 설정
        url = f"{base_url}{start_node}/{start_node + node_limit - 1}/FOOD_CD={food_cd}"


        response = requests.get(url) # HTTP GET 요청 보내기
        if response.status_code == 200: # 성공적인 응답 처리
            data = response.json()

            if 'RESULT' in data and data['RESULT']['CODE'] == 'INFO-200':
                print("더 이상 데이터가 없습니다.")
                break

            # 'row' 키가 있는지 확인하여 데이터가 있는지 확인
            if 'row' in data['I2790']:
                foods = data['I2790']['row']
                for food in foods:
                    if food['FOOD_CD'] == food_cd:
                        # 원하는 음식을 찾았으므로 결과 출력
                        print("찾은 음식:", food)
                        found_food = True

                        global food_name, current_kcal, current_carbohydrate, current_protein, current_fat, maker_name
                        food_name = food['DESC_KOR']
                        if food['MAKER_NAME'] == '':
                            maker_name = ""
                        else:
                            maker_name = food['MAKER_NAME']
                        if food['NUTR_CONT1'] == '':
                            current_kcal = 0
                        else:
                            current_kcal = round(float(food['NUTR_CONT1']))
                        if food['NUTR_CONT2'] == '':
                            current_carbohydrate = 0
                        else:
                            current_carbohydrate = round(float(food['NUTR_CONT2']))
                        if food['NUTR_CONT3'] == '':
                            current_protein = 0
                        else:
                            current_protein = round(float(food['NUTR_CONT3']))
                        if food['NUTR_CONT4'] == '':
                            current_fat = 0
                        else:
                            current_fat = round(float(food['NUTR_CONT4']))

                        nutrient_label.init_current_nutrient()
                        menu_interface_button.insert_new_text()
                        color_label.set_color()
                        break
        else:
            print("API에 액세스하는 데 문제가 발생했습니다. 상태 코드:", response.status_code)

        # 다음 요청을 위해 시작 노드 업데이트
        start_node += node_limit


########## window ##########
window = tk.Tk()
window.title("점메추")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))

window.geometry("480x640+400+300")
window.resizable(False, False)




########## menu interface button ##########
class MenuInterfaceButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.config(text="식품 이름")
        self['width'] = 50
        self['height'] = 6
        self.place(x=60, y=20)
        self['command'] = self.clicked

    def insert_new_text(self):
        if maker_name == "":
            self.config(text=f"{food_name}")
        else:
            self.config(text=f"[{maker_name}] {food_name}")

        self.update()

    def clicked(self):
        global  rgb1, rgb2, rgb3

        if BLD_index.index == "breakfast":
            rgb1 = global_rgb
        elif BLD_index.index == "lunch":
            rgb2 = global_rgb
        elif BLD_index.index == "dinner":
            rgb3 = global_rgb

        logging.info(f'Interface button clicked')
        logging.info(f'{rgb1}, {rgb2}, {rgb3}')

        # 현재 날짜와 시간 가져오기
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        food_info = {"date": date_time, "time": BLD_index.index, "food": food_name, "RGB": global_rgb}

        # JSON 파일에 데이터 추가
        with open("JMC_log.json", "a") as f:
            json.dump(food_info, f)
            f.write("\n")

########## direct Input box ##########
def direct_input(event=None):
    new_text = entry.get()
    logging.info(f'new input : {new_text}')
    direct_food_founder(new_text)

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
        self.flag = False

        self.calendar_window = None  # 캘린더 창의 참조를 저장할 변수

    def clicked(self):
        logging.info(f'calendar button clicked')
        if not self.flag:
            self.image = tk.PhotoImage(file='calendar_icon_b.png')
            self.image = self.image.subsample(4, 4)
            self['image'] = self.image
            self.update()
            if self.calendar_window is None:  # 캘린더 창이 열려있지 않은 경우
                self.calendar_window = Calendar(master=self.master)  # 캘린더 창 생성
            self.flag = True
        else:
            self.calendar_close()  # 캘린더 창이 열려있는 경우 닫기

    def calendar_close(self):
        if self.calendar_window is not None:
            self.calendar_window.destroy()  # 캘린더 창 닫기
            self.calendar_window = None
            self.flag = False
        self.image = tk.PhotoImage(file='calendar_icon.png')
        self.image = self.image.subsample(4, 4)
        self['image'] = self.image
        self.update()


########## Calendar ##########
class Calendar(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.title("점메추 캘린더")
        self.iconphoto(False, tk.PhotoImage(file="calendar_icon.png"))
        self.geometry("480x640+{}+{}".format(self.master.winfo_x()+490, self.master.winfo_y()))
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.calendar_destroy)
        self.bind('<Escape>', lambda event: self.calendar_destroy())

        self.create_calendar()

    def create_calendar(self):
        today = datetime.now()
        year, month = today.year, today.month

        # 월 레이블 생성
        month_label = tk.Label(self, text=f"{year}년 {month}월", font=("Arial", 14))
        month_label.place(x=200, y=580)

        # 캘린더 그리드 생성
        cal = calendar.Calendar()
        for i, week in enumerate(cal.monthdayscalendar(today.year, today.month)):
            for j, day in enumerate(week):
                if day == 0:
                    day = "-"
                if day == today.day:
                    # 오늘 날짜에 하이라이트 추가
                    label = tk.Label(self, text=day, bg="yellow")
                else:
                    label = tk.Label(self, text=day)

                label.grid(row=i, column=j, padx=21, pady=42)


        if rgb1 != "":
            label1 = tk.Label(self, bg=f"{rgb1}", width=8)
            label1.place(x=275,y=70)
            label1.update()
        if rgb2 != "":
            label2 = tk.Label(self, bg=f"{rgb2}", width=8)
            label2.place(x=275,y=90)
            label2.update()
        if rgb3 != "":
            label3 = tk.Label(self, bg=f"{rgb3}", width=8)
            label3.place(x=275,y=110)
            label3.update()






    def calendar_destroy(self):
        self.destroy()

        calendar_button.calendar_close() # have to fix



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

        lunch_button.off()  # have to fix
        dinner_button.off() # have to fix

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

        dinner_button.off()     # have to fix
        breakfast_button.off()  # have to fix

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

        lunch_button.off()      # have to fix
        breakfast_button.off()  # have to fix

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
        logging.info(f'data node = {data_node}')
        food_founder()


########## nutrient label ##########
class NutrientLabel():
    def __init__(self):
        self.kcal_label = tk.Label(window, text="칼로리(Kcal)")
        self.carbohydrate_label = tk.Label(window, text="탄수화물 [R]")
        self.protein_label = tk.Label(window, text="단백질    [G]")
        self.fat_label = tk.Label(window, text="지방       [B]")

        self.kcal_label.place(x=80,y=150)
        self.carbohydrate_label.place(x=80,y=180)
        self.protein_label.place(x=80,y=210)
        self.fat_label.place(x=80,y=240)

        self.kcal = tk.Label(window, text=f"")
        self.carbohydrate = tk.Label(window, text=f"")
        self.protein = tk.Label(window, text=f"")
        self.fat = tk.Label(window, text=f"")

        self.kcal.place(x=160, y=150)
        self.carbohydrate.place(x=160, y=180)
        self.protein.place(x=160, y=210)
        self.fat.place(x=160, y=240)

    def init_current_nutrient(self):
        self.kcal.config(text=f"{current_kcal}")
        self.carbohydrate.config(text=f"{current_carbohydrate}")
        self.protein.config(text=f"{current_protein}")
        self.fat.config(text=f"{current_fat}")

        self.kcal.update()
        self.carbohydrate.update()
        self.protein.update()
        self.fat.update()

########## etc ##########
class ColorInterface():
    def __init__(self):
        self.label = tk.Label(window, width=20, height=5)
        self.label.place(x=240,y=170)

    def set_color(self):
        global current_protein, current_fat, current_carbohydrate
        current_carbohydrate *= 4
        current_protein *= 4
        current_fat *= 9

        global global_rgb, rgb1, rgb2, rgb3
        global_rgb = f"#{decimal_to_hex(current_carbohydrate)+decimal_to_hex(current_protein)+decimal_to_hex(current_fat)}"



        self.label.config(bg=f"{global_rgb}")
        self.label.update()

########## etc ##########
def decimal_to_hex(decimal):
    if decimal < 0:
        decimal = 0
    elif decimal > 255:
        decimal = 255

    hex_value = hex(decimal)[2:]
    if len(hex_value) == 1:
        hex_value = '0' + hex_value
    return hex_value.upper()

########## main ##########
data_node = 0

BLD_index = BLDIndex()
menu_interface_button = MenuInterfaceButton()
recommend_button = RecommendButton()
calendar_button = CalendarButton()

breakfast_button = BreakfastButton()
lunch_button = LunchButton()
dinner_button = DinnerButton()

nutrient_label = NutrientLabel()
color_label = ColorInterface()


rgb1 = ""
rgb2 = ""
rgb3 = ""

global_data = [ rgb1, rgb2, rgb3 ]

window.bind('<Escape>', lambda event: window.quit())
window.mainloop()