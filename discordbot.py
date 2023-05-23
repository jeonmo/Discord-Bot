import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

def book_check(m): # 도서검색의 wait_for에 사용되는 check 함수
    return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5' or m.content == '6' or m.content == '7' or m.content == '8' or m.content == '9' or m.content == '10'

intents = discord.Intents.default()  # 권한 설정
intents.message_content = True

client = discord.Client(intents=intents)
token = 'MTEwMjc0ODU3MzQ2MTkyMTg4Mw.G4vATq.mIblLeuuEOoh0mdpqd2eOrhCgBLPSSkNW0NKbY'  # 토큰 입력 필요

@client.event
async def on_ready():  # when discord bot got ready
    print('Done')
    await client.change_presence(status=discord.Status.online, activity=None)  # 봇 상태 온라인, 활동상태 없음
   
@client.event
async def on_message(message): # 메세지 입력 시
    functionNum = 0
    if message.author == client.user: # 봇이 입력한 경우
        return
    if message.author != client.user :
        print("discord에서 입력한 메세지 :", message.content)


    if message.content == "안녕하세요": # 메세지 내용이 안녕하세요 일때
        await message.channel.send("반갑습니다") # 반갑습니다 라는 내용을 채널에 입력
    if message.content == "안녕하세요!": # 메세지 내용이 안녕하세요 일때
        await message.channel.send("반갑습니다!") # 반갑습니다 라는 내용을 채널에 입력
    if message.content == "스트림":
        await message.channel.send("스트림합니다")
        await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name='스트리밍', url='https://www.twitch.tv/ajehr'))
    if message.content == "중지":
        await message.channel.send("현재 활동을 중지합니다")
        await client.change_presence(status=discord.Status.online, activity=None)
        

    if "도서검색" in message.content: # 메세지 내용이 안녕하세요 일때
        msg = message.content.split()
        book = msg[1]

        url = "https://lib.deu.ac.kr/data_data_list.mir?search_keyword_type1=title&search_keyword1=" + book
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

        if book_list_str != '':
            await message.channel.send(book + "의 검색 결과입니다.\n```" + book_list_str + '```' + '소장사항을 보길 원하는 도서의 번호를 입력해주세요.')

            input_no_msg = await client.wait_for('message', check=book_check)
            input_no = input_no_msg.content # 사용자로부터 입력받은 메세지

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

                #elements 로 여러개 출력하는 것이 안됨, 나중에 고칠 것
                #book_info_element = dr.find_element(By.CLASS_NAME,'table_data_view_list').text
                #await message.channel.send('도서 정보입니다. ```' + book_info_element + '```')
                
                # book_info_element = dr.find_elements(By.CSS_SELECTOR,'td.table_data_view_list')
                #book_info_element = dr.find_elements_by_css_selector('td')
                
                #for i in book_info_element:
                #    print('리스트:', i.text)
                #time.sleep(1000)   
                #await message.channel.send('도서 정보입니다. ```' + book_info_element + '```')
                
                # 접속 대기 시간 설정
                dr.implicitly_wait(3)
                dr.set_window_size(800, 600)

                elements = dr.find_elements_by_css_selector('td.table_data_view_list')
                book_detail_str = '```'
                for i in elements:
                    book_detail_str += i.text
                    book_detail_str += "\n──────────────────────────\n"
                book_detail_str += '```'
                book_result_str = '해당 도서의 소장사항입니다.\n'

                # 소장사항이 하나라도 존재할 경우
                if book_detail_str != '``````': 
                    book_result_str += book_detail_str
                    await message.channel.send(book_result_str)
                
                else:
                    book_result_str += '```해당 도서는 중앙도서관에서 소장 중이지 않습니다.```'
                    await message.channel.send(book_result_str)
            
            else :
                await message.channel.send("올바른 값이 아닙니다.")

        else :
            await message.channel.send('검색 결과가 없습니다.')
        
        dr.quit()

client.run(token)