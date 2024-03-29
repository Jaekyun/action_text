import requests
from bs4 import BeautifulSoup as bs
import telegram
import asyncio

async def get_new_links(old_links=[]):
    url = f'https://search.naver.com/search.naver?where=news&query=%ED%95%9C%EB%8F%99%ED%9B%88&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0'

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
        await asyncio.sleep(5)  # Execute every 10 seconds

async def main():
    bot_token = '5139194628:AAHB_PXqv0y_xfn57Z5IAAYL98QtxPLn7-o'
    bot = telegram.Bot(token=bot_token)

    chat_id = '@pgecho'

    await bot.send_message(chat_id='@pgecho', text="한동훈 키워드 기사 검색 시작")

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
