from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import random
import time
import get_pictures

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.138 YaBrowser/20.4.2.201 Yowser/2.5 Yptp/1.23 Safari/537.36',
           'accept': '*/*'}

login, password = 'login', 'password'
vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
try:
    vk_session.auth(token_only=True)
    print('Succesfully authorised')
except vk_api.AuthError as error_msg:
    print(error_msg)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_user_name(user_id):
    request = requests.get('http://vk.com/id' + str(user_id), headers=HEADERS)
    soup = BeautifulSoup(request.text, 'html.parser')
    items = soup.find_all('div', class_='page_top')
    name = ''
    while name == '':
        for item in items:
            name = item.find('h1', class_='page_name')

    return name.get_text(strip=True)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Сообщение пришло в: ', str(datetime.strftime(datetime.now(), '%H:%M:%S')))
        print('Текст сообщения: ' + str(event.text))
        print('В диалоге с ' + get_user_name(event.user_id) + f', id пользователя = {event.user_id}')
        print('=' * 100)
        response = event.text.lower()
        if event.from_user and not event.from_me:
            if response == "12!":
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'И тебе привет от бота!', 'random_id': 0})
            elif response == 'котейки':
                attachment = get_pictures.get(vk_session, -175086907, session_api)
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'Лови котиков!', 'random_id': 0,
                                                    'attachment': attachment})


