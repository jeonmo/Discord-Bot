import DB
async def 백준기능설명(mainmsg):
    await mainmsg.edit(content='```/백준기능 [명령어] [인자]를 통해 사용합니다.\n명령어는 문제번호, 문제설명, 백준팁추가 3가지가 존재합니다.\n예시\n/백준기능 문제번호 1000\n/백준기능 문제설명 1000\n/백준기능 백준팁추가 1000 [추가할 내용]```')

async def 백준기능(message, mainmsg):
    query = message.content.split()
    print(query)
    ctx = query[1] # 명령어
    query = query[2:] # 인자

    if ctx.startswith("문제번호"):
        await 문제번호(message, query[0], mainmsg)
    if ctx.startswith("문제설명"):
        await 문제설명(message, query[0], mainmsg)
    if ctx.startswith("백준팁추가"):
        await 백준팁추가(message, mainmsg, query)
    

async def 문제번호(ctx, query: str, mainmsg):
    # try:
    if query.isdigit():
        mainmsg = await mainmsg.edit(content=f"문제설명은 **/백준기능 문제설명 {query}**를 입력하세요\n```{DB.retrieve_data_by_id(query)}```")
    else:
        print('제목으로 검색 아직 미완성입니다.')
    # except:
    #     mainmsg = await mainmsg.edit(content='```오류 발생```')
    # finally:
    #     await ctx.message.delete()

async def 문제설명(ctx, query: str, mainmsg):
    try:
        if query.isdigit():
            mainmsg = await mainmsg.edit(content=f"```{DB.problem_info(query)}```")
        else:
            print('문제명으로 검색 미지원')
    except:
        mainmsg = await mainmsg.edit(content='```오류 발생```')
    # finally:
    #     await ctx.message.delete()



async def 백준팁추가(mainmsg, *, querys:str):
    try:
        querys = querys.split()
        DB.append_column_value(int(querys[0]), 'tips', querys[1:])
        mainmsg = await mainmsg.edit(content=f"```추가된 팁{querys[1:]}```")
    except:
        mainmsg = await mainmsg.edit(content='```재실행 바랍니다.```')
    # finally:
    #     await ctx.message.delete()
