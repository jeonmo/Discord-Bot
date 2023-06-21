import discord         
import selenium_script                          # #페이스북 관련 import
import weather_bot
import library
import RiotSearch
import defaultFunction
import baekjoon
import webScraping
import move
import Notice

intents = discord.Intents.default()  # 권한 설정
intents.message_content = True

client = discord.Client(intents=intents)
token = 'MTEwMDk4NDQwMTQyMjIwMDg3NA.Gh6g-_.DnsGeYSbF8xVBxVDUWDQuIZ_TEA_kvLMCbRDpI'  # 토큰은 자신의 것으로 수정해야함
riot_token ="RGAPI-54517728-5e08-4beb-95d6-6c4b5dfb132a"  # 본인 라이엇 api키 입력


@client.event
async def on_ready():  # when discord bot got ready
    print('Done.')
    await client.change_presence(status=discord.Status.online, activity=None)  # 봇 상태 온라인, 활동상태 없음
   
# 중심이 되는 메세지 박스 딕셔너리
global mainmsg
mainmsg={}
global longmsg # 페이스북 등 긴 메세지 출력 시 사용
longmsg=[]

@client.event
async def on_message(message): # 메세지 입력 시
    global mainmsg
    global buttons
    global longmsg
    buttons = [
        {"custom_id": "Button 1", "label": "최초화면(사용방법)"},
        {"custom_id": "Button 2", "label": "학사일정"},
        {"custom_id": "Button 3", "label": "페이스북 확인"},
        {"custom_id": "Button 4", "label": "부산 날씨"},
        {"custom_id": "Button 5", "label": "백준 기능"},
        {"custom_id": "Button 6", "label": "기숙사 식단"},
        {"custom_id": "Button 7", "label": "공지사항"}
    ]
    if message.author == client.user: # 봇이 입력한 경우
        return
    if message.author != client.user :
        print("discord에서 입력한 메세지 :", message.content)
    if len(longmsg)>0:
        for msg in longmsg:
            try:
                await msg.delete()
            except discord.errors.NotFound:
                pass
        longmsg = []
    if message.author not in mainmsg:
        msg = await move.newChannel(message, mainmsg, client)
        mainmsg[message.author]=msg
        await defaultFunction.startBot(mainmsg, message.author)

        button_style = discord.ButtonStyle.primary
        view = discord.ui.View()
        for button_info in buttons:
            button = discord.ui.Button(label=button_info['label'], style=button_style, custom_id=button_info['custom_id'])
            view.add_item(button)
        await mainmsg[message.author].edit(view=view)
    else:
        if mainmsg[message.author].embeds:
            await mainmsg[message.author].edit(embed=None)
        if message.content.startswith("/도서검색"):  #  /도서검색 {query}
            await library.library_search(message, client, mainmsg[message.author])
        if message.content.startswith("/도서추천"):
            mainmsg[message.author] = await library.library_collection(message, client, longmsg, mainmsg[message.author])
            print(mainmsg[message.author].content)
        if message.content.startswith("/페이스북"):
            await selenium_script.facebook_search(message, longmsg, mainmsg[message.author])    
        if message.content.startswith("/날씨"):  # /날씨 {지역}
            await weather_bot.handle_weather_command(message, mainmsg[message.author])
        if message.content.startswith("/검색"):  # /검색 "소환사이름"
            await RiotSearch.search_summoner(message, riot_token, longmsg) 
        if message.content.startswith("/백준기능설명"):
            await baekjoon.백준기능설명(mainmsg[message.author])
        if message.content.startswith("/백준기능"):
            await baekjoon.백준기능(message, mainmsg[message.author])
        if message.content.startswith("/식단"):
            await webScraping.happiness_dormintory_diet(message.content, message)
        if message.content.startswith("/학사일정"):
            await webScraping.academic_calendar(mainmsg, message)
        await message.delete()
    

@client.event
async def on_interaction(interaction):
    global longmsg
    if len(longmsg)>0:
        for msg in longmsg:
            try:
                await msg.delete()
            except discord.errors.NotFound:
                pass
        longmsg = []
    if mainmsg[interaction.user].embeds:
        await mainmsg[interaction.user].edit(embed=None)
    if interaction.type == discord.InteractionType.component:
        for button_info in buttons:
            if interaction.data['custom_id'] == button_info['custom_id']:
                if button_info['custom_id']=='Button 1': # 기본화면
                    await interaction.response.defer()
                    await defaultFunction.startBot(mainmsg, interaction.user)
                elif button_info['custom_id']=='Button 2': # 학사일정
                    await interaction.response.defer()
                    await webScraping.academic_calendar(mainmsg, interaction.user)
                elif button_info['custom_id']=='Button 3': # 페이스북
                    await interaction.response.defer()
                    longmsg = await selenium_script.facebook_search(longmsg, mainmsg[interaction.user])
                elif button_info['custom_id']=='Button 4': # 부산날씨
                    await interaction.response.defer()
                    await weather_bot.handle_weather_command("부산", mainmsg[interaction.user])
                elif button_info['custom_id']=='Button 5': # 백준 기능
                    await interaction.response.defer()
                    await baekjoon.백준기능설명(mainmsg[interaction.user])
                elif button_info['custom_id']=='Button 6': # 식단
                    await interaction.response.defer()
                    await webScraping.happiness_dormintory_diet(mainmsg[interaction.user])
                elif button_info['custom_id']=='Button 7': # 공지사항
                    await interaction.response.defer()
                    await Notice.get_notice_information(mainmsg[interaction.user])
client.run(token)