#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

import telegram

bot = telegram.Bot(token='')
url = 'https://goo.gl/ZYMoXm'


chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get(url)
req.encoding = 'utf-8'

html = req.text
soup = BeautifulSoup(html, 'html.parser')

cafeNames = soup.select('#elThumbnailResultArea > li > dl > dd.txt_block > span > a')
titles = soup.select('#elThumbnailResultArea > li > dl > dt > a')
postsText = soup.select('#elThumbnailResultArea > li > dl > dd.sh_cafe_passage')

if cafeNames[0] == '중고나라':
    latest_title = titles[0].text.strip() # 첫번째 글 자리
    latest_url = titles[0].get('href')
    latest_text = postsText[0].text.strip()
    second_title = titles[1].text.strip() # 두번째 글 자리
    third_title = titles[2].text.strip() # 세번째 글 자리

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        f_read.close()
        if before != latest_title:
            # 같은 경우는 에러 없이 넘기고, 다른 경우에만
            bot.sendMessage(chat_id=chat_id, text='새 글!\n\n제목 - '+ latest_title +
                            '\n내용 - ' + latest_text +
                            '\n링크 :\n' + latest_url +
                            '\n\n둘째 - ' + second_title + '\n셋째 - ' + third_title
                            +'\n\n' + '\n목록\n'+url)
            with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
                f_write.write(latest_title)
                f_write.close()


