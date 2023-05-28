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
            
    await weather_bot.handle_weather_command(message) # 날씨 명령어 처리
    
    if message.content.startswith("/검색 "):
        UserName = message.content.replace("/검색 ", "")  
        UserInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + UserName
        res = requests.get(UserInfoUrl, headers={"X-Riot-Token":riot_token})
        resjs = json.loads(res.text)

        if res.status_code == 200:
            UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/13.10.1/img/profileicon/{}.png"  # 패치될떄 버전 수정
            embed = discord.Embed(title=f"{resjs['name']} 님의 플레이어 정보", description=f"**{resjs['summonerLevel']} LEVEL**", color=0xFF9900)

            UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + resjs["id"]
            res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token":riot_token})
            res_2js = json.loads(res_2.text)

            if res_2js == []: # 언랭크일때
                embed.add_field(name=f"{resjs['name']} 님은 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)

            else: # 언랭크가 아닐때
                for rank in res_2js:
                    if rank["queueType"] == "RANKED_SOLO_5x5":
                        embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

                    else:
                        embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

            embed.set_author(name=resjs['name'], url=f"http://fow.kr/find/{UserName.replace(' ', '')}", icon_url=UserIconUrl.format(resjs['profileIconId']))
            await message.channel.send(embed=embed) # UserName에 띄워쓰기 제거

        else: # 존재하지 않는 소환사일때, 오류코드 4??
            error = discord.Embed(title="존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.", color=0xFF9900)
            await message.channel.send(embed=error)

client.run(token)
