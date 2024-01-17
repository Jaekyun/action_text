import requests
from bs4 import BeautifulSoup as bs
import telegram
import asyncio

async def get_new_links(old_links=[]):
    url = f'https://url.kr/16yqpw'

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
        for link in new_links:
            await bot.send_message(chat_id=chat_id, text=link)
    else:
        pass

    old_links += new_links.copy()

async def periodic_task(bot, chat_id):
    while True:
        await send_links(bot, chat_id)
        await asyncio.sleep(10)  # 10초마다 실행

async def main():
    bot_token = '5139194628:AAHB_PXqv0y_xfn57Z5IAAYL98QtxPLn7-o'
    bot = telegram.Bot(token=bot_token)

    chat_id = '@eyes1000'

    await bot.send_message(chat_id='@eyes1000', text="뉴스 기사 크롤링이 시작 되었습니다")

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
