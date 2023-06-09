async def startBot(message, mainmsg):  # 기능 설명, 최초화면 생성  
    if mainmsg==None:
        return await message.channel.send("```**/최초화면**을 입력하면 언제든지 현재 화면으로 복귀합니다.\n명령어 목록\n1. /도서검색 [검색키워드]\n2. /날씨 [지역이름]\n3. /페이스북\n4. /검색 [소환사명]\n5. /백준기능설명```")
    else:
        return await mainmsg.edit(content="```**/최초화면**을 입력하면 언제든지 현재 화면으로 복귀합니다.\n명령어 목록\n1. /도서검색 [검색키워드]\n2. /날씨 [지역이름]\n3. /페이스북\n4. /검색 [소환사명]\n5. /백준기능설명```")