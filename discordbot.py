import discord         
import selenium_script                          # #페이스북 관련 import
import weather_bot
import library
import RiotSearch
import defaultFunction
import baekjoon
import webScraping
import move

intents = discord.Intents.default()  # 권한 설정
intents.message_content = True

client = discord.Client(intents=intents)
token = ''  # 토큰은 자신의 것으로 수정해야함
riot_token =""  # 본인 라이엇 api키 입력


@client.event
async def on_ready():  # when discord bot got ready
    print('Done.')
    await client.change_presence(status=discord.Status.online, activity=None)  # 봇 상태 온라인, 활동상태 없음
   
# 중심이 되는 메세지 박스
global mainmsg
mainmsg=None
@client.event
async def on_message(message): # 메세지 입력 시
    global mainmsg

    if message.author == client.user: # 봇이 입력한 경우
        return
    if message.author != client.user :
        print("discord에서 입력한 메세지 :", message.content)
    if message.content == "/최초화면": # 봇 시작, 또는 최초화면으로 돌아가기
        mainmsg = await defaultFunction.startBot(message, mainmsg)
    if message.content == "/이동":
        await move.channelPingPong(message)
    if message.content == "/채널삭제":
        await move.deleteChannel()
        # await move.channel()
    if message.content.startswith("/도서검색"):  #  /도서검색 {query}
        await library.library_search(message, client, mainmsg)
    if message.content.startswith("/페이스북"):
        await selenium_script.facebook_search(message, client, mainmsg)    
    if message.content.startswith("/날씨"):  # /날씨 {지역}
        await weather_bot.handle_weather_command(message, mainmsg)
    if message.content.startswith("/검색"):  # /검색 "소환사이름"
        await RiotSearch.search_summoner(message, riot_token, mainmsg) 
    if message.content.startswith("/백준기능설명"):
        await baekjoon.백준기능설명(mainmsg)
    if message.content.startswith("/백준기능"):
        await baekjoon.백준기능(message, mainmsg)
    if message.content.startswith("/식단"):
        mainmsg = await mainmsg.edit(content=webScraping.happiness_dormintory_diet(message.content))
    if message.content.startswith("/학사일정"):
        mainmsg = await mainmsg.edit(content=webScraping.academic_calendar())
    
       
client.run(token)