from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

async def send_results(results, message, mainmsg): # 2000자 제한
    for result in results:
        await message.channel.send(content = result)

async def facebook_search(message, client, mainmsg):
    DRIVER_PATH = './chromedriver.exe'  # ChromeDriver의 파일 경로로 수정해주세요
    url = "https://www.deu.ac.kr/www"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")             #알림 표시를 비활성화하는 옵션
    options.add_argument("--ignore-certificate-errors")         #인증서 오류를 무시하는 옵션을 추가합니다.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])#ChromeDriver 로그를 출력하지 않도록 설정하는 옵션
    driver = webdriver.Chrome(DRIVER_PATH, options=options)

    try:
        driver.get(url)

        element = driver.find_element(By.XPATH, '//*[@id="nav-ctrl01-tab"]')#XPath를 사용하여 요소를 찾습니다.
        driver.execute_script("arguments[0].click();", element)    # JavaScript를 실행하여 요소를 클릭

        time.sleep(5)

        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(2)

        feed_elements = driver.find_elements(By.XPATH, '//*[@id="nav-ctrl01"]/div/div') #XPath를 사용하여 피드 요소들을 탐색

        feed_texts = []
        feed_images = []

        for element in feed_elements:
            text_element = element.find_element(By.XPATH, ".//p[contains(@class, 'tit')]")#요소에서 텍스트를 포함하는 요소를 찾습니다.
            text = text_element.text
            feed_texts.append(text)

            image_elements = element.find_elements(By.CSS_SELECTOR, 'div.thum img')#요소에서 이미지를 포함하는 요소를 찾습니다.
            images = [image.get_attribute('src') for image in image_elements]
            feed_images.append(images)

        results = []
        if feed_texts:          #피드 텍스트가 있을때만 실시
            for i, text in enumerate(feed_texts):
                result = f'Text {i+1}: {text}\n'
                if feed_images[i]:  #해당 인덱스의 피드에 이미지가 있는 경우에만 실시
                    for image in feed_images[i]:
                        result += f'Image: {image}\n'
                results.append(result)
        else:
            results.append('페이스북 피드를 찾을 수 없습니다.')

        await send_results(results, message, mainmsg)

    finally:
        driver.quit()
