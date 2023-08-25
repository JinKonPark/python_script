from haversine import haversine
from geopy.geocoders import Nominatim
import psycopg2

#PostgreSQL 서버 정보 
host = 'main-dev.cluster-c5we8h1iqxur.ap-northeast-2.rds.amazonaws.com'
port = 5432
database = 'main'
user = 'postgres'
password = 'kidsworld'



def get_city_info(row):
    emd_code = row[0]
    emd_korean_name = row[1]
    latitude = row[2]
    longitude = row[3]
    print(emd_code, emd_korean_name, latitude, longitude)
    #지오 코딩 객체 생성 
    geolocator = Nominatim(user_agent='South Korea')
    #위경도 정보로 주소 정보 가져오기 
    location = geolocator.reverse(f'{latitude}, {longitude}')
    address = location.raw['address']
    print(address)
    # 시 정보 혹은 군 단위의 정보를 캐낸다. 
    city = address.get('city', '') or address.get('county', '')
    return (emd_code, city)

#PostgreSQL 서버에 적솝
conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

#커서 생성
cur = conn.cursor()

try:
    #SQL 쿼리 실행 
    cur.execute('SELECT emd_code, emd_korean_name, latitude, longitude FROM korea_emd_geometry')
    #결과 가져오기 
    rows = cur.fetchall()

    for row in rows:
        (emd_code, city) = get_city_info(row)
        print(emd_code, city)
        # update 쿼리 수행 
        cur.execute("update korea_emd_geometry set city=%s where emd_code=%s", (city, emd_code))
        conn.commit()
        
finally:
    cur.close()
    conn.close()






