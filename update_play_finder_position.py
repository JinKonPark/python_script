import requests
import psycopg2

service_key = "66ff875292132b326b974f47419cd0c3"
url = "https://dapi.kakao.com/v2/local/search/address"


dev_host = "main-dev.cluster-c5we8h1iqxur.ap-northeast-2.rds.amazonaws.com"
beta_host = "main-beta.cluster-c5we8h1iqxur.ap-northeast-2.rds.amazonaws.com"
prod_host = "main.cluster-c4npmqkr9mr7.ap-northeast-2.rds.amazonaws.com"
user = "postgres"
password = "kidsworld"

host = dev_host

## Prod 환경의 DB 접속 정보 
conn = psycopg2.connect(
    host=host,
    database="main",
    user=user,
    password=password,
)

# Kakao API를 이용하여 주소로부터 위경도 정보를 가져오는 함수
def getPosition(address):
    headers = {"Authorization": "KakaoAK 66ff875292132b326b974f47419cd0c3"}
    response = requests.get(url, params={"query": address}, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if len(result['documents']) > 0:
            return result['documents'][0]['y'], result['documents'][0]['x']
        else:
            return None, None
    else:
        print("Error:", response.status_code)
        return None, None

cur = conn.cursor()
cur.execute("SELECT id, address FROM play_finder_site where address is not null and longitude is null and latitude is null")
rows = cur.fetchall()

## 위경도 정보가 존재하지 않는 데이터에 대한 update 수행
for row in rows:
    id = row[0]
    address = row[1]
    (y, x) = getPosition(address)
    print(address, x, y)
    if x is not None and y is not None:
        cur.execute("update play_finder_site set longitude = %s, latitude = %s where id = %s", (x, y, id))
        conn.commit()

## 종료
cur.close()
conn.close()
