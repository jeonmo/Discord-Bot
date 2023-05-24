import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import booksearch

def book_check(m): # 도서검색의 wait_for에 사용되는 check 함수
    return m.content
    #return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5' or m.content == '6' or m.content == '7' or m.content == '8' or m.content == '9' or m.content == '10'

intents = discord.Intents.default()  # 권한 설정
intents.message_content = True

client = discord.Client(intents=intents)
token = 'MTEwMjc0ODU3MzQ2MTkyMTg4Mw.G_TW_w.2iCczzVUi1CzsG1UGEGBjrj1RYzXZi3zBAt5nc'  # 토큰 입력 필요

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
        

    if "도서검색" in message.content: 
        book_list_str, book = booksearch.book_list_search(message.content)

        if book_list_str != '':
            await message.channel.send(book + "의 검색 결과입니다.\n```" + book_list_str + '```' + '소장사항을 보길 원하는 도서의 번호를 입력해주세요.')

            input_no_msg = await client.wait_for('message', check=booksearch.book_check)
            input_no = input_no_msg.content # 사용자로부터 입력받은 메세지

            book_rental_msg = booksearch.book_rental_check(input_no)

            await message.channel.send(book_rental_msg)
        else :
            await message.channel.send('검색 결과가 없습니다.')
        
        

client.run(token)