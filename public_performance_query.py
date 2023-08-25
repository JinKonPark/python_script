from math import ceil
import requests
import xml.etree.ElementTree as ET
from dataclasses import dataclass
import xmltodict
import json
import pandas as pd


class PlayFinderFestivalSite:
    title: str
    start_date: str
    end_date: str
    place: str
    thumbnail: str
    gps_x: str
    gps_y: str
    place_url: str
    sub_title: str
    price: str
    url: str
    phone: str
    imgUrl: str
    place_url: str
    place_addr: str
    


c_page = 1
rows = 30

# API 서비스 인증키
service_key = 'bAaSZzazZKIurExM+XmxLd5S//OotobzAYzSgs7kHWeXIT9YZyvYS5UXa+2uTp19MjHuGFACl5kjUHNPlbYKUA=='
# API 호출 URL
performance_list_url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/period'

def get_performance_list(start_date, end_date, c_page, rows):
    
    # API 호출 파라미터
    params = {
        'from': start_date, #'20230801',
        'to': end_date, #'20230830',
        'cPage': c_page,
        'rows': rows,
        'place': '',
        'gpsxfrom': '',
        'gpsyfrom': '',
        'gpsxto': '',
        'gpsyto': '',
        'keyword': '',
        'sortStdr': '1',
        'serviceKey': service_key
    }
    # API 호출
    performance_list_res = requests.get(performance_list_url, params=params)
    performance_list_res_json_dict = json.loads(json.dumps(xmltodict.parse(performance_list_res.text), ensure_ascii=False))
    return performance_list_res_json_dict

def get_performance_detail(performance_list_res_json_dict):
    performance_list = []
    for performance in performance_list_res_json_dict['response']['msgBody']['perforList']:
        """
        performance의 형태 
            {
                "seq": "249941",
                "title": "변신",
                "startDate": "20230727",
                "endDate": "20230806",
                "place": "대학로 공간아울",
                "realmName": "연극",
                "area": "서울",
                "thumbnail": "http://www.culture.go.kr/upload/rdf/23/07/rdf_2023070621171411718.gif",
                "gpsX": "127.00228690963143",
                "gpsY": "37.58187272296083"
            }
        """
        performanceseq = performance['seq']
        performance_detail_url = f'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/d/?serviceKey=bAaSZzazZKIurExM%2BXmxLd5S%2F%2FOotobzAYzSgs7kHWeXIT9YZyvYS5UXa%2B2uTp19MjHuGFACl5kjUHNPlbYKUA%3D%3D&seq={performance_seq}'
        performance_detail_res = requests.get(performance_detail_url)    
        response_json_dict = json.loads(json.dumps(xmltodict.parse(performance_detail_res.text), ensure_ascii=False))
        
        """response_json_dict은 다음과 같은 형태의 JSON임. 
                {
                "response": {
                    "comMsgHeader": {
                        "RequestMsgID": "",
                        "ResponseTime": "2023-08-25 14:22:26.2226",
                        "ResponseMsgID": "",
                        "SuccessYN": "Y",
                        "ReturnCode": "00",
                        "ErrMsg": "NORMAL SERVICE."
                    },
                    "msgBody": {
                        "seq": "250635",
                        "perforInfo": {
                            "seq": "250635",
                            "title": "우리 모두는 서로의 운명이다 - 멸종위기동물 예술로 HUG",
                            "startDate": "20230630",
                            "endDate": "20230801",
                            "place": "포항시립중앙아트홀 전시실",
                            "realmName": "미술",
                            "area": "경북",
                            "subTitle": "",
                            "price": "무료",
                            "contents1": "",
                            "contents2": "",
                            "url": "",
                            "phone": "포항문화재단 054-289-7823",
                            "imgUrl": "http://www.culture.go.kr/upload/rdf/23/07/show_2023071715344895948.png",
                            "gpsX": "129.36735763201557",
                            "gpsY": "36.04099796619284",
                            "placeUrl": "http://phtour.pohang.go.kr/phtour/concert/space/art_hall/",
                            "placeAddr": "경상북도 포항시 북구 서동로 83 포항시립중앙아트홀 전시실",
                            "placeSeq": "4026"
                        }
                    }
                }
            }
        """
        #만약 response 하위의 comMsgHeader 하위의 returnCode가 00이 아니면
        #ErrMsg 필드를 출력한다. 
        if response_json_dict['response']['comMsgHeader']['ReturnCode'] != '00':
            print(response_json_dict['response']['comMsgHeader']['ErrMsg'])
            return None
        else:
            json_str = json.dumps(response_json_dict['response']['msgBody']['perforInfo']).replace("'", '"').replace('None', '""')
            # df = pd.DataFrame([json.loads(json_str)], index=[0])
            # if len(performance_list) == 0:
            #     df.to_csv('performance.csv', header=True, index=False, mode='a')
            # else:
            #     df.to_csv('performance.csv', header=False, index=False, mode='a')
            # performance_list.append(json_str)
            performance_list.append(json.loads(json_str))
    return performance_list
                
# API 응답 결과 출력
performance_list_result = get_performance_list('20230801', '20230830', 1, 1)
total_count = performance_list_result['response']['msgBody']['totalCount']
print(f"total_count = {total_count}")

#마지막 페이지 정보 획득
last_page = ceil(int(total_count)/30.0)
print(last_page)

#마지막 페이지까지 반복하면서 공연 정보 획득
for page in range(1, last_page+1):
    print(f'page = {page}')
    performance_list_result = get_performance_list('20230801', '20230830', page, 30)
    performance_detail_result = get_performance_detail(performance_list_result)
    #ççprint(performance_detail_result)
    
    





