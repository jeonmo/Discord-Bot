import math
import requests
import json
import discord
from datetime import datetime, timedelta

def get_coordinates(city):
   # 주어진 도시 이름으로 위도와 경도를 추출하는 함수
   # OpenStreetMap의 Nomination API를 사용해 주어진 도시의 좌표를 검색
   # Args:
   #     city(str): 도시 이름
   # Returns:
   #     float: 추출된 위도
   #     float: 추출된 경도

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data:
        place = data[0]
        lat = float(place["lat"])
        lon = float(place["lon"])
        return lat, lon

    return None, None

def convert_to_grid(lat, lon):  
    # 위도와 경도를 기상청 좌표 체계로 변환하는 함수
    # Args:
    #     lat (float): 위도
    #     lon (float): 경도
    # Returns:
    #     int: 변환된 x 좌표
    #     int: 변환된 y 좌표

    NX = 149
    NY = 253
    Re = 6371.00877
    grid = 5.0
    slat1 = 30.0
    slat2 = 60.0
    olon = 126.0
    olat = 38.0
    xo = 210 / grid
    yo = 675 / grid
    first = 0

    if first == 0:
        PI = math.asin(1.0) * 2.0
        DEGRAD = PI / 180.0
        RADDEG = 180.0 / PI

        re = Re / grid
        slat1 = slat1 * DEGRAD
        slat2 = slat2 * DEGRAD
        olon = olon * DEGRAD
        olat = olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        first = 1

    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI:
        theta -= 2.0 * PI
    if theta < -PI:
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def get_forecast_temperature(x, y): 
    # 기상청 날씨 예보 정보를 조회하여 날씨 정보를 반환하는 함수
    # Args:
    #     x (int): 변환된 x 좌표
    #     y (int): 변환된 y 좌표
    # Returns:
    #     str: 날씨 정보 결과 문자열

    service_key = "0ZgOGSd8egwTu+X57LKlm6sVYmaOl5ENiwN/wtS2KVVBwdfNNpJlluUKqL+4XYrqbJVl/F14zOWCRptfxGiKaA=="  # 기상청 인증키 입력 필요
    base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    previous_date = datetime.now() - timedelta(days=1)
    base_date = previous_date.strftime("%Y%m%d")
    base_time = "2300"

    params = {
        "serviceKey": service_key,
        "dataType": "JSON",
        "numOfRows": 266,
        "pageNo": 1,
        "base_date": base_date,
        "base_time": base_time,
        "nx": x,
        "ny": y
    }

    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    weather_items = data['response']['body']['items']['item']
    result = ""

    tmp_value = None  # 현재기온
    tmx_value = None  # 최고기온
    tmn_value = None  # 최저기온
    pty_value = None  # 하늘상태
    reh_value = None  # 습도
    pop_value = None  # 강수확률

    for item in weather_items:
        category = item['category']
        value = item['fcstValue']
        # 현재기온
        if category == 'TMP':
            tmp_value = value
        # 최고기온
        elif category == 'TMX':
            tmx_value = value
        # 최저기온
        elif category == 'TMN':
            tmn_value = value
        # 하늘상태
        elif category == 'PTY':
            pty_value = value
        # 습도
        elif category == 'REH':
            reh_value = value
        # 강수확률
        elif category == 'POP':
            pop_value = value

    if pty_value is not None:
        if pty_value == '0':
            result += "날씨: 맑음\n"
        elif pty_value == '1':
            result += "날씨: 비\n"
        elif pty_value == '2':
            result += "날씨: 비/눈\n"
        elif pty_value == '3':
            result += "날씨: 눈\n"
        elif pty_value == '5':
            result += "날씨: 빗방울\n"
        else:
            result += "날씨: 없음\n"

    # 정보가 있는 경우 해당 정보를 결과 문자열에 추가
    if tmp_value is not None:
        result += f"현재기온: {tmp_value}도\n"
    if tmx_value is not None:
        result += f"최고기온: {tmx_value}도\n"
    if tmn_value is not None:
        result += f"최저기온: {tmn_value}도\n"
    if reh_value is not None:
        result += f"습도: {reh_value}%\n"
    if pop_value is not None:
        result += f"강수확률: {pop_value}%\n"

    # 정보가 없는 경우 메시지로 알림
    if tmp_value is None:
        result += "현재기온 정보를 가져올 수 없습니다.\n"
    if tmx_value is None:
        result += "최고기온 정보를 가져올 수 없습니다.\n"
    if tmn_value is None:
        result += "최저기온 정보를 가져올 수 없습니다.\n"
    if reh_value is None:
        result += "습도 정보를 가져올 수 없습니다.\n"
    if pop_value is None:
        result += "강수확률 정보를 가져올 수 없습니다.\n"
        
    return result

def process_weather_command(city):
    # 날씨 명령을 처리하는 함수
    # Args:
    #     city(str): 도시 이름
    # Returns:
    #     str: 날씨 정보 결과 문자열

    lat, lon = get_coordinates(city) # 주어진 도시의 위도와 경도를 가져옴

    if lat is not None and lon is not None:
        x, y = convert_to_grid(lat, lon) # 위도와 경도를 기상청 좌표 체계로 변환
        print(f"변환된 좌표 - x: {x}, y: {y}")

        result = get_forecast_temperature(x, y) # 변환된 좌표를 사용해 날씨 정보를 가져옴
        if result:
            # 날씨 정보가 존재하는 경우 해당 정보를 반환
            return result
        else:
            # 날씨 정보가 존재하지 않는 경우 메시지 반환
            return f"'{city}'의 날씨 정보를 가져올 수 없습니다."
    else:
        # 주어진 도시의 좌표를 찾을 수 없는 경우 메시지 반환
        return f"'{city}'의 좌표를 찾을 수 없습니다."
    
async def handle_weather_command(message):
    # 날씨 명령어를 처리하는 함수
    # Args:
    #    message: 디스코드에서 수신된 메시지 객체
    # Returns:
    #    None

    # 메시지가 "날씨"로 시작하는 경우에만 처리
    #if message.content.startswith("날씨"): # 명령어: 날씨 도시이름
        city = message.content[3:].strip() # 도시 이름 추출
        result = process_weather_command(city) # 날씨 정보 처리 함수 호출
        await message.channel.send(result) # 결과를 디스코드 채널로 전송
