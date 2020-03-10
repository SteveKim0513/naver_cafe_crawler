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
total_list = ['writer', 'head', 'title']

nowDate = datetime.date.today()
filename = './' + str(nowDate) + '_list' + '.csv'
f = open(filename, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow([total_list[0], total_list[1], total_list[2]])
f.close()

# --------------------------------------------------------------------------------- #

# chrome driver setting
driver = webdriver.Chrome('./chromedriver')
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
base_url = 'https://cafe.naver.com/imsanbu/ArticleList.nhn?search.clubid=10094499'
# check the number of collected data
cnt = 0
# 게시판 리스트
boardList = ['596', '817', '242', '404', '437', '126']
# max 수집 페이지 수
crawlingPage = 1000
# 수집 기간
checkDate = nowDate - datetime.timedelta(days=7)


for currentBoard in boardList:
    driver.get('https://naver.com/')
    print("MENU : " + currentBoard + '\n')

    page = 0  # position of current page

    while page < crawlingPage:
        page = page + 1
        print("PAGE : " + str(page) + '\n')


        try:
            driver.get(base_url + '&search.menuid=' + currentBoard + '&search.page=' +
                       str(page) + '&userDisplay=50')

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


        # html parsing check
        if not soup.select('a.article') or not soup.select('td.p-nick') or not soup.select('td.td_date'):
            print("Cannot read page! Try Again")
            page = page - 1
            time.sleep(3)
            continue

        else:
            # 공지사항 제외 리스트 수 추출
            num_Notice = 0 # 공지사항 갯수
            num_Title = len(soup.select('a.article')) # 게시판 페이지 글 갯수 

            if (num_Title) > 50:
                num_Notice = num_Title - 50


        # 제목 리스트 50개 추출
        for i in range(num_Notice, num_Title) :

            # 추출 String(한 줄씩 입력하고 초기화)
            tempStr = '' # 말머리와 글 제목 추출 시 데이터 전처리 용

            userStr = ''
            titleStr = ''
            headStr = ''
            resultList = [] 

            # 작성자 추출
            userStr = soup.select('td.p-nick')[i].get_text()

            # 머리말 & 제목 추출
            ## 데이터 전처리
            tempStr = soup.select('a.article')[i].get_text()
            tempStr = tempStr.replace("\t","")
            tempStr = tempStr.replace(" ","")
            tempStr = tempStr.replace("\n","")

            seperatorVal = tempStr.find(']')

            for hLoop in range(seperatorVal+1):
                headStr = headStr + tempStr[hLoop]

            for tLoop in range(seperatorVal+1, len(tempStr)):
                titleStr = titleStr + tempStr[tLoop]

            # Result List
            resultList.append(userStr)
            resultList.append(headStr)
            resultList.append(titleStr)

            # Write to csv
            f = open(filename, 'a+', encoding='utf-8', newline='')
            wr = csv.writer(f)
            wr.writerow(resultList)
            f.close()
            cnt = cnt + 1


            if soup.select('td.td_date')[i].get_text() == (str(checkDate).replace('-', '.')+'.'):
                print("기간 내 데이터 수집 완료!")
                break

        if cnt%50 != 0 : break

        time.sleep(3)

print("Done!")
