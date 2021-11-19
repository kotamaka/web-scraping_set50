from bs4 import BeautifulSoup
from ezsheets import Sheet
import requests,datetime,time,json
import ezsheets

sheets = ezsheets.Spreadsheet('1-4Qsc0YmhSvajyesDTvcqbRQjEylpbY8sigy34MQQnU')

now = datetime.datetime.now()
date_time = now.strftime("/%d-%m-%Y")
localtime = time.localtime()
day = localtime[2]
month = localtime[1]
year = localtime[0]
n_hour = localtime[6]
n_min = localtime[4]
n_sec = localtime[5]

url = "https://www.settrade.com/C13_MarketSummary.jsp?detail=SET50"

res = requests.get(url)
res.encoding = "utf-8"
if res.status_code == 200:
    print("Get URL Successful\n")
elif res.status_code == 404:
    print("Error 404 page not found")
else:
    print("Not both 200 and 404")

soup = BeautifulSoup(res.text, 'html.parser')
#courses = soup.find_all('tbody')
courses = soup.select(".table-responsive")
soup2 = BeautifulSoup(str(courses), 'html.parser')
courses2 = soup2.select(".link-stt")

course_list = []
for i in courses2:
    if "txtSymbol" in str(i):
        name = i.next_element
        course_list.append(name)
        
#print(course_list)

def push2sheets():
    p_date = '{}/{}/{}'.format(day,month,year)
    data = sheets['Category_name']
    data[1,1] = 'SET50 : {}'.format(p_date)
    count = 2
    for i in course_list:
        data[1,count] = i
        count += 1
    print('Add to sheets successful!')

push2sheets()