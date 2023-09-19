import requests
import psycopg2
from bs4 import BeautifulSoup

## Prod 환경의 DB 접속 정보 
conn = psycopg2.connect(
    host="main.cluster-c4npmqkr9mr7.ap-northeast-2.rds.amazonaws.com",
    database="main",
    user="postgres",
    password="YnkR?pY1oNH}HY*t",
)

cur = conn.cursor()
cur.execute("SELECT id, summary FROM play_finder_site")
rows = cur.fetchall()


def removeHtml(html):
    if html is None:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text
    

## 위경도 정보가 존재하지 않는 데이터에 대한 update 수행
for row in rows:
    id = row[0]
    summay = row[1]
    removed_html_summay = removeHtml(summay)
    print(id, removed_html_summay)
    if removed_html_summay is not None:
        cur.execute("update play_finder_site set summary = %s where id = %s", (removed_html_summay, id))
        conn.commit()
    

## 종료
cur.close()
conn.close()
