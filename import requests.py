import xml.etree.ElementTree as ET
from attr import dataclass
import requests
import xmltodict
import json



test_str = "{'seq': '245673', 'title': '무릉도원보다 지금 삶이 더 다정하도다', 'startDate': '20230505', 'endDate': '20230827', 'place': '제주도립미술관', 'realmName': '미술', 'area': '제주', 'subTitle': None, 'price': '어른 2,000원 / 청소년 및 군인 1,000원 / 어린이 500원 / 노인 및 유아 무료', 'contents1': None, 'contents2': None, 'url': None, 'phone': '제주도립미술관 064-710-4300', 'imgUrl': 'http://www.culture.go.kr/upload/rdf/23/05/show_2023051716514355876.jpg', 'gpsX': '126.48963496144127', 'gpsY': '33.45259362658467', 'placeUrl': 'http://jmoa.jeju.go.kr/?sso=ok', 'placeAddr': '제주특별자치도 제주시 1100로 2894-78 제주도립미술관', 'placeSeq': '2645'}"
print(test_str.replace("'", '"').replace('None', '""'))