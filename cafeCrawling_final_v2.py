import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
from bs4 import BeautifulSoup as bs
import csv

# --------------------------------------------------------------------------------- #

# Select the menu
print('''
신생아 돌보기 질문방: 596
아이가 열이 나요 : 817
수유 질문방: 242
이유식/유아식 질문방: 404
아이 건강 질문방: 437
육아 질문방: 126
그만 : 0
''')

user_input_Menu = []

while 1:
    temp = int(input("Select menu : "))

    if temp == 0:
        break
    else:
        user_input_Menu.append(temp)

user_input_Page = int(input("Number of pages(1~1,000) : "))

# --------------------------------------------------------------------------------- #

# Create csv file
# Column names
total_list = ['번호', '게시판', '말머리', '작성자', '제목', '내용', '댓글']

nowDate = datetime.date.today()
filename = './' + str(nowDate) + '.csv'
f = open(filename, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow([total_list[0], total_list[1],
             total_list[2], total_list[3], total_list[4], total_list[5], total_list[6]])
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
driver.find_element_by_name('id').send_keys('ID')
driver.find_element_by_name('pw').send_keys('PW!')
# click login
driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
time.sleep(15)  # 자동입력방지 문자는 직접 입력

# --------------------------------------------------------------------------------- #

# base_url = cafe main page url
base_url = 'https://cafe.naver.com/imsanbu/ArticleList.nhn?search.clubid=10094499'

cnt = 0  # number of collected data

for selectedMenu in user_input_Menu:
    driver.get('https://naver.com/')
    print("MENU : " + str(selectedMenu) + '\n\n\n')
    page = 0  # position of current page

    while page < user_input_Page:  # Number of pages (max 1000)
        page = page + 1

        print("PAGE : " + str(page))

        quest_urls = []
        quest_list = []

        try:
            driver.get(base_url + '&search.menuid=' + str(selectedMenu) + '&search.page=' +
                       str(page) + '&userDisplay=50')
            driver.switch_to.frame('cafe_main')

            # 공지사항을 제외한 사용자 작성글만 list화
            temp_list = driver.find_elements_by_css_selector(
                'div.inner_list a.article')
            compare_list = driver.find_elements_by_css_selector(
                'tr._noticeArticle td.td_article div.board-list div.inner_list a.article')

        except Exception as ex1:
            print("Exception has been thrown"+str(ex1))
            page = page - 1
            driver.refresh()
            driver.implicitly_wait(20)
            continue

        for i in range(len(temp_list)):
            compare = 0
            for j in range(len(compare_list)):
                if temp_list[i] == compare_list[j]:
                    compare = compare + 1

            if compare == 0:
                quest_list.append(temp_list[i])

        quest_urls = [i.get_attribute('href') for i in quest_list]

        print(len(quest_list))

        for quest in quest_urls:

            try:
                driver.get(quest)
                driver.switch_to.frame('cafe_main')
                soup = bs(driver.page_source, 'html.parser')

                # 제목 추출
                if not soup.select('div.tit-box span.b'):
                    title = 'NULL'
                else:
                    title = soup.select('div.tit-box span.b')[0].get_text()

                # 내용 추출
                if not soup.select('#tbody'):
                    content = 'NULL'
                else:
                    content_tags = soup.select('#tbody')[0].select('p')
                    content = ' '.join([tags.get_text()
                                        for tags in content_tags])

                # 말머리 추출
                if not soup.select('div.tit-box span.head'):
                    tag = '0'
                else:
                    tag = soup.select('div.tit-box span.head')[0].get_text()

                # 작성자 추출
                if not soup.select('td.p-nick '):
                    user = 'NULL'
                else:
                    user = soup.select('td.p-nick ')[0].get_text()

                # 댓글 추출
                if not soup.select('span.comm_body'):
                    comm_temp = []
                else:
                    comm_temp = soup.select('span.comm_body')

                comment = ''
                for k in range(len(comm_temp)):
                    comment = comment + comm_temp[k].get_text() + ' '

                # 추출된 내용 csv에 기록
                temp_list = [str(cnt+1), selectedMenu, tag, user,
                             title, content, comment]

                f = open(filename, 'a+', encoding='utf-8', newline='')
                wr = csv.writer(f)
                wr.writerow(temp_list)
                f.close()
            except Exception as ex2:
                print("Exception has been thrown"+str(ex2))
                driver.refresh()
                driver.implicitly_wait(20)
                continue

            # 데이터 횟수 증가
            cnt = cnt + 1
            print(cnt)

        # page로는 진행상황을 알 수 있고 cnt로는 몇개의 데이터를 모았는지 알 수 있음
        print([page, cnt])

        time.sleep(3)
