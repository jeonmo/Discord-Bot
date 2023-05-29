import discord
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import booksearch
from discord.ext import commands                #페이스북 관련 import
from selenium_script import perform_facebook_search # #페이스북 관련 import
import weather_bot
import json
import library

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
       
     if "페이스북" in message.content:          #페이스북을 검색하는 
        results = perform_facebook_search()
        if results:
            for result in results:
                await message.channel.send(result)  # 디스코드에 결과를 전송합니다.
        else:
            await message.channel.send('페이스북 피드를 찾을 수 없습니다.')
            
    if message.content == "동의대 공지사항"  # "동의대 공지사항" 메시지가 도착하면 공지사항 정보를 가져와서 전송
    
        result = await get_notice_information()
        await message.channel.send(result)

    await bot.process_commands(message)
            
    await weather_bot.handle_weather_command(message) # 날씨 명령어 처리
    
 @client.event
async def on_message(message):     # Riot소환사 정보 검색
    await search_summoner(message, "YOUR_RIOT_API_TOKEN")

client.run(token)
