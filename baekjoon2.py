
import requests  # http 요청
import os.path  # .isfile() 파일 존재 유무 확인
from bs4 import BeautifulSoup  # 웹 크롤링
import pandas as pd
import matplotlib.pyplot as plt

#https://solvedac.github.io/unofficial-documentation/#/schemas/Problem
#https://github.com/DipokalLab/solvedac-info/blob/main/get_info.js

# User-Agent 설정, 일부 웹사이트는 User-Agent 헤더를 검사하여 브라우저에서의 요청인지 확인한다.
# 일반적인 브라우저인척 속이기 위해 헤더를 작성하였다.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_problem_info(problem_id: str):  # 문제 번호로 해당 문제에 대한 정보를 확인, 문자열 반환
    url = f"https://www.acmicpc.net/problem/{problem_id}"

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    problem_title = soup.find('span', id='problem_title').text.strip()
    problem_description = soup.find('div', id='problem_description').text.strip()

    # 입력 조건 가져오기
    input_section = soup.select_one('#problem_input > p')
    input_description = input_section.text.strip() if input_section else None

    # 출력 조건 가져오기
    output_section = soup.select_one('#problem_output > p')
    output_description = output_section.text.strip() if output_section else None

    # 예제 가져오기
    sample_data = []
    sample_section = soup.find_all('pre', class_='sampledata')
    for sample in sample_section:
        sample_data.append(sample.text.strip())


    problem_info = {
        'title': problem_title,
        'description': problem_description,
        'input_description': input_description,
        'output_description': output_description,
        'sample_data': sample_data,
    }

    returningStr = ""
    if problem_info:
        returningStr += f"문제 제목: {problem_info['title']}\n"
        returningStr += f"문제 설명: {problem_info['description']}\n"
        if problem_info['input_description'] is not None:
            returningStr += f"\n입력 조건:"
            returningStr += f"{problem_info['input_description']}"
        if problem_info['output_description'] is not None:
            returningStr += f"\n출력 조건:"
            returningStr += f"{problem_info['output_description']}"

        sample_data = problem_info['sample_data']
        num_samples = len(sample_data)

        
        if num_samples > 0:
            returningStr += f"\n예제 입출력\n"
            for i in range(0,num_samples,2):
                sample_input = sample_data[i]
                returningStr += f"예제 {i+1} 입력 : \n{sample_input}\n"
                sample_output = sample_data[i+1]
                returningStr += f"예제 {i+1} 출력 : \n{sample_output}\n"
    else:
        returningStr += "문제 정보를 가져올 수 없습니다."
    print(returningStr)
    return returningStr
    

def counterExample(id: str, content: str):
    f = open(f'./problemData/{id}.txt', 'a', encoding='utf-8')

