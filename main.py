import calendar
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from logging import info as info, debug as debug, warning as warning

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime, timedelta
import random
import requests
# url = "http://openapi.foodsafetykorea.go.kr/api/a91585442a9345bba0e1/I2790/json/1/1000/NUM=1"
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.json()
#     # 이제 'data' 변수에 API에서 반환된 JSON 데이터가 들어 있습니다.
#     # 여기서 데이터를 분석하고 사용할 수 있습니다.
# else:
#     print("API에 액세스하는 데 문제가 발생했습니다. 상태 코드:", response.status_code)
#
# # 데이터에서 'I2790' 키의 값 추출
# i2790_data = data['I2790']
#
# # 총 항목 수 추출
# total_count = i2790_data['total_count']
#
# # 각 제품의 정보에 접근
# products = i2790_data['row']
#
# for product in products:
#     # 각 제품의 메이커 이름과 영양 정보 출력 예시
#     maker_name = product['MAKER_NAME']
#     nutr_cont1 = product['NUTR_CONT1']
#     print("제품 메이커:", maker_name)
#     print("1회 제공량의 영양 정보:", nutr_cont1)
#     print("--------------------")

# 초기 설정

def food_founder():
    global data_node
    data_node = "D" + str(random.randint(0, 12151)).zfill(6)

    base_url = "http://openapi.foodsafetykorea.go.kr/api/sample/I2790/json/"
    food_cd = data_node
    start_node = 1
    node_limit = 1000

    # 반복적으로 요청하여 원하는 음식 찾기
    found_food = False
    # 반복적으로 요청하여 원하는 음식 찾기
    found_food = False
    while not found_food:

        if start_node > 12500:
            data_node = "D" + str(random.randint(0, 12151)).zfill(6)
            food_cd = data_node
            print("검색 결과 존재하지 않는 food_cd입니다. 재검색합니다.")
        # 요청 URL 설정
        url = f"{base_url}{start_node}/{start_node + node_limit - 1}/FOOD_CD={food_cd}"


        response = requests.get(url) # HTTP GET 요청 보내기
        if response.status_code == 200: # 성공적인 응답 처리
            data = response.json()
            # 'RESULT' 키를 확인하여 데이터가 있는지 확인
            if 'RESULT' in data and data['RESULT']['CODE'] == 'INFO-200':
            # if 'RESULT' in data and data['RESULT']['MSG'] == '정상처리되었습니다.':
                # 데이터가 없다는 메시지 출력 후 반복문 종료
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


########## Global Variables ##########


########## menu interface button ##########
class MenuInterfaceButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.image = tk.PhotoImage(file='exfood.png')
        self.image = self.image.subsample(5, 5)
        self['image'] = self.image
        self['command'] = self.clicked
        self.place(x=120, y=20)

    def clicked(self):
        logging.info(f'Interface button clicked')


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
        # 오늘 날짜
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
                label.grid(row=i, column=j, padx=24, pady=42)

    def calendar_close(self):
        pass

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



########## main ##########
data_node = 0
BLD_index = BLDIndex()
menu_interface_button = MenuInterfaceButton()
recommend_button = RecommendButton()
calendar_button = CalendarButton()

breakfast_button = BreakfastButton()
lunch_button = LunchButton()
dinner_button = DinnerButton()

window.bind('<Escape>', lambda event: window.quit())
window.mainloop()