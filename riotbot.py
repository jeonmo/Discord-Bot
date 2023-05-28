import requests
import json
import discord

async def search_summoner(message, riot_token):
    if message.content.startswith("/검색 "):
        UserName = message.content.replace("/검색 ", "")
        UserInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + UserName  # 변수명 + 디스코드에서 사용자가 입력한 소환사 명
        res = requests.get(UserInfoUrl, headers={"X-Riot-Token": riot_token})  # url에 접근하기 위한 header정보 필요, header = riot_token(api key)
        resjs = json.loads(res.text)

        if res.status_code == 200:    # 올바른 소환사 명 입력시 서버상태 코드인 200출력
            UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/13.10.1/img/profileicon/{}.png"  # 패치 버전에 맞게 수정
            embed = discord.Embed(title=f"{resjs['name']} 님의 플레이어 정보", description=f"**{resjs['summonerLevel']} LEVEL**", color=0xFF9900)

            UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + resjs["id"]  #랭크정보와 관련된 api, resjs["id"]로 소환사정보 출력
            res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token": riot_token})  # url에 접근하기 위한 header정보 필요, header = riot_token(api key)
            res_2js = json.loads(res_2.text)

            if res_2js == []:  # 언랭크일떄   # 자유랭크,솔로랭크 정보가 없을떄 [] 빈리스트를 출력함.
                embed.add_field(name=f"{resjs['name']} 님은 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)
            
            else:   # 언랭크가 아닐떄
                for rank in res_2js:
                    if rank["queueType"] == "RANKED_SOLO_5x5":
                        embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                    else:
                        embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)
                                                                                                                                            
            embed.set_author(name=resjs['name'], url=f"http://fow.kr/find/{UserName.replace(' ', '')}", icon_url=UserIconUrl.format(resjs['profileIconId']))  
            await message.channel.send(embed=embed)  # UserName 띄워쓰기 제거

        else:  # 존재하지 않는 소환사일떄, 없는 소환사 명은 오류코드 4?? 출력
            error = discord.Embed(title="존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.", color=0xFF9900)
            await message.channel.send(embed=error)
