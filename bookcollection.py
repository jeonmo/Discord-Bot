import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def book_bestSeller():

    url = "https://lib.deu.ac.kr/sb/recommend_bestseller_list.mir"
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CSS_SELECTOR,'dt')

    book_no = 0
    book_list_str = '```cs\n#동의대 컬렉션의 베스트셀러입니다.\n'
    book_list_str += "#중앙도서관에서는 여러 매체를 참고하여 선정된 베스트셀러를 이용 접근성과 효율성을 위해 2F 북카페 내 베스트셀러 코너에 설치하여 운영하고 있다.\n"

    
    for x in book_element :
        book_no += 1
        if book_no >= 7:
            book_list_str += "- "
            book_list_str += x.text
            book_list_str += "\n"

    book_list_str += "\n#자세한 책의 정보는 도서검색 기능을 이용해주세요.```"

    dr.quit()
    return book_list_str



def book_recommended():

    url = "https://lib.deu.ac.kr/sb/recommend_refinement100_list.mir"
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CSS_SELECTOR,'dt')

    book_no = 0
    book_list_str = '```cs\n#동의대 컬렉션의 동의대권장도서입니다.\n'
    book_list_str += "#본교생들의 독서의욕을 고취하고 양질의 독서를 통한 교양함양과 지적 성장을 지원하며 도서관 이용 및 독서 활동을 도모하기 위하여 동의대학교 동의지천교양대학에서 선정한 교양100선과 학과(학부)에서 추천한 전공교양도서를 비치하여 대학생들의 길잡이 역할을 하고자 한다. (소장위치: 2F 권장도서코너)\n"
    for x in book_element :
        book_no += 1
        if book_no >= 7:
            book_list_str += "- "
            book_list_str += x.text
            book_list_str += "\n"

    book_list_str += "\n#자세한 책의 정보는 도서검색 기능을 이용해주세요.```"

    dr.quit()
    return book_list_str



def book_oneBookOneBusan():

    url = "https://lib.deu.ac.kr/sb/recommend_onebookone_list.mir"
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CSS_SELECTOR,'dt')

    book_no = 0
    book_list_str = '```cs\n#동의대 컬렉션의 원북원부산도서입니다.\n'
    book_list_str += "#원북원부산 도서는 한 권의 책을 통해 지역사회가 하나가 된다는 취지로 1998년 미국 시애틀에서 시작된 '원북원 시티(One Book One city)'운동을 모델로 하여 2004년부터 부산에서 시행된 것으로, 해마다 권장 교양 도서 한 권을 선정해 함께 읽고 토론하는 부산지역 시민 독서 생활 운동 도서입니다. (소장위치: 2F 원북원부산도서코너)\n"
    for x in book_element :
        book_no += 1
        if book_no >= 7:
            book_list_str += "- "
            book_list_str += x.text
            book_list_str += "\n"

    book_list_str += "\n#자세한 책의 정보는 도서검색 기능을 이용해주세요.```"

    dr.quit()
    return book_list_str

def book_trend():

    url = "https://lib.deu.ac.kr/sb/recommend_trendbook_list.mir"
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CSS_SELECTOR,'dt')

    book_no = 0
    book_list_str = '```cs\n#동의대 컬렉션의 특성화(트렌드)도서입니다.\n'
    book_list_str += "#중앙도서관에서는 이용자의 관심이 높거나 최신 트렌드에 맞는 특정 분야의 자료를 개발 및 구입하여 도서관 이용자들에게 다양한 정보를 제공하고 있음\n"
    for x in book_element :
        book_no += 1
        if book_no >= 7:
            book_list_str += "- "
            book_list_str += x.text
            book_list_str += "\n"

    book_list_str += "\n#자세한 책의 정보는 도서검색 기능을 이용해주세요.```"

    dr.quit()
    return book_list_str



def book_bookCuration():

    url = "https://lib.deu.ac.kr/sb/recommend_bookcuration_list.mir?search_sort_type=title"
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CSS_SELECTOR,'dt')

    book_no = 0
    book_list_str = '```cs\n#동의대 컬렉션의 북큐레이션입니다.\n'
    for x in book_element :
        book_no += 1
        if book_no >= 7:
            book_list_str += "- "
            book_list_str += x.text
            book_list_str += "\n"

    book_list_str += "\n#자세한 책의 정보는 도서검색 기능을 이용해주세요.```"

    dr.quit()
    return book_list_str
