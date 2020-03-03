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
total_list = ['작성자', '제목']

nowDate = datetime.date.today()
filename = './' + str(nowDate) + '.csv'
f = open(filename, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow([total_list[0], total_list[1]])
f.close()

# --------------------------------------------------------------------------------- #

# chrome driver setting
driver = webdriver.Chrome(
    '/Users/genius/Documents/Project_python/chromedriver')
driver.implicitly_wait(3)

# --------------------------------------------------------------------------------- #

# Login Page
driver.get(
    'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
driver.find_element_by_name('id').send_keys('11andhalf')
driver.find_element_by_name('pw').send_keys('Monalisa!')
# click login
driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
time.sleep(15)  # 자동입력방지 문자는 직접 입력

# --------------------------------------------------------------------------------- #

# base_url = cafe main page url
base_url = 'https://cafe.naver.com/imsanbu/ArticleList.nhn?search.clubid=10094499'
# number of collected data
cnt = 0
# 게시판 리스트
boardList = ['596', '817', '242', '404', '437', '126']
# max 수집 페이지 수
crawlingPage = 1000


for i in range(len(boardList)):
    driver.get('https://naver.com/')
    print("MENU : " + boardList[i] + '\n\n\n')

    page = 0  # position of current page

    while page < crawlingPage:
        page = page + 1

        print("PAGE : " + str(page))

        titleResult = []
        userResult = []
        dateResult = []
        temp_list = []

        try:
            driver.get(base_url + '&search.menuid=' + boardList[i] + '&search.page=' +
                       str(page) + '&userDisplay=50')
            driver.switch_to.frame('cafe_main')
            soup = bs(driver.page_source, 'html.parser')

        except Exception as ex1:
            print("Exception has been thrown"+str(ex1))
            page = page - 1
            driver.refresh()
            driver.implicitly_wait(20)
            continue

        if not soup.select('a.article') or not soup.select('td.p-nick') or not soup.select('td.td_date'):
            print("Cannot read page! Try Again")
            page = page - 1
            continue
        else:
            for j in range(len(soup.select('a.article'))):
                # 제목 추출
                titleResult.append(soup.select('a.article')[j].get_text())

                # 작성자 추출
                userResult.append(soup.select('td.p-nick')[j].get_text())

                # temp_list
                temp_list.append([titleResult[j], userResult[j]])

                # Write to csv
                f = open(filename, 'a+', encoding='utf-8', newline='')
                wr = csv.writer(f)
                wr.writerow(temp_list[j])
                f.close()
                cnt = cnt + 1

                # 날짜 확인
                checkDate = nowDate - datetime.timedelta(days=7)

                if soup.select('td.td_date')[j].get_text() == str(checkDate).replace('-', '.'):
                    break

        # End loop
        print([page, cnt])

        # 7일 전 데이터 수집 완료
        if j < 49:
            break
        time.sleep(3)

print("Done!")
