import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import tkinter.font
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from datetime import datetime

# What to add and modify / 추가 및 수정할 것
# Resize text and chart windows / 텍스트 및 차트창 크기 조정
# Replace with tree format in the industry data display window - Done / industry 데이터 표시 창 tree 형식으로 바꾸기 - 완료
# Display Chart Vertical and Horizontal Figures Accurately - Done / 차트 세로 가로 수치 정확히 표시 - 완료
# Add two industry search buttons (industry description inquiry, predictive model description inquiry) - Done (create/connect two functions) / industry search 버튼 두개 추가(산업 설명 조회, 예측 모델 설명 조회) - 완료 (함수 두개 생성/연결)
# Industry radio button - Done, column interval adjustment is required / industry radio button - 완료, column 간격 조절 필요 
# Add Review Lookup button - Done (Create/Connect function) / 리뷰 조회 버튼 추가 - 완료(함수 생성/연결)


# MySQL Connection Settings / MySQL 연결 설정
mydb = mysql.connector.connect(
        host="localhost",
        user = "root",
        passwd = "",
        db = "financial"
)
mycursor = mydb.cursor()

def search_company():
    show_txt()
    show_chart()
company_search_result = None


def company_search_window(): # Create new window for 'Return Rentals' button
    global search_window,middle_frame, entry_title

    search_window = tk.Toplevel()
    search_window.geometry("600x500")
    search_window.title("Company Search")

    top_frame = tk.Frame(search_window, bg='aliceblue')
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)

    for i in range(1):  
        top_frame.columnconfigure(i, weight=1)
    
    label = tk.Label(top_frame, text="Enter Company Name", font=font1, pady=15, bg='aliceblue')
    label.grid(row=0,column=0)
    entry_title = tk.Entry(top_frame)
    entry_title.grid(row=1,column=0)
    entry_title.bind("<Return>", return_name)

    middle_frame = tk.Frame(search_window, bg='lightblue')
    middle_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.7)
    middle_frame.pack_propagate(1)
    middle_frame.grid_propagate(True)

    for i in range(3):
        middle_frame.columnconfigure(i, weight=1)


    bottom_frame = tk.Frame(search_window, padx=15, bg='aliceblue')
    bottom_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
    bottom_frame.pack_propagate(0)

    button = tk.Button(bottom_frame, text="Clear", width=6, command=clear)
    button.pack(side="right")



def return_name(event): # Show results of overdue customer rentals
    for widget in middle_frame.winfo_children():
        widget.destroy()
        
    name = entry_title.get()
    query = f"SELECT code, name from company_info \
            WHERE LOWER(name) LIKE LOWER('%{name}%') LIMIT 7"
    mycursor.execute(query)
    data = mycursor.fetchall()
        
    column_names=["Code", "Company Name",'Option']
    if not data:
        result_label = tk.Label(middle_frame, text=f"Company Name with '{name}' does not exist",font= font2, bg='lightblue', pady=30)
        result_label.pack()
    else:
        company_label = tk.Label(middle_frame, font=(font1), text="Results", bg='lightblue')
        company_label.grid(row=0,column=0,columnspan=3)

        for i in range(3):
            column_label = tk.Label(middle_frame, bg = 'lightblue', text=column_names[i], font=(font1))
            column_label.grid(row=1,column=i,sticky="w")

        for idx, company in enumerate(data):
            for i in range(2):
                result_label = tk.Label(middle_frame, text=company[i], bg='lightblue', pady = 10)
                result_label.grid(row=idx+2,column=i,sticky="w")
            result_label = tk.Button(middle_frame, text='Select', bg='cornflowerblue', fg='white', width= 8, command=lambda comp=company: select_button_pressed(comp[1]))
            result_label.grid(row=idx+2,column=2,sticky="w")



def select_company(companyname): # Execute query for updating return date of rental item
    global company_search_result
    company_search_result = companyname
    label_var.set(company_search_result)

def select_button_pressed(companyname): # Update DB and display pop-up
    messagebox.showinfo("Message", "The company has been selected!")
    select_company(companyname)
    search_window.destroy()

def clear(): # Clear the text entry and results in 'Return Rental' window
    for widget in middle_frame.winfo_children():
        widget.destroy()
    entry_title.delete(0, 'end')

def show_txt():
    company_name = company_search_result
    try:   
        # Run MySQL Queries - Search for information that corresponds to the entered company name / MySQL 쿼리 실행 - 입력된 회사 이름에 해당하는 정보 검색
        select_query = "SELECT c.name, c.industry, c.current_assets, c.current_liability, c.net_profit, \
        AVG(d.volume) FROM sep_trading d, company_info c \
        WHERE d.company_code = c.code AND c.name = %s \
        GROUP BY d.company_code"
        mycursor.execute(select_query, (company_name,))
        company_info = mycursor.fetchone()
        
        # Display searched information in the text  / 검색된 정보를 텍스트 창에 표시
        if company_info:
            # Adding a title for text information / 텍스트창 정보에 대한 제목 추가 
            display_text = f"Industry: {company_info[1]}\n\nCurrent Assets: {company_info[2]}\n\nCurrent Liability: {company_info[3]}\n\nNet Profit: {company_info[4]}\n\nAverage Volume: {company_info[5]}"
            T1.delete(1.0, tk.END)  # Delete existing text / 기존 텍스트 삭제
            T1.insert(tk.END, display_text)
        else:
            messagebox.showinfo(title='Message', message="Error! Company name is incorrect. Please re-enter.")
            T1.delete(1.0, tk.END)  # Delete existing text / 기존 텍스트 삭제
            T1.insert(tk.END, "Error!\nCompany name is incorrect.\nPlease re-enter.")

    except mysql.connector.Error as error:
        print("Error:", error)

# function that shows a chart
def show_chart():
    try:
    
        company_name = company_search_result
        start_date = startdate_entry.get()
        end_date = enddate_entry.get()
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        # Excecute MySQL query

        query = ("SELECT d.high, d.low "
                "FROM sep_trading d, company_info c "
                "WHERE d.company_code = c.code "
                "AND c.name = %s "
                "AND d.date BETWEEN %s AND %s")

        mycursor.execute(query, (company_name, start_date, end_date))
        data = mycursor.fetchall()

        highs = [row[0] for row in data]
        lows = [row[1] for row in data]

        # draw chart
        ax.clear()
        ax.plot(highs, label='High')
        ax.plot(lows, label='Low')
        ax.set_xlabel('Days')
        ax.set_ylabel('Price(CNY)')
        # ax.set_title(f'Stock Prices for {company_name} from {start_date} to {end_date}', fontsize = 7)
        compChart_label.config(text=f'Stock Prices for {company_name} from {start_date} to {end_date}', font=font2)
        ax.legend() 

        # Set x-axis range / x 축 범위 설정
        ax.set_xlim(start_date, end_date)


        # Setting the highest and lowest values / 최고값과 최저값 설정
        max_price = max(max(highs), max(lows))
        min_price = min(min(highs), min(lows))

        # Set y-axis range (stock price range) / y 축 범위 설정 (주식 가격 범위)
        ax.set_ylim(min_price, max_price)

        chart_canvas.draw()     

    except ValueError: 
        if company_name:
            messagebox.showinfo(title='Message', message="Invalid date format. Please use YYYY-MM-DD.")
            compChart_label.config(text='Error! Invalid date format. Please use YYYY-MM-DD.', font=font2)
        else:
            pass


def search_industry():

    #industry_name = industry_entry.get()
    
    industry_name = industry_var.get()

    # Delete data from all Treviews / 모든 Treeview의 데이터 삭제
    tree1.delete(*tree1.get_children())
    tree2.delete(*tree2.get_children())
    tree3.delete(*tree3.get_children())

    try:
        # Running MySQL Queries / MySQL 쿼리 실행
        # Read Model 1 Data / 모델 1 데이터 읽어오기
        mycursor = mydb.cursor()
        select_query = "SELECT name FROM company_info \
                        WHERE industry = %s \
                        ORDER BY fama_french_3factors DESC LIMIT 15"
        mycursor.execute(select_query, (industry_name,))
        
        # Show Imported Data / 가져온 데이터 표시
        data = mycursor.fetchall()
        display_data(data, tree1)



        # Reading Model 2 Data / 모델 2 데이터 읽어오기
        mycursor = mydb.cursor()
        select_query = "SELECT name FROM company_info \
                        WHERE industry = %s \
                        ORDER BY carhart_4factors DESC LIMIT 15"
        mycursor.execute(select_query, (industry_name,))
        
        # Show Imported Data / 가져온 데이터 표시
        data = mycursor.fetchall()
        display_data(data, tree2)

        # Reading Model 3 Data / 모델 3 데이터 읽어오기
        mycursor = mydb.cursor()
        select_query = "SELECT name FROM company_info \
                        WHERE industry = %s \
                        ORDER BY fama_french_5factors DESC LIMIT 15"
        mycursor.execute(select_query, (industry_name,))
        
        # Show Imported Data / 가져온 데이터 표시
        data = mycursor.fetchall()
        display_data(data, tree3)
        

    except mysql.connector.Error as error:
        print("Error:", error)
        



def display_data(data, frame):

    for i, item in enumerate(data, start=1):
        frame.insert("", "end", text=str(i), values=item)



# Industry information lookup function for pop-up windows - resize windows if necessary / 팝업창을 위한 산업 정보 조회 함수 - 필요시 창 크기 조정
def industryInfoSearch():
    # industry info search new window
    industryInfo_window = tk.Toplevel()
    industryInfo_window.geometry("600x500")
    industryInfo_window.title('Industry Info Search')

    top_frame = tk.Frame(industryInfo_window, bg='azure')
    top_frame.pack(fill="both", expand=True)
    
    industry_name = industry_var.get()

    if industry_name:
        mycursor = mydb.cursor()
        select_query = f"SELECT content,explanation FROM description \
                        WHERE LOWER(content) LIKE LOWER('%{industry_name}%')"
        mycursor.execute(select_query, )

        data = mycursor.fetchone()

        result_label1 = tk.Label(top_frame, text=data[0], font=(font1, 20, 'bold'), bg='azure',wraplength=400, pady=20)
        result_label1.pack()
        result_label2 = tk.Label(top_frame, text=data[1], font=(font2, 16 ), bg='azure',wraplength=500, pady=20)
        result_label2.pack()
        
    else:
        result_label1 = tk.Label(top_frame, text="Please choose the industry", font=(font2, 20, 'bold'), bg='azure',wraplength=400, pady=20)
        result_label1.pack()



# Model information lookup function for pop-up windows - resize windows if necessary / 팝업창을 위한 모델 정보 조회 함수 - 필요시 창 크기 조정
def modelInfoSearch():
    # model info search new window
    modelInfo_window = tk.Toplevel()
    modelInfo_window.geometry("600x500")
    modelInfo_window.title('Model Info Search')

    top_frame = tk.Frame(modelInfo_window, bg='azure')
    top_frame.pack(fill="both", expand=True)

    mycursor = mydb.cursor()
    select_query = "SELECT content,explanation FROM description \
                    WHERE content IN ('Fama-French 3factors', 'Carhart 4factors', 'Fama-French 5factors')"
    mycursor.execute(select_query, )

    data = mycursor.fetchall()

    for i in range(2):  
        top_frame.columnconfigure(i, weight=1)

    for idx, text in enumerate(data):
        result_label1 = tk.Label(top_frame, text=text[0], font=(font2, '13', 'bold'), bg='azure',wraplength=400, pady=40)
        result_label1.grid(row=idx,column=0)
        result_label2 = tk.Label(top_frame, text=text[1], font=font2, bg='azure',wraplength=400, pady=20)
        result_label2.grid(row=idx,column=1)



# Company review insert function / 회사 리뷰 insert 함수 
def insert_review():
    company_name = company_search_result
    review_text = review_entry.get()
    
    try:
        # Run MySQL Queries / MySQL 쿼리 실행
        if company_name and review_text:

            mycursor = mydb.cursor()
            select_query = "INSERT INTO review (company_name, comment) VALUES (%s, %s)"
            mycursor.execute(select_query, (company_name,review_text))
        
            # Reflect changes to DB / 변경사항을 DB에 반영
            mydb.commit()
        
            # success message / 성공 메시지
            result_label.config(text="Review added successfully!")

            # delete the typed company name and review after inserting the review
            review_entry.delete(0, tk.END)
        
        else:
            messagebox.showinfo(title='Message', message="Company name or review has not been entered. Please input again.")
            result_label.config(text="Company name or review has not been entered. Please input again.")


    except mysql.connector.Error as error:
        print("Error:", error)



# Review query function for pop-up windows - resize windows if needed / 팝업창을 위한 리뷰 조회 함수 - 필요시 창 크기 조정
def show_review():
    # model info search new window
    review_window = tk.Toplevel()
    review_window.geometry("700x500")
    review_window.title('Review Search')

    top_frame = tk.Frame(review_window, bg='azure')
    top_frame.pack(fill="both", expand=True)

    mycursor = mydb.cursor()
    select_query = "SELECT * FROM review LIMIT 15"
    mycursor.execute(select_query, )

    data = mycursor.fetchall()


    top_frame.columnconfigure(0, weight=1)
    top_frame.columnconfigure(1, weight=2)
    top_frame.columnconfigure(2, weight=7)



    column_names=["ID", "Company Name", "Review"]
    if not data:  
        result_label1 = tk.Label(top_frame, text="Please write a review", font=(font2, 20, 'bold'), bg='azure',wraplength=400, pady=20)
        result_label1.pack()
    else:
        for i in range(3):
            result_label1 = tk.Label(top_frame, text=column_names[i], font=font1, bg = 'azure', wraplength=400)
            result_label1.grid(row=0,column=i,sticky='w')
        for idx, review in enumerate(data):
            for i in range(3):
                result_label1 = tk.Label(top_frame, text=review[i], font=font2, bg='azure', wraplength=400)
                result_label1.grid(row=idx+1,column=i,sticky='w')


def on_double_click(event,tree):
    global company_search_result
    item = tree.selection()[0]
    name = tree.item(item, "values")[0]  

    select_company(name)
    show_txt()
    show_chart()

# Set title of tkinter, and window size / tkinter의 제목, 창크기 설정
application_window = tk.Tk()
application_window.geometry("1000x850")
application_window.title('BizInsight Hub')
application_window.configure(bg="aliceblue")

# Adjust row width / 행 너비 조절
for i in range(10):  
    application_window.rowconfigure(i, minsize=0)

# Adjust column width / 열 너비 조절
for i in range(3):  # Adjust width for columns 0 to 2 / 열 0~2에 대해 너비를 조절
    application_window.columnconfigure(i, weight=1)

# Set font type for tkinter / tkinter의 폰트 종류 설정
font0=tkinter.font.Font(family="Verdana", size=20)
font1=tkinter.font.Font(family="Verdana", size=15)
font2=tkinter.font.Font(family="Helvetica", size=11)

# Central Labeling (Writing color: navy, font1) / 중앙 라벨링 (글씨색: navy, font1적용)
title_label = tk.Label(application_window, text = 'BIZ-INSIGHT HUB',
                 fg="navy", font=font0, bg="aliceblue")
# Set the center label position / 중앙 라벨 위치 설정
title_label.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

# 'Search by company' label (Written color: royal blue, font2) / '회사별 검색' 라벨 (글씨색: royalblue, font2적용)
CompanyPerformanceInsight_label = tk.Label(application_window, text = 'Company Performance Insight',
                 fg="royalblue", font=font1, bg="aliceblue")
# Setting Label Locations / 라벨 위치 설정
CompanyPerformanceInsight_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Search Frames by Company / 회사별검색 프레임 
frame1 = tk.Frame(application_window, width=1000, height=260, bg="lightblue")
frame1.grid(row=2, column=0, padx=5, pady=5, sticky='n',columnspan=8)
frame1.grid_propagate(False)

# Frame1 Column Width Adjustment / frame1 열 너비 조절
for i in range(8):  # Adjust width for columns 0 to 7 / 열 0~7에 대해 너비를 조절
    frame1.columnconfigure(i, weight=1)

# Frame1 row width Adjustment / frame1 행 너비 조절
for i in range(8):  # Adjust width for columns 0 to 7 / 행 0~7에 대해 너비를 조절
    frame1.rowconfigure(i, minsize=0)


# 'Company name' label for search box (Writing color: black, font2) / 검색창을 위한 '회사 이름' 라벨 (글씨색: black, font2적용)
companyName_label = tk.Label(frame1, text = 'Company', bg="lightblue",fg="black", font=font2)
companyName_label.grid(row=0, column=0, padx=5, pady=5)
# Search window for company name / 회사 이름 검색 창



label_var = tk.StringVar(value="please choose company")
companyName_entry = tk.Label(frame1, textvariable=label_var, bg ="lightblue", width=40)
companyName_entry.grid(row=0, column=1)
companyName_button = tk.Button(frame1, text="Search", bg="cornflowerblue", fg="white", command=company_search_window, width = 10)
companyName_button.grid(row=0, column=2)


# 'Enter start date' label for search window (Writing color: black, font2 applied) / 검색창을 위한 '시작 날짜 입력' 라벨 (글씨색: black, font2적용)
start_label = tk.Label(frame1, text = 'Start', bg="lightblue",fg="black", font=font2)
start_label.grid(row=0, column=3, padx=5, pady=5)
# Search Start Date Input Window / 검색 시작 날짜 입력 창
startdate_entry = tk.Entry(frame1, width=15)
startdate_entry.grid(row=0, column=4, padx=5, pady=5)
#default data typed in to show the format
startdate_entry.insert(0, '2023-09-01')

# 'Enter last date' label for search window (Writing color: black, font2 applied) / 검색창을 위한 '마지막 날짜 입력' 라벨 (글씨색: black, font2적용)
end_label = tk.Label(frame1, text = 'End', bg="lightblue",fg="black", font=font2)
end_label.grid(row=0, column=5, padx=5, pady=5)
# Last Date Input Window / 마지막 날짜 입력 창
enddate_entry = tk.Entry(frame1, width=15)
enddate_entry.grid(row=0, column=6, padx=5, pady=5)
#default data typed in to show the format
enddate_entry.insert(0, '2023-09-30')

# search button / 검색 버튼
search_button1 = tk.Button(frame1, text="Search", bg="cornflowerblue", fg="white", command=search_company, width = 10)
search_button1.grid(row=0, column=7, padx=10, pady=5)

# 'company info' label 
compInfo_label = tk.Label(frame1, text = 'Brief Company Info', bg="lightblue",fg="black", font=font2)
compInfo_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
# "The upper and lower limit graph of the company." Label' / 회사 상한가 하한가 그래프' 라벨
compChart_label = tk.Label(frame1, text = 'Chart', bg="lightblue",fg="black", font=font2)
compChart_label.grid(row=1, column=2, padx=5, pady=5, columnspan=6)

# Set the company information output window (txt) (recognize string variables) / 회사 정보 출력 창(txt) 설정 (문자열 변수 인식) - company, industry, volume, current assets, current reliability, net profit
T1 = tk.StringVar()
T1 = tk.Text(frame1, height = 10, width = 45, bg="aliceblue")
T1.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

# Creating Chart Display Labels / 차트 표시 라벨 생성
fig, ax = plt.subplots(figsize=(5, 1.6))
chart_canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas_widget = chart_canvas.get_tk_widget()
canvas_widget.grid(row=2, column=2, padx=5, pady=5, columnspan=6)
fig.subplots_adjust(left=0.15, right=0.9, top=0.95, bottom=0.15)



# 'In-industry search' label (Writing color: royal blue, font2) / '산업 내 검색' 라벨 (글씨색: royalblue, font2적용)
industrySearch_label = tk.Label(application_window, text = 'Top 10 Company List by Prediction Models',
                 fg="royalblue", font=font1, bg="aliceblue")
# Setting Label Locations / 라벨 위치 설정
industrySearch_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

# In-industry search frame / 산업내검색 프레임 
frame2 = tk.Frame(application_window, width=1000, height=300, bg="lightblue")
frame2.grid(row=5, column=0, padx=5, pady=5, sticky='n',columnspan=9)
frame2.grid_propagate(False)

# Adjust column width / 열 너비 조절
for i in range(45):  # Adjust width for columns 0 to 8 / 열 0~8에 대해 너비를 조절
    frame2.columnconfigure(i, weight=1)


# Industry Select Radio Button / 산업 선택 라디오 버튼
# Industry options
industry_options = [("Integrated Enterprise", "integrated enterprise"),
                    ("Finance", "finance"), 
                    ("Utilities", "Utilities"), 
                    ("Real Estate", "real estate"), 
                    ("Industry", "industry"), 
                    ("Business", "Business")
                    ]

# Variable to store the selected Industry / 선택된 Industry를 저장할 변수
industry_var = tk.StringVar()


# Create a radio button / 라디오 버튼 생성
for index, (text, value) in enumerate(industry_options):
    rb = tk.Radiobutton(frame2, text=text, variable=industry_var, value=value, bg='lightblue', fg='black')
    rb.grid(row=1, column=index*5, pady=5, columnspan=5)
    rb_width = len(text) + 4  # Adjust button width according to text length / 텍스트 길이에 따라 버튼 너비 조절
    rb.config(width=rb_width)  # Setting button width / 버튼 너비 설정


#search button / 검색 버튼
search_button2 = tk.Button(frame2, text="Search", bg="cornflowerblue", fg="white", command=search_industry, width = 15)
search_button2.grid(row=1, column=30, padx=10, pady=5, columnspan=5)

# industry info button / 산업 정보 버튼
search_button2 = tk.Button(frame2, text="Industry Info", bg="cornflowerblue", fg="white", command=industryInfoSearch, width = 15)
search_button2.grid(row=1, column=35, padx=10, pady=5, columnspan=5)

# model info button / 예측 모델 정보 버튼
search_button2 = tk.Button(frame2, text="Model Info", bg="cornflowerblue", fg="white", command=modelInfoSearch, width = 15)
search_button2.grid(row=1, column=40, padx=10, pady=5,columnspan=5)

# Output company list by prediction model / prediction 모델 별 회사 리스트 출력
# model1 label / 모델 1 라벨
model1_label = tk.Label(frame2, text= 'Fama-French 3 factors', bg="lightblue",fg="black", font=font2)
model1_label.grid(row=2, column=0, padx=10, pady=10, columnspan=11)
# model2 label / 모델 2 라벨
model2_label = tk.Label(frame2, text= 'Carhart 4 factors', bg="lightblue",fg="black", font=font2)
model2_label.grid(row=2, column=15, padx=10, pady=10, columnspan=11)
# model3 label / 모델 3 라벨
model3_label = tk.Label(frame2, text= 'Fama-French 5 factors', bg="lightblue",fg="black", font=font2)
model3_label.grid(row=2, column=30, padx=10, pady=10, columnspan=15)

# Canvas for Data Display / Data 표시를 위한 canvas
# Canvas for Model 1 Data / 모델 1 Data를 위한 canvas
canvas2_1 = tk.Canvas(frame2, width=295, height=190, bg="lightblue")
canvas2_1.grid(row=3, column=0, padx=1, pady=5, columnspan=11)
canvas2_1.grid_propagate(False)


# Create scrollbar / 스크롤바 생성
scrollbar2_1 = ttk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas2_1.yview)
scrollbar2_1.grid(row=3, column=11, sticky='ns')
canvas2_1.config(yscrollcommand=scrollbar2_1.set)
#canvas2_1.config(scrollregion=canvas2_1.bbox("all"))


scrollable_frame2_1 = tk.Frame(canvas2_1)
canvas2_1.create_window((0,0), window= scrollable_frame2_1, anchor='nw')

canvas2_1.bind('<Configure>', lambda e: canvas2_1.configure(scrollregion=canvas2_1.bbox("all")))

# Create a Treview to display the contents of the database / 데이터베이스 내용을 표시할 Treeview 생성
tree1 = ttk.Treeview(scrollable_frame2_1)
tree1.grid(row=0, column=0, sticky="nsew")
tree1['columns'] = ("Company Name",)
#tree3.column("#0", width=0, stretch=tk.NO) 
tree1.heading("#0", text="Ranking")  # 좌측 열(번호)의 헤딩 설정
tree1.heading("Company Name", text="Company Name")
tree1.grid(row=0, column=0)
tree1.column("#0", width =50, anchor='center')
tree1.column("Company Name", width=240, anchor='center')
tree1.bind("<Double-1>", lambda event,tree=tree1: on_double_click(event,tree))


# Canvas for Model 2 Data / 모델 2 Data를 위한 canvas
canvas2_2 = tk.Canvas(frame2, width=295, height=190, bg="lightblue")
canvas2_2.grid(row=3, column=12, padx=1, pady=5, columnspan= 17)
canvas2_2.grid_propagate(False)

# Create scrollbar / 스크롤바 생성
scrollbar2_2 = ttk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas2_2.yview)
scrollbar2_2.grid(row=3, column=29, sticky='ns')
canvas2_2.config(yscrollcommand=scrollbar2_2.set)
canvas2_2.bind('<Configure>', lambda e: canvas2_2.configure(scrollregion=canvas2_2.bbox("all")))

scrollable_frame2_2 = tk.Frame(canvas2_2)
canvas2_2.create_window((0,0), window= scrollable_frame2_2, anchor='w')

# Create a Treview to display the contents of the database / model2 Treeview 생성
tree2 = ttk.Treeview(scrollable_frame2_2)
tree2['columns'] = ("Company Name",)
#tree3.column("#0", width=0, stretch=tk.NO) 
tree2.heading("#0", text="Ranking")  # 좌측 열(번호)의 헤딩 설정
tree2.heading("Company Name", text="Company Name")
tree2.grid(row=0, column=0)
tree2.column("#0", width =50, anchor='center')
tree2.column("Company Name", width=240, anchor='center')
tree2.bind("<Double-1>", lambda event,tree=tree2: on_double_click(event,tree))

# Canvas for Model 3 Data / 모델 3 Data를 위한 canvas
canvas2_3 = tk.Canvas(frame2, width=295, height=190, bg="lightblue")
canvas2_3.grid(row=3, column=30, padx=1, pady=5, columnspan=14)
canvas2_3.grid_propagate(False)

# Create scrollbar / 스크롤바 생성
scrollbar2_3 = ttk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas2_3.yview)
scrollbar2_3.grid(row=3, column=44, sticky='ns')
canvas2_3.config(yscrollcommand=scrollbar2_3.set)
canvas2_3.bind('<Configure>', lambda e: canvas2_3.configure(scrollregion=canvas2_3.bbox("all")))

scrollable_frame2_3 = tk.Frame(canvas2_3)
canvas2_3.create_window((0,0), window= scrollable_frame2_3, anchor='w')

# Create a Treview to display the contents of the database / model3 Treeview 생성
tree3 = ttk.Treeview(scrollable_frame2_3)
tree3['columns'] = ("Company Name",)
#tree3.column("#0", width=0, stretch=tk.NO) 
tree3.heading("#0", text="Ranking")  # 좌측 열(번호)의 헤딩 설정
tree3.heading("Company Name", text="Company Name")
tree3.grid(row=0, column=0)
tree3.column("#0", width =50, anchor='center')
tree3.column("Company Name", width=240, anchor='center')
tree3.bind("<Double-1>", lambda event,tree=tree3: on_double_click(event,tree))




# 'Add Data' label (Writing color: royal blue, font2) / '데이터 추가' 라벨 (글씨색: royalblue, font2적용)
addReview_label = tk.Label(application_window, text = 'Company Reviews',
                 fg="royalblue", font=font1, bg="aliceblue")
# Setting Label Locations / 라벨 위치 설정
addReview_label.grid(row=7, column=0, padx=5, pady=5, sticky='w')

# In-industry search frame / 산업내검색 프레임 
frame3 = tk.Frame(application_window, width=1000, height=90, bg="lightblue")
frame3.grid(row=8, column=0, padx=5, pady=5, sticky='n',columnspan=3)
frame3.grid_propagate(False)

# Adjust column width / 열 너비 조절
for i in range(7):  # 열 0~6에 대해 너비를 조절
    frame3.columnconfigure(i, weight=1)

# 'Company name' label for input window (Writing color: black, font2) / 입력창을 위한 '회사 이름' 라벨 (글씨색: black, font2적용)
companyName_label = tk.Label(frame3, text = 'Company Name', bg="lightblue",fg="black", font=font2)
companyName_label.grid(row=0, column=0, padx=5, pady=5)

# company name entry / 회사 이름 입력창
company_entry = tk.Label(frame3, textvariable = label_var, bg="lightblue",fg="black", font=font2)
company_entry.grid(row=0, column=1)

# 'Company review' label for input window (Writing color: black, font2) / 입력창을 위한 '회사 리뷰' 라벨 (글씨색: black, font2적용)
review_label = tk.Label(frame3, text = 'Review', bg="lightblue",fg="black", font=font2)
review_label.grid(row=0, column=2, padx=5, pady=5)

#company review entry / 회사 리뷰 입력창
review_entry = tk.Entry(frame3, width=35)
review_entry.grid(row=0, column=3, columnspan=2)

# Add company review  button / 회사 리뷰 추가 버튼
insert_button = tk.Button(frame3, text="Insert", bg="cornflowerblue", fg="white", command=insert_review, width = 10)
insert_button.grid(row=0, column=5, padx=5, pady=5)

# Company review view button / 회사 리뷰 조회 버튼
insert_button2 = tk.Button(frame3, text="Review List", bg="cornflowerblue", fg="white", command=show_review, width = 10)
insert_button2.grid(row=0, column=6, padx=5, pady=5)


# Labels displaying results / 결과를 표시하는 라벨
result_label = tk.Label(frame3, text="(Label for the result message)", bg="lightblue",fg="black", font=font2)
result_label.grid(row=1, column=0, padx=5, pady=5, columnspan=7)



application_window.mainloop()