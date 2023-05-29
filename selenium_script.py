from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

async def send_results(results, message):
    for result in results:
        await message.channel.send(result)

async def facebook_search(message, client):
    DRIVER_PATH = 'C:/projectbot/selenium/chromedriver.exe'  # ChromeDriver의 파일 경로로 수정해주세요
    url = "https://www.deu.ac.kr/www"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = webdriver.chrome.service.Service(DRIVER_PATH)
    service.start()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        element = driver.find_element(By.XPATH, '//*[@id="nav-ctrl01-tab"]')
        driver.execute_script("arguments[0].click();", element)

        time.sleep(5)

        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(2)

        feed_elements = driver.find_elements(By.XPATH, '//*[@id="nav-ctrl01"]/div/div')

        feed_texts = []
        feed_images = []

        for element in feed_elements:
            text_element = element.find_element(By.XPATH, ".//p[contains(@class, 'tit')]")
            text = text_element.text
            feed_texts.append(text)

            image_elements = element.find_elements(By.CSS_SELECTOR, 'div.thum img')
            images = [image.get_attribute('src') for image in image_elements]
            feed_images.append(images)

        results = []
        if feed_texts:
            for i, text in enumerate(feed_texts):
                result = f'Text {i+1}: {text}\n'
                if feed_images[i]:
                    for image in feed_images[i]:
                        result += f'Image: {image}\n'
                results.append(result)
        else:
            results.append('페이스북 피드를 찾을 수 없습니다.')

        await send_results(results, message)

    finally:
        driver.quit()
