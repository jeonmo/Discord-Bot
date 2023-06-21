import discord
import time

async def newChannel(message, mainmsg, client):
    if not mainmsg:  # 이미 생성된 텍스트 채널이 없는 경우
        guild = message.guild  # 현재 서버의 정보 가져오기
        await deduplication(str(message.author).split('#'), guild, client) # 채널 생성 때는 #이 들어가지 않지만, 유저 이름에는 # 존재함.
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  # 모든 사용자의 읽기 권한 제한
            message.author: discord.PermissionOverwrite(read_messages=True)  # 명령어를 입력한 사용자만 읽기 권한 부여
        }
        
        channel = await guild.create_text_channel(name=f"{message.author}", overwrites=overwrites)  # 텍스트 채널 생성
        mainmsg = f"프라이빗 채널이 생성되었습니다. 채널 이름: {channel.mention}"
        await message.channel.send(mainmsg)  # 메인 채널에 메시지 전송
    
        hello_msg = "hello"  # 보낼 메시지
        mainmsg = await channel.send(hello_msg)  # 생성된 채널로 메시지 전송
        
    return mainmsg

async def deduplication(channel_name, guild, client):
    if guild:
        channel_name=channel_name[0]+channel_name[1] # 유저#1234 를 유저1234로 변경
        channels = [channel for channel in guild.channels if channel.name == channel_name]  # 채널 이름이 일치하는 모든 채널 찾기
        if len(channels) >= 1:
            for channel in channels:
                await channel.delete()  # 찾은 모든 채널 삭제
            return f"{len(channels)}개의 채널이 삭제되었습니다."
        else:
            return "일치하는 채널이 없습니다."
    else:
        return "해당 서버를 찾을 수 없습니다."

#--------------------------- 안쓰는 코드
async def channelPingPong(message):  # 새 채널 만들고 이동시켰다가 다시 원래대로 두기
    new_channel = await moveToNewVoiceChannel(message, '인생')
    time.sleep(5)
    await moveUser(message, message.channel, message.author)
    await deleteChannel(new_channel.channel.name, message)

async def moveToNewVoiceChannel(message, user_name):  # 새 채널 만들고 이동시키기
    # 새로운 보이스 채널 생성
    new_channel=createNewVoiceChannel(message, '임시채널')
    # 특정 유저들을 새로운 보이스 채널로 이동
    await moveUser(message, new_channel, user_name)
    return new_channel

async def createNewVoiceChannel(message, channel_name):  # 새채널 만들기
    # 새로운 보이스 채널 생성
    guild = message.guild
    new_channel = await guild.create_voice_channel(channel_name)
    return new_channel

async def moveUser(message, channel, user_name:list):  # 유저 이동시키기
    # 특정 유저들을 새로운 보이스 채널로 이동
    target_users = [discord.utils.get(message.guild.members, name=un) for un in user_name] #, discord.utils.get(guild.members, name='유저2')
    for user in target_users:
        await user.move_to(channel)

async def findUser(message, channelName: str, userName: str):  # 채널 이름과 유저 이름으로 유저 찾기
    target_channel = discord.utils.get(message.guild.channels, name=channelName, type=discord.ChannelType.voice)
    if target_channel:
        target_user = discord.utils.get(target_channel.members, name=userName)
        if target_user:
            return target_user
        else:
            return None
    else:
        return None

async def deleteChannel(channelName, message):  # 채널 이름으로 채널 삭제
    # 채널을 찾아서 삭제
    target_channel = discord.utils.get(message.guild.channels, name=channelName)
    if target_channel:
        await target_channel.delete()
        await message.channel.send(f'채널 {channelName}이 삭제되었습니다.')
    else:
        await message.channel.send(f'채널 {channelName}을 찾을 수 없습니다.')

async def checkUserInVoiceChannel(message):  # 메세지 보낸 이 찾기
    author = message.author
    voice_state = author.voice

    if voice_state is None:  # 보이스 채널에 없으면
        return [author]  # 보낸 이 정보
    else:  # 보이스 채널에 있으면
        voice_channel = voice_state.channel
        return [author, voice_channel]  # 보낸 이 정보, 보이스 채널 정보