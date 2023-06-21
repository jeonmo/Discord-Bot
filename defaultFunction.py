async def startBot(mainmsg, author):  # 기능 설명, 최초화면 생성  
    await mainmsg[author].edit(content="```디스코드 봇 기본화면입니다.\n명령어 목록\n1. /도서검색 [검색키워드]\n2. /날씨 [지역이름]\n3. /도서추천\n4. /검색 [소환사명]```")
    