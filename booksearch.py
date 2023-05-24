import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

def book_check(m): # 도서검색의 wait_for에 사용되는 check 함수
    return m.content
    #return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5' or m.content == '6' or m.content == '7' or m.content == '8' or m.content == '9' or m.content == '10'


def book_list_search(message):
    # book_list_str은 디스코드 봇이 메시지로 사용할 책 리스트 문자열입니다.
    # book은 검색어 이름입니다. (ex) 도서검색 자바 --> book == '자바'
    # book_list_search 함수는 메시지로 사용할 책 리스트 문자열과 검색어 제목을 반환합니다.

    msg = message.split() 
    book = msg[1]

    url = "https://lib.deu.ac.kr/data_data_list.mir?search_keyword_type1=title&search_keyword1=" + book
    global dr
    dr = webdriver.Chrome()
    dr.get(url) 

    act = ActionChains(dr)
        
    book_element = dr.find_elements(By.CLASS_NAME,'book_title')

    book_no = 0
    book_list_str = ''
    for x in book_element :
        book_no += 1
        book_list_str += str(book_no)
        book_list_str += ". \t"
        book_list_str += x.text
        book_list_str += "\n"

    return book_list_str, book

def book_rental_check(input_no):

    if input_no == '1' or input_no == '2' or input_no == '3' or input_no == '4' or input_no == '5' or input_no == '6' or input_no == '7' or input_no == '8' or input_no == '9' or input_no == '10' :
        if input_no == '1':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[1]/td[3]/a').click()
        elif input_no == '2':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[3]/td[3]/a').click()
        elif input_no == '3':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[5]/td[3]/a').click()
        elif input_no == '4':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[7]/td[3]/a').click()
        elif input_no == '5':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[9]/td[3]/a').click()
        elif input_no == '6':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[11]/td[3]/a').click()
        elif input_no == '7':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[13]/td[3]/a').click()
        elif input_no == '8':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[15]/td[3]/a').click()
        elif input_no == '9':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[17]/td[3]/a').click()
        elif input_no == '10':
            book_click_element = dr.find_element(By.XPATH,'//*[@id="content_data"]/form/div[4]/table/tbody/tr[19]/td[3]/a').click()

        dr.implicitly_wait(3)
        dr.set_window_size(800, 600)

        elements = dr.find_elements_by_css_selector('td.table_data_view_list')
        book_detail_str = '```'
        for i in elements:
            book_detail_str += i.text
            book_detail_str += "\n──────────────────────────\n"
        book_detail_str += '```'
        book_result_str = '해당 도서의 소장사항입니다.\n'

        if book_detail_str != '``````': 
            book_result_str += book_detail_str
            

        else:
            book_result_str += '```해당 도서는 중앙도서관에서 소장 중이지 않습니다.```'


        dr.quit()
        return book_result_str
    
    else:

        dr.quit()
        book_result_str = "올바른 값이 아닙니다."
        return book_result_str
