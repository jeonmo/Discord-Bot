import requests
from bs4 import BeautifulSoup

url = "https://www.deu.ac.kr/www/board/3/1"

async def get_notice_information():
    # 공지사항 정보를 가져오는 비동기 함수
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    notice_rows = soup.find_all("tr")
    result = "```"

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

    result += "```"

    return result
