import json
from math import ceil
import time
import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

reg_exp = '<.*?>|&lt;|&gt;|lt;|&nbsp;'


#행사 정보 클래스
class FestivalBase:
    def __init__(self, data):
        self.addr1 = re.sub(reg_exp, '', data['addr1'])
        self.addr2 = re.sub(reg_exp, '', data['addr2'])
        self.booktour = re.sub(reg_exp, '', data['booktour'])
        self.cat1 = re.sub(reg_exp, '', data['cat1'])
        self.cat2 = re.sub(reg_exp, '', data['cat2'])
        self.cat3 = re.sub(reg_exp, '', data['cat3'])
        self.contentid = re.sub(reg_exp, '', data['contentid'])
        self.contenttypeid = re.sub(reg_exp, '', data['contenttypeid'])
        self.createdtime = re.sub(reg_exp, '', data['createdtime'])
        self.eventstartdate = re.sub(reg_exp, '', data['eventstartdate'])
        self.eventenddate = re.sub(reg_exp, '', data['eventenddate'])
        self.firstimage = re.sub(reg_exp, '', data['firstimage'])
        self.firstimage2 = re.sub(reg_exp, '', data['firstimage2'])
        self.cpyrhtDivCd = re.sub(reg_exp, '', data['cpyrhtDivCd'])
        self.mapx = re.sub(reg_exp, '', data['mapx'])
        self.mapy = re.sub(reg_exp, '', data['mapy'])
        self.mlevel = re.sub(reg_exp, '', data['mlevel'])
        self.modifiedtime = re.sub(reg_exp, '', data['modifiedtime'])
        self.areacode = re.sub(reg_exp, '', data['areacode'])
        self.sigungucode = re.sub(reg_exp, '', data['sigungucode'])
        self.tel = re.sub(reg_exp, '', data['tel'])
        self.title = re.sub(reg_exp, '', data['title'])
        
#행사 디테일정보 클래스
class FestivalDetail:
    def __init__(self, data):
        self.contentid = re.sub(reg_exp, '', data['contentid'])
        self.contenttypeid = re.sub(reg_exp, '', data['contenttypeid'])
        self.sponsor1 = re.sub(reg_exp, '', data['sponsor1'])
        self.sponsor1tel = re.sub(reg_exp, '', data['sponsor1tel'])
        self.sponsor2 = re.sub(reg_exp, '', data['sponsor2'])
        self.sponsor2tel = re.sub(reg_exp, '', data['sponsor2tel'])
        self.eventenddate = re.sub(reg_exp, '', data['eventenddate'])
        self.playtime = re.sub(reg_exp, '', data['playtime'])
        self.eventplace = re.sub(reg_exp, '', data['eventplace'])
        self.eventhomepage = re.sub(reg_exp, '', data['eventhomepage'])
        self.agelimit = re.sub(reg_exp, '', data['agelimit'])
        self.bookingplace = re.sub(reg_exp, '', data['bookingplace'])
        self.placeinfo = re.sub(reg_exp, '', data['placeinfo'])
        self.subevent = re.sub(reg_exp, '', data['subevent'])
        self.program = re.sub(reg_exp, '', data['program'])
        self.eventstartdate = re.sub(reg_exp, '', data['eventstartdate'])
        self.usetimefestival = re.sub(reg_exp, '', data['usetimefestival'])
        self.discountinfofestival = re.sub(reg_exp, '', data['discountinfofestival'])
        self.spendtimefestival = re.sub(reg_exp, '', data['spendtimefestival'])
        self.festivalgrade = re.sub(reg_exp, '', data['festivalgrade'])

class EventDetail:
    def __init__(self, data):
        self.infotext = re.sub(reg_exp, '', data['infotext'])
        self.serialnum = re.sub(reg_exp, '', data['serialnum'])
        self.infoname = re.sub(reg_exp, '', data['infoname'])

class AddtionalImage:
    def __init__(self, data):
        self.originimgurl = re.sub(reg_exp, '', data['originimgurl'])

class FestivalCommon:
    def __init__(self, data):
        self.contentid = data['contentid']
        self.contenttypeid = data['contenttypeid']
        self.title = data['title']
        self.createdtime = data['createdtime']
        self.modifiedtime = data['modifiedtime']
        self.tel = data['tel']
        self.telname = data['telname']
        self.homepage = data['homepage']
        self.booktour = data['booktour']
        
columns = ['이름', 
            '주소', 
            '전화번호', 
            '위도', 
            '경도', 
            '가격정보',
            '장소정보', 
            '주차난이도', 
            '주차장 정보', 
            '편의시설 정보', 
            '홈페이지URL', 
            '장소이름', 
            '이미지 경로', 
            '썸네일이미지 경로', 
            '행사 시작일', 
            '행사 종료일',
            '운영시간',
            '이용시간',
            '연령제한',
            '예약URL',
            '요약정보',
            '행사 설명',
            '할인정보',
            '서브 행사 정보',
            '프로그램 내용',
            '실내외 여부',
            '추가 이미지 정보'
            ]


public_api_service_key = 'bAaSZzazZKIurExM+XmxLd5S//OotobzAYzSgs7kHWeXIT9YZyvYS5UXa+2uTp19MjHuGFACl5kjUHNPlbYKUA=='


def get_performance_list(start_date, c_page, rows, to_get_total_page=False):
    # API 호출 URL
    url = 'http://apis.data.go.kr/B551011/KorService1/searchFestival1'
    
    # API 호출 파라미터
    params = {
        'serviceKey': f'{public_api_service_key}',
        'numOfRows': f'{rows}',
        'pageNo': f'{c_page}',
        'MobileOS': 'ETC',
        'MobileApp': 'AppTest',
        'arrange': 'A',
        'listYN': 'Y',
        'eventStartDate': f'{start_date}',
        '_type': 'json'
    }
    
    # API 호출
    response = requests.get(url, params=params)
    json_dict = json.loads(response.text)
    
    if to_get_total_page:
        return json_dict['response']['body']['totalCount']
    
    ## 행사 리스트를 반복하면서 행사의 상세정보를 조회해서 dataframe에 추가 
    for item in json_dict['response']['body']['items']['item']:
        #행사 기본 정보
        festival = FestivalBase(item)
        
        #행사 상세 정보
        festival_detail = get_festival_detail(festival.contentid)  
        
        #공통정보 가져오기
        common = get_common_detail(festival.contentid) 
        homepage_url = ''
        
        if common:
            soup = BeautifulSoup(common.homepage, 'html.parser')
            if soup :
                try:
                    # 링크 추출
                    homepage_url = soup.a.get('href')
                except:
                    pass
        
        # 반복정보 가져오기 
        (summary, description) = get_festival_event_info(festival.contentid) 
        
        # 추가이미지 가져오기 
        image_list = get_festival_additional_image(festival.contentid)
        
        df = pd.DataFrame(columns=columns)
        df.loc[len(df)] = [festival.title,  # 이름
                        festival.addr1 + festival.addr2, # 주소
                        festival.tel, # 전화번호
                        festival.mapy, # 위도
                        festival.mapx, # 경도
                        festival_detail.usetimefestival, # 가격정보
                        festival_detail.placeinfo, # 장소정보(행사장 위치안내)
                        np.nan, # 주차난이도
                        np.nan, # 주차장 정보
                        np.nan, # 편의시설정보
                        homepage_url, #홈페이지 URL 
                        festival_detail.eventplace, # 장소이름
                        festival.firstimage, # 이미지 경로
                        festival.firstimage2, # 썸네일이미지 경로
                        festival.eventstartdate, # 행사 시작일
                        festival.eventenddate, # 행사 종료일
                        festival_detail.playtime,
                        festival_detail.spendtimefestival, # 이용시간
                        festival_detail.agelimit, # 연령제한
                        festival_detail.bookingplace, # 예약URL
                        summary, 
                        description,
                        festival_detail.discountinfofestival,
                        festival_detail.subevent,
                        festival_detail.program, 
                        False,
                        image_list]
        
        df.to_csv('festival.csv', header=False, index=False, mode='a')


def get_festival_detail(content_id):
    #행사정보 상세조회 URL
    detail_url = 'http://apis.data.go.kr/B551011/KorService1/detailIntro1'

    # API 호출 파라미터
    params = {
        'serviceKey': f'{public_api_service_key}',
        'MobileOS': 'ETC',
        'MobileApp': 'AppTest',
        '_type': 'json',
        'contentId': f'{content_id}',
        'contentTypeId': '15',
        'numOfRows': '10',
        'pageNo': '1'
    }
       
    res = requests.get(detail_url, params=params)
    detail_json_dict = json.loads(res.text)
    print(detail_json_dict)
    festival_detail = FestivalDetail(detail_json_dict['response']['body']['items']['item'][0])
    return festival_detail
    

def get_festival_event_info(content_id):
    url = 'http://apis.data.go.kr/B551011/KorService1/detailInfo1'
    
    params = {
        'serviceKey': f'{public_api_service_key}',
        'MobileOS': 'ETC',
        'MobileApp': 'AppTest',
        '_type': 'json',
        'contentId': f'{content_id}',
        'contentTypeId': '15',
    }
    contens_json_dict = json.loads(requests.get(url, params=params).text)
    
    event_sumamry = '' 
    event_contents = '' 
    
    if contens_json_dict['response']['body']['items']:
        item_list = contens_json_dict['response']['body']['items']['item']
        for item in item_list:
            event_detail = EventDetail(item)
            
            if event_detail.infoname == '행사소개':
                event_sumamry = event_detail.infotext
            elif event_detail.infoname == '행사내용':
                event_contents = event_detail.infotext
            
    return (event_sumamry, event_contents)        

def get_festival_additional_image(content_id):
    url = 'http://apis.data.go.kr/B551011/KorService1/detailImage1'
    
    params = {
        'serviceKey': f'{public_api_service_key}',
        'MobileOS': 'ETC',
        'MobileApp': 'AppTest',
        '_type': 'json',
        'contentId': f'{content_id}',
        'numOfRows': '10',
        'imageYN' : 'Y',
        'subImageYN': 'Y'
    }
    
    contens_json_dict = json.loads(requests.get(url, params=params).text)
    add_image_list = []
    if contens_json_dict['response']['body']['items']:
        item_list = contens_json_dict['response']['body']['items']['item']
        for item in item_list:
            add_image = AddtionalImage(item)
            add_image_list.append(add_image)
        return list(map(lambda x: x.originimgurl, add_image_list))
    else:
        return add_image_list
    

def get_common_detail(content_id):
    url = 'http://apis.data.go.kr/B551011/KorService1/detailCommon1'
    
    params = {
        'serviceKey': f'{public_api_service_key}',
        'MobileOS': 'ETC',
        'MobileApp': 'AppTest',
        '_type': 'json',
        'contentId': f'{content_id}',
        'contentTypeId': '15',
        'defaultYN' : 'Y',
    }
    
    contens_json_dict = json.loads(requests.get(url, params=params).text)
    if contens_json_dict['response']['body']['items']:
        return FestivalCommon(contens_json_dict['response']['body']['items']['item'][0])
    else:
        return None
    
         
def main():    
    df = pd.DataFrame(columns=columns)
    df.to_csv('festival.csv', header=True, index=False, mode='w')

    start_date = '20230926'
    # API 응답 결과 출력
    total_count = get_performance_list(start_date, 1, 1, True)
    print(f"total_count = {total_count}")
    
    rows = 30
    #마지막 페이지 정보 획득
    last_page = ceil(int(total_count)/ float(rows))
    print(last_page)
    
    #마지막 페이지까지 반복하면서 공연 정보 획득
    for page in range(1, last_page+1):
        get_performance_list(start_date, page, rows)

main()





    

    
    




    
