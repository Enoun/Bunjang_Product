from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# ChromeDriver 경로 설정
service = Service('/Users/fastcampus/chromedriver-mac-arm64/chromedriver')

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# ChromeDriver 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# 암묵적 대기
driver.implicitly_wait(10)

# 번개장터 남성의류 카테고리 페이지 열기
driver.get("https://m.bunjang.co.kr/categories/320?order=date&page=1")

# 명시적 대기 설정 (페이지가 완전히 로드될 때까지 최대 60초 대기)
wait = WebDriverWait(driver, 5)

# 스크롤을 내려 동적 콘텐츠 로드 시도
scroll_count = 1
for i in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # 스크롤 후 페이지 로드 대기

# 상품 리스트가 로드될 때까지 대기
print("상품 리스트가 로드될 때까지 대기 중...")
products = driver.find_elements(By.XPATH, "//*[@id='root']/div/div/div[4]/div/div[4]/div/div")  # 상품 셀의 XPATH

# 셀별 데이터를 저장할 리스트
product_name = []
product_price = []
product_time = []
product_location = []
product_data_list = []

# 상품 정보 추출 및 저장
for product in products:
    try:
        # 상품명 추출
        item_name = product.find_element(By.XPATH, ".//a/div[2]/div[1]").text

        # 가격 추출
        price = product.find_element(By.XPATH, ".//a/div[2]/div[2]/div[1]").text

        # 광고인지 언제 올라온 것 인지의 정보를 추출
        time = product.find_element(By.XPATH, ".//a/div[2]/div[2]/div[2]").text

        # 지역정보 추출 (없으면 '지역 정보 없음' 처리)
        try:
            location = product.find_element(By.XPATH, ".//a/div[3]").text
        except:
            location = "지역 정보 없음"

        # 셀별로 데이터 묶기
        product_data = {
            '상품명': item_name,
            '가격': price,
            '시간': time,
            '지역 정보': location
        }

        # 리스트에 저장
        product_data_list.append(product_data)
        product_name.append(item_name)
        product_price.append(price)
        product_time.append(time)
        product_location.append(location)


    except Exception as e:
        print(f"데이터 추출 중 오류 발생: {e}")

# 리스트 출력 (저장된 데이터 확인)
# for data in product_data_list:
#     print(data)

data = {"name": product_name, "price": product_price, "time": product_time, "location": product_location}
df = pd.DataFrame(data)
print("저장되는 경로: ", os.getcwd())

df.to_csv("/Users/gimseongho/Documents/selenium_test1.csv", encoding = "utf-8-sig")


# 작업이 끝나면 브라우저 종료
driver.quit()