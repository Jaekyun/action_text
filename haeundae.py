import requests
from bs4 import BeautifulSoup as bs
import telegram
import asyncio

async def get_new_links(old_links=[]):
    url = f'https://search.naver.com/search.naver?where=news&query=%EC%A3%BC%EC%A7%84%EC%9A%B0%20%7C%20%ED%95%B4%EC%9A%B4%EB%8C%80%EA%B5%AC%EA%B0%91%20%7C%20%ED%95%B4%EC%9A%B4%EB%8C%80%EA%B0%91&sort=1&sm=tab_smr&nso=so:dd,p:all,a:all'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_titles = soup.select('a.news_tit')
    list_links = [i.attrs['href'] for i in news_titles]

    new_links = [link for link in list_links if link not in old_links]

    return new_links

async def send_links(bot, chat_id):
    global old_links

    new_links = await get_new_links(old_links)

    if new_links:
        # Reverse the order of new links to send the most recent news first
        new_links.reverse()

        for link in new_links:
            await bot.send_message(chat_id=chat_id, text=link)
    else:
        pass

    old_links += new_links.copy()

async def periodic_task(bot, chat_id):
    while True:
        await send_links(bot, chat_id)
        await asyncio.sleep(60)  # Execute every 5 seconds

async def main():
    bot_token = '6784271517:AAGXzwpDyeS11r3Txf7KyYn8LHtj8lHvKJQ'
    bot = telegram.Bot(token=bot_token)

    chat_id = '@nice110argos'

    await bot.send_message(chat_id=chat_id, text="주진우 | 해운대구갑 | 해운대갑으로 뉴스 기사 검색 시작")

    global old_links
    old_links = []

    task = asyncio.ensure_future(periodic_task(bot, chat_id))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        task.cancel()

if __name__ == '__main__':
    asyncio.run(main())
