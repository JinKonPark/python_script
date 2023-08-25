import http
import json
import time
import urllib.request
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import urlencode, urlparse
from enum import Enum

class SearchSortType(Enum):
    SIM="sim"
    DATE="date"

def get_search_result(client_id, client_secret, url):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
    else:
        print("Error Code:" + rescode)

    return response_body.decode('utf-8')

# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_contents_from_url(url):
    #크롬 드라이버 초기화
    driver = set_chrome_driver()
    driver.get(url) # 웹사이트 접속
    time.sleep(2)
    driver.switch_to.frame('mainFrame')

    contents = ''
    try:
        a = driver.find_element(By.CSS_SELECTOR,'div.se-main-container').text
        contents = a.replace('\n', " ")
    except NoSuchElementException:
        print("요소를 찾을 수 없습니다. urls: ", url)
    finally:
        driver.quit()

    return contents
 
 
 # Naver Open API application ID, Secret
client_id = "D7LmDEYrMic2YRpskwt1" # 발급받은 id 입력
client_secret = "th6PYwzWnU" # 발급받은 secret 입력 

# 정보입력
quote = input("검색어 입력: ") #검색어 입력받기
display_num = input("검색 출력결과 갯수를 적어주세요.(최대100, 숫자만 입력): ") #출력할 갯수 입력받기
sort_type = SearchSortType.SIM if input("검색 정렬방법을 선택해 주세요.(1. 정확도순, 2. 최신순): ") == "1" else SearchSortType.DATE
temp = input("다양성 성향(tempertature)(0.0~2.0사이 defeault 1.0): ") or "1.0" 
top_p = input("핵 샘플링 값(top_p)(0.0~1.0사이 defeault 1.0): ") or "1.0" 
max_token = input("응답 토큰 수(default 1024): ") or "1024" 

query_string = urlencode({"query": quote, 
                          "display": display_num,
                          "sort": sort_type.value})
url = "https://openapi.naver.com/v1/search/blog?" + query_string

# 검색결과 받아오기
"""
다음과 같은 형식의 결과를 가져옴 
{
    "lastBuildDate": "Wed, 02 Aug 2023 17:24:02 +0900",
    "total": 28221,
    "start": 1,
    "display": 10,
    "items": [
        {
            "title": "ChatGPT (인공지능 챗봇)와 <b>OpenAI</b>에 대해...",
            "link": "https://ystazo.tistory.com/1964",
            "description": "org ChatGPT - Wikipedia From Wikipedia, the free encyclopedia Artificial intelligence chatbot developed by <b>OpenAI</b> ChatGPT (Chat Generative Pre-trained Transformer[2]) is a chatbot developed by <b>OpenAI</b> and launched in November 2022. It is built on... ",
            "bloggername": "TASTORY : 타스토리!",
            "bloggerlink": "https://ystazo.tistory.com/",
            "postdate": "20230220"
        },
        ...
"""
search_result = json.loads(get_search_result(client_id, client_secret, url))


#OpenAI의 system role의 persona 설정
system = """
    무언가를 요약해달라는 요청이 올때 다음과 같은 내용을 아래의 형식에 맞게 요약해서 전달한다. 
    형식정보는 다음과 같다. 
     - 장소의 이름 
     - 장소의 컨셉
     - 장소의 주소
     - 장소의 실내외 여부
     - 운영시간
     - 장소의 공연정보
     - 휴무일 정보
     - 연락처
     - 간략한 장소 설명
     - 장소 이미지 링크
     - 가격정보
     - 이용시간
     - 이용 대상 연령
     - 주차장 유무
     - 주차 난이도
     - 주변 주차장 정보
     - 장소 예약 난이도
     - 유아 편의 시절
     - 할인정보
     - 해시태그
    형식에 맞는 정보를 블로그에서 찾을 수 없는 경우 인터넷에서 확인후 직접 입력한다.
    """  

conn  = http.client.HTTPConnection("localhost:8080")

# data의 items를 순환하며 출력하기
for item in search_result['items']:
    print('------------------------------ 블로그 스크래핑 정보 ------------------------------')
    print("블로그 링크주소 -> {}".format(item['link']))
    blog_contents = get_contents_from_url(item['link'])
    user_message='아래 큰 따옴표 3개로 구분된 블로그 기사의 내용을 요약해줘 """{}"""'.format(blog_contents)
    print(blog_contents)
    print('------------------------------ OPEN AI RESPONSE ------------------------------')

    query_param = {"temp": temp, "top-p": top_p, "max-tokens": max_token, "n": 1}
    query_string = urlencode(query_param)
    url = "/open-ai/question?" + query_string
    request_body = json.dumps({"system": system, "user": user_message})
    conn.request("POST", url, request_body, {"Content-Type": "application/json"})
    response = json.loads(conn.getresponse().read().decode("utf-8"))
    print(response["data"]["answerList"][0])
    print('------------------------------------------------------------')

