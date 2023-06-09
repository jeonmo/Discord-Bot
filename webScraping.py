import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def academic_calendar():
    # 웹 페이지에 대한 데이터를 요청
    response = requests.get('https://www.deu.ac.kr/www/academic_calendar')
    # 페이지 데이터를 텍스트형태로 변환
    page_data = response.text
    # html 파서 실행
    parsed = BeautifulSoup(page_data, 'html.parser') 
    # select 메서드로 col-12, col-md-6 클래스 2개를 포함하는 li태그를 리스트로 반환
    selectTag_li = parsed.select('li.col-12.col-md-6')

    # 태그를 제거하고 내용만 리스트에 저장
    selectTag_li_text = ""
    for tag in selectTag_li:
        selectTag_li_text += tag.get_text() + '\n'

    # 내용을 리스트형태로 반환
    return '```'+selectTag_li_text+'```'

import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def happiness_dormintory_diet(DayOfWeek: str = '2'):
    DayOfWeek=DayOfWeek.split()[1]
    # 크롬 드라이버 설정
    options = Options()
    options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행 (백그라운드 모드)
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

    try:
        # 사이트 접속하기
        driver.get('https://dorm.deu.ac.kr/deu/50/5050.kmc')
        time.sleep(1)
        # 식단표 날짜 선택
        driver.find_element(By.CSS_SELECTOR, '#tabDayA').click()
        # 식단표 부분만 선택
        table = driver.find_elements(By.CSS_SELECTOR, 'li#tab' + DayOfWeek)

        Info = []
        dietSubInfo = [['조식', '중식', '석식'], ['한식\n', '일품\n']]
        three = 0
        two = 0
        for dietInfo in table:
            for mle in ['_mor', '_lun', '_eve']:
                for ms in ['menu', 'sub']:
                    tmp = []
                    tmp.append(dietSubInfo[1][two % 2])
                    two += 1
                    tmp.append(dietInfo.find_element(By.CSS_SELECTOR, 'td' + '#fo_' + ms + mle + DayOfWeek).text)
                    Info.append(tmp)

        returningStr = '해당 요일의 메뉴는 다음과 같습니다.\n'
        for i in Info:
            for j in i:
                if j == '':
                    returningStr += '*없음*'
                else:
                    returningStr += str(j)
            returningStr += '\n\n'

        return "```"+returningStr+"```"

    finally:
        driver.quit()

# def happiness_dormintory_diet(DayOfWeek : str = '2'):
#     # 크롬 드라이버 생성
#     driver = webdriver.Chrome("C:\\Users\\wooji\\OneDrive\\바탕 화면\\study\\discordBot\\chormedriver\\chromedriver.exe")

#     # 사이트 접속하기
#     driver.get('https://dorm.deu.ac.kr/deu/50/5050.kmc')
#     # 접속 대기 시간 설정
#     driver.implicitly_wait(3)
#     # 식단표 날짜 선택
#     driver.find_element_by_css_selector('#tabDayA').click()
#     # 식단표 부분만 선택
#     table = driver.find_elements_by_css_selector('li#tab' + DayOfWeek)



#     Info = []
#     dietSubInfo = [['조식', '중식', '석식'], ['한식\n', '일품\n']]
#     three = 0
#     two = 0
#     for dietInfo in table:
#         for mle in ['_mor', '_lun', '_eve']:
#             for ms in ['menu', 'sub']:
#                 tmp = []
#                 tmp.append(dietSubInfo[1][two%2])
#                 two+=1
#                 tmp.append(dietInfo.find_element_by_css_selector('td' + '#fo_' + ms + mle + DayOfWeek).text)
#                 Info.append(tmp)

#     returningStr = '해당 요일의 메뉴는 다음과 같습니다.\n'
#     for i in Info:
#         for j in i:
#             if j == '':
#                 returningStr += '*없음*'
#             else:
#                 returningStr += str(j)
#         returningStr += '\n\n'
    
#     return returningStr


def DEU_Door_Recent(id : str, pw : str):
    # 크롬 드라이버 생성
    driver = webdriver.Chrome("C:\\Users\\wooji\\OneDrive\\바탕 화면\\study\\discordBot\\chormedriver\\chromedriver.exe")

    # 사이트 접속하기
    driver.get('https://door.deu.ac.kr/sso/login.aspx')
    # 접속 대기 시간 설정
    driver.implicitly_wait(3)
    # 로그인
    driver.find_element_by_css_selector('#logId').send_keys(id)
    driver.find_element_by_css_selector('#logPw').send_keys(pw)
    driver.find_element_by_css_selector('#btn_Login').click()
    driver.get('http://door.deu.ac.kr/MyPage')

    # 최근 공지사항
    recent = driver.find_element_by_css_selector('ul.mg10')
    return recent.text

def DEU_Door_Room(id : str, pw : str):
    # 크롬 드라이버 생성
    driver = webdriver.Chrome("C:\\Users\\wooji\\OneDrive\\바탕 화면\\study\\discordBot\\chormedriver\\chromedriver.exe")

    # 사이트 접속하기
    driver.get('https://door.deu.ac.kr/sso/login.aspx')
    # 접속 대기 시간 설정
    driver.implicitly_wait(3)
    # 로그인
    driver.find_element_by_css_selector('#logId').send_keys(id)
    driver.find_element_by_css_selector('#logPw').send_keys(pw)
    driver.find_element_by_css_selector('#btn_Login').click()
    driver.get('http://door.deu.ac.kr/MyPage')

    # 강의실 리스트
    room_div = driver.find_elements_by_css_selector('div.popupCon.mg_220_left.mg_10_top')
    for i in room_div:
        print(i.text)
    room_tr = driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[3]/div[3]/table/tbody')
    
    # 데이터사이언스 클래스 선택후 공지사항 출력
    driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[3]/div[3]/table/tbody/tr[7]/td[3]/a').click() # 2번째 td로 공지시항 선택
    driver.find_element_by_xpath('//*[@id="lnbContent"]/div/div[5]/ul/li/ul/li[1]/a').click() # 공지사항 버튼

    ds_announcement_page = driver.find_element_by_xpath('//*[@id="sub_content2"]/div[2]/table/tbody')

    return ds_announcement_page.text
    # //*[@id="wrap"]/div[2]/div[3]/div[3]/table/tbody/tr[1]
    # //*[@id="wrap"]/div[2]/div[3]/div[3]/table/tbody/tr[2]/td[3]/a
def test():
    # 크롬 드라이버 생성
    driver = webdriver.Chrome("C:\\Users\\wooji\\OneDrive\\바탕 화면\\study\\discordBot\\chormedriver\\chromedriver.exe")

    # 사이트 접속하기
    driver.get('https://lib.deu.ac.kr/data_view.mir?ebscohostsearchtexttemp=%EC%9E%90%EB%B0%94&ebscohostsearchtexttemp=%EC%9E%90%EB%B0%94&search_keyword1=%EC%9E%90%EB%B0%94&search_keyword2=&search_keyword3=&search_keyword_type1=text&search_keyword_type2=&search_keyword_type3=&srch_condi_01=&srch_condi_02=&page_num=1&scope_code=&mtype_code=&srch_type=kw&search_re_yn=&search_keyword_re=&search_keyword_type_re=&search_keyword_type1_re_add=&search_keyword1_re_add=&facet_limit_search_field_code=&facet_limit_search_start_pub_year=&facet_limit_search_end_pub_year=&srch_mloc=&rno=87054&hloc_code=FI&all_hloc_code=&serial_hloc_code=')
    # 접속 대기 시간 설정
    driver.implicitly_wait(3)
    driver.set_window_size(800, 600)
    
    elements = driver.find_elements_by_css_selector('td')
    num = 1
    for i in elements:
      print(i.text)

    time.sleep(50)

