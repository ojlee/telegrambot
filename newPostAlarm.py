
import requests
from bs4 import BeautifulSoup
import os

import telegram

bot = telegram.Bot(token='540032183:AAEHc2AJ3oXfKY8Hi8a56XSRQJIYfvPotmI')
chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('https://www.clien.net/service/board/news')
req.encoding = 'utf-8' # Clien에서 encoding 정보를 보내주지 않아 encoding옵션을 추가해줘야합니다.

html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.select('a.list_subject')
latest_title = posts[2].text # 첫번째 글 자리
latest_url = posts[2].get('href')
second_title = posts[3].text # 두번째 글 자리
third_title = posts[4].text # 세번째 글 자리


with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
    before = f_read.readline()
    f_read.close()
    if before != latest_title:
        # 같은 경우는 에러 없이 넘기고, 다른 경우에만
        bot.sendMessage(chat_id=chat_id, text='새 글!\n'+ latest_title + '\n링크 :\n ' + latest_url + '\n\n' + second_title + '\n' + third_title
                        +'\n목록\nhttps://www.clien.net/service/board/news')
        with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
            f_write.write(latest_title)
            f_write.close()


