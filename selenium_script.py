from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import asyncio

async def perform_facebook_search():
    # Selenium 웹 드라이버 설정 (Chrome)
    DRIVER_PATH = 'C:/projectbot/selenium/chromedriver.exe'  # 크롬 드라이버 파일 경로를 입력

    # 페이스북 페이지 URL
    url = "https://www.deu.ac.kr/www"  # 페이스북 페이지 URL 입력

    # Selenium 웹 드라이버 생성
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")  # 알림 끄기 옵션 추가
    options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시 옵션 추가
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 로깅 기능 비활성화
    service = webdriver.chrome.service.Service(DRIVER_PATH)
    service.start()
    driver = webdriver.Chrome(service=service, options=options)  # 드라이버 경로 지정

    try:
        driver.get(url)

        # 'FaceBook' 링크 클릭
        element = driver.find_element(By.XPATH, '//*[@id="nav-ctrl01-tab"]')
        driver.execute_script("arguments[0].click();", element)

        # 페이지 로딩을 위해 약간의 대기 시간 부여
        time.sleep(5)

        # 화면 스크롤을 맨 아래로 내리기
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(2)  # 스크롤 동작을 위한 대기 시간 부여

        # 페이스북 피드 요소 선택
        feed_elements = driver.find_elements(By.XPATH, '//*[@id="nav-ctrl01"]/div/div')

        # 텍스트와 이미지를 저장할 리스트 생성
        feed_texts = []
        feed_images = []

        # 피드 텍스트와 이미지 추출
        for element in feed_elements:
            # 텍스트 추출
            text_element = element.find_element(By.XPATH, ".//p[contains(@class, 'tit')]")
            text = text_element.text
            feed_texts.append(text)

            # 이미지 추출
            image_elements = element.find_elements(By.CSS_SELECTOR, 'div.thum img')
            images = [image.get_attribute('src') for image in image_elements]
            feed_images.append(images)

        # 텍스트와 이미지를 순서대로 반환
        if feed_texts:
            results = []
            for i, text in enumerate(feed_texts):
                result = f'Text {i+1}: {text}\n'
                if feed_images[i]:
                    for image in feed_images[i]:
                        result += f'Image: {image}\n'
                results.append(result)
            return results
        else:
            return None

    finally:
        # 브라우저 종료
        driver.quit()
