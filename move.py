import discord
import time
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