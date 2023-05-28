import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

url = "https://www.deu.ac.kr/www/board/3/1"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # 봇이 준비되었을 때 호출되는 이벤트 핸들러
    print(f'봇이 로그인했습니다. (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    # 메시지가 도착했을 때 호출되는 이벤트 핸들러
    if message.author.bot:
        return

    if message.content == "동의대 공지사항":
        # "동의대 공지사항" 메시지가 도착하면 공지사항 정보를 가져와서 전송
        result = await get_notice_information()
        await message.channel.send(result)

    await bot.process_commands(message)

async def get_notice_information():
    # 공지사항 정보를 가져오는 비동기 함수
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    notice_rows = soup.find_all("tr")
    result = ""

    for row in notice_rows:
        columns = row.find_all("td")

        if len(columns) > 0:
            # 각 행에서 필요한 정보 추출
            serial_number_element = row.find("th", {"scope": "row"})
            serial_number = serial_number_element.text.strip() if serial_number_element else "N/A"
            title_element = columns[0].find("a")
            title = title_element.text.strip() if title_element else "N/A"
            author = columns[1].text.strip() if len(columns) > 1 else "N/A"
            date = columns[2].text.strip() if len(columns) > 2 else "N/A"
            views = columns[3].text.strip() if len(columns) > 3 else "N/A"

            # 정보를 포맷팅하여 결과 문자열에 추가
            result += f"순번: {serial_number}\n제목: {title}\n작성자: {author}\n작성일: {date}\n조회수: {views}\n-------------------\n"

    return result

bot.run('MTEwMzc4MDIxMzkwNjczNTE0NA.GwF9Im.3JNSiieH36Se7Vfi-pQ7c36ErAWDS0rErgmDco')
