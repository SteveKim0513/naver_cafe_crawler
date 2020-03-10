import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
from bs4 import BeautifulSoup as bs
import csv

# --------------------------------------------------------------------------------- #

# Create csv file
# Column names
total_list = ['category', 'count']

nowDate = datetime.date.today()
filename = './' + str(nowDate) + '_numCategory' + '.csv'
f = open(filename, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow([total_list[0], total_list[1]])
f.close()

# --------------------------------------------------------------------------------- #

# chrome driver setting
driver = webdriver.Chrome(
    './chromedriver')
driver.implicitly_wait(3)

# --------------------------------------------------------------------------------- #

# Login Page
driver.get(
    'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
driver.find_element_by_name('id').send_keys('{ID}')
driver.find_element_by_name('pw').send_keys('{PW}')
# click login
driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
time.sleep(15)  # 자동입력방지 문자는 직접 입력

# --------------------------------------------------------------------------------- #

# base_url = cafe main page url
base_url = 'https://cafe.naver.com/imsanbu/ArticleList.nhn?search.clubid=10094499&search.menuid=&search.page='


# max 수집 페이지 수
crawlingPage = 1000


# 파악하고 싶은 기간
checkDate = nowDate - datetime.timedelta(days=7)
durationDate = str(nowDate) + " ~ " + str(checkDate)

cnt = 0
page = 0 # position of current page
categoryResult = []

while page < crawlingPage:
    page = page + 1

    print("PAGE : " + str(page))

    # Chrome Driver 정상 작동 체크
    try:
        driver.get(base_url + str(page) + '&userDisplay=50')

        time.sleep(5)

        driver.switch_to.frame('cafe_main')
        soup = bs(driver.page_source, 'html.parser')

    except Exception as ex1:
        print("Exception has been thrown"+str(ex1))
        page = page - 1
        driver.refresh()
        driver.implicitly_wait(20)
        continue

    time.sleep(5)


    # Title list와 작성날짜 parsing 확인
    if not soup.select('a.article') or not soup.select('td.td_date') or not soup.select('a.link_name'):
        print("Cannot read page! Try Again")
        page = page - 1
        time.sleep(3)
        continue
    else:
        # 공지사항 갯수
        num_Notice = 0

        # 게시판 페이지 글 갯수
        num_Title = len(soup.select('a.article'))


        if (num_Title) > 50:
            num_Notice = num_Title - 50
        
        print(num_Notice)
        print(num_Title)

        for j in range(num_Notice, num_Title) :

            if soup.select('td.td_date')[j].get_text() == (str(checkDate).replace('-', '.')+'.'):
                break
            else : 
                categoryResult.append(soup.select('a.link_name')[j-num_Notice].get_text())
                cnt = cnt + 1
               
    print(cnt)

    if cnt%50 != 0 : break



# Write to csv
f = open(filename, 'a+', encoding='utf-8', newline='')
wr = csv.writer(f)
for k in range(len(categoryResult)):
    wr.writerow([categoryResult[k], 1])
f.close()
            


print("Done!")
