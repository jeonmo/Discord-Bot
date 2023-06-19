import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import booksearch
from discord.ext import commands                #페이스북 관련 import
import selenium_script                          # #페이스북 관련 import
import weather_bot
import json
import library
import RiotSearch

intents = discord.Intents.default()  # 권한 설정
intents.message_content = True

client = discord.Client(intents=intents)
token = 'MTEwMjc0ODU3MzQ2MTkyMTg4Mw.GvcvAO.L6-fSusJvexvzoi65zOGGlraIvnS3bR3Cly_7U'  # 토큰은 자신의 것으로 수정해야함
riot_token =" "  # 본인 라이엇 api키 입력

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
        await library.library_search(message, client)
    
    if "페이스북" in message.content:
        await selenium_script.facebook_search(message, client)

    # 중앙도서관 도서추천 기능 추가했습니다. (discordbot.py에 if문 추가, library에 library_collection 함수 추가 및 bookcollection 임포트, bookcollection 코드 추가) 
    if "도서추천" in message.content: 
        await library.library_collection(message, client)    
     
    if "동의대 공지사항" in message.content:
        result = await get_notice_information()
        await message.channel.send(result)
        
    if message.content.startswith("날씨"):
        await weahter_bot.handle_weather_command(message)
    
    if message.content.startswith("/검색 "):
        await RiotSearch.search_summoner(message, riot_token)
            
client.run(token)
