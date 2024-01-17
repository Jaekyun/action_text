# step1.라이브러리 불러오기
import requests
from bs4 import BeautifulSoup as bs
import telegram
import schedule
import time


# step2.새로운 네이버 뉴스 기사 링크를 받아오는 함수
def get_new_links(old_links=[]):
    # (주의) 네이버에서 키워드 검색 - 뉴스 탭 클릭 - 최신순 클릭 상태의 url
    url = f'https://url.kr/jbq5uz'

    # html 문서 받아서 파싱(parsing)
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # 해당 페이지의 뉴스기사 링크가 포함된 html 요소 추출
    news_titles = soup.select('a.news_tit')

    # 요소에서 링크만 추출해서 리스트로 저장
    list_links = [i.attrs['href'] for i in news_titles]

    # 기존의 링크와 신규 링크를 비교해서 새로운 링크만 저장
    new_links = [link for link in list_links if link not in old_links]

    return new_links


# step3.새로운 네이버 뉴스 기사가 있을 때 텔레그램으로 전송하는 함수
def send_links():
    # 함수 내에서 처리된 리스트를 함수 외부에서 참조하기 위함
    global old_links

    # 위에서 정의했던 함수 실행
    new_links = get_new_links(old_links)

    # 새로운 메시지가 있으면 링크 전송
    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id=chat_id, text=link)
    # 없으면 패스
    else:
        pass

    # 기존 링크를 계속 축적하기 위함
    old_links += new_links.copy()


# 실제 프로그램 구동
if __name__ == '__main__':

    # 토큰을 변수에 저장
    bot_token = '5139194628:AAHB_PXqv0y_xfn57Z5IAAYL98QtxPLn7-o'

    bot = telegram.Bot(token=bot_token)

    # 가장 최근에 온 메세지의 정보 중, chat id만 가져옴 (이 chat id는 사용자(나)의 계정 id임)
    chat_id = '@eyes1000'

    # step4.검색할 키워드 설정
    # query = input('크롤링 할 뉴스기사 키워드를 입력하세요:  ')

    # 위에서 얻은 chat id로 bot이 메세지를 보냄.
    bot.sendMessage(chat_id='@eyes1000', text=f"'한동훈'을 주제로 뉴스 기사 수집이 시작되었습니다")

    # step5.기존에 보냈던 링크를 담아둘 리스트 만들기
    old_links = []

    # 주기적 실행과 관련된 코드 (hours는 시, minutes는 분, seconds는 초)
    job = schedule.every(10).seconds.do(send_links)

    while True:
        schedule.run_pending()
        time.sleep(1)
