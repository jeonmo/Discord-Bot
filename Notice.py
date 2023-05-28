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
    print(f'봇이 로그인했습니다. (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "동의대 공지사항":
        # URL로 GET 요청 보내기
        response = requests.get(url)

        # HTML 콘텐츠를 구문 분석할 BeautifulSoup 개체 만들기
        soup = BeautifulSoup(response.content, "html.parser")

        # 공지사항 행을 포함하는 요소 찾기
        notice_rows = soup.find_all("tr")

        # 공지사항 행을 순회하며 정보 추출
        for row in notice_rows:
            # 행 내부 요소 찾기
            columns = row.find_all("td")

            # 공지 정보가 포함된 행인지 확인
            if len(columns) > 0:
                # 공지의 일련번호, 제목, 작성자, 날짜, 조회수 추출
                serial_number_element = row.find("th", {"scope": "row"})
                serial_number = serial_number_element.text.strip() if serial_number_element else "N/A"

                title_element = columns[0].find("a")
                title = title_element.text.strip() if title_element else "N/A"

                author = columns[1].text.strip() if len(columns) > 1 else "N/A"

                date = columns[2].text.strip() if len(columns) > 2 else "N/A"

                views = columns[3].text.strip() if len(columns) > 3 else "N/A"

                # 추출한 정보를 포맷팅
                result = f"순번: {serial_number}\n제목: {title}\n작성자: {author}\n작성일: {date}\n조회수: {views}\n-------------------"

                # 결과를 메시지로 전송
                await message.channel.send(result)

    await bot.process_commands(message)

bot.run('MTEwMzc4MDIxMzkwNjczNTE0NA.GmYuFo.sCrI_YlfaVFqe-pI8LU_nTCu5TKHGjxIdsTSPg')
